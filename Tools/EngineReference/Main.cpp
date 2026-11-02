#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
#include <compiler.h>
#include <impulse_response.h>
#include <piston_engine_simulator.h>

// -----------------------------------------------------------------------------

class CapturingSimulator : public PistonEngineSimulator {

    // -------------------------------------------------------------------------
    // API

    public: std::vector<float> trace;
    public: bool recording { false };

    // -------------------------------------------------------------------------
    // INTERNALS

    protected: void writeToSynthesizer() override {
        PistonEngineSimulator::writeToSynthesizer();
        if (!recording) return;
        trace.push_back(static_cast<float>(m_engine->getRpm()));
        trace.push_back(static_cast<float>(m_engine->getOutputCrankshaft()->getCycleAngle()));
        for (int index = 0; index < m_engine->getExhaustSystemCount(); ++index) {
            trace.push_back(static_cast<float>(m_exhaustFlowStagingBuffer[index]));
        }
    }
};

// -----------------------------------------------------------------------------

static void writeInteger(std::ostream& stream, uint32_t value, int bytes) {
    for (int index = 0; index < bytes; ++index) {
        stream.put(static_cast<char>((value >> (index * 8)) & 255));
    }
}

static void writeWave(const std::string& path, const std::vector<int16_t>& samples) {
    std::ofstream stream(path, std::ios::binary);
    if (!stream) throw std::runtime_error("Cannot open output: " + path);
    stream.write("RIFF", 4);
    writeInteger(stream, 36 + samples.size() * 2, 4);
    stream.write("WAVEfmt ", 8);
    writeInteger(stream, 16, 4);
    writeInteger(stream, 1, 2);
    writeInteger(stream, 1, 2);
    writeInteger(stream, 44100, 4);
    writeInteger(stream, 88200, 4);
    writeInteger(stream, 2, 2);
    writeInteger(stream, 16, 2);
    stream.write("data", 4);
    writeInteger(stream, samples.size() * 2, 4);
    for (int16_t sample : samples) writeInteger(stream, static_cast<uint16_t>(sample), 2);
    if (!stream) throw std::runtime_error("Cannot write output: " + path);
}

static std::vector<int16_t> readImpulse(const std::string& path) {
    std::ifstream stream(path, std::ios::binary | std::ios::ate);
    if (!stream || stream.tellg() <= 0 || stream.tellg() % 2 != 0) {
        throw std::runtime_error("Invalid mono PCM16 impulse: " + path);
    }
    std::vector<int16_t> samples(static_cast<size_t>(stream.tellg()) / 2);
    stream.seekg(0);
    stream.read(reinterpret_cast<char*>(samples.data()), samples.size() * 2);
    if (!stream) throw std::runtime_error("Cannot read impulse");
    return samples;
}

// -----------------------------------------------------------------------------

static void renderQuantum(CapturingSimulator& simulator, Engine& engine, std::vector<int16_t>& samples) {
    Synthesizer& synthesizer = simulator.synthesizer();
    simulator.startFrame(0.01);
    while (simulator.simulateStep()) {}
    const int available = static_cast<int>(synthesizer.m_inputChannels[0].data.size());
    const auto parameters = synthesizer.getAudioParameters();
    for (int channel = 0; channel < engine.getExhaustSystemCount(); ++channel) {
        synthesizer.m_inputChannels[channel].data.read(available, synthesizer.m_inputChannels[channel].transferBuffer);
        synthesizer.m_filters[channel].jitterFilter.setJitterScale(parameters.inputSampleNoise);
    }
    for (int index = 0; index < available; ++index) samples.push_back(synthesizer.renderAudio(index));
    for (int channel = 0; channel < engine.getExhaustSystemCount(); ++channel) {
        synthesizer.m_inputChannels[channel].data.removeBeginning(available);
    }
}

static void serve(CapturingSimulator& simulator, Engine& engine) {
    std::vector<int16_t> pending;
    pending.reserve(2048);
    int frames = 0;
    int ignition = 0;
    double pedal = 0;
    double texture = 1;
    double convolution = 1;
    double baseRpm = 800;
    double load = 0;
    double contactTime = 0;
    double throttle = 0;
    bool wasRunning = false;
    while (std::cin >> frames >> ignition >> pedal >> texture >> convolution >> baseRpm >> load) {
        if (frames < 1 || frames > 960 || ignition < 0 || ignition > 1 ||
            !std::isfinite(pedal) || pedal < 0 || pedal > 1 ||
            !std::isfinite(texture) || texture < 0 || texture > 1 ||
            !std::isfinite(convolution) || convolution < 0 || convolution > 1 ||
            !std::isfinite(baseRpm) || baseRpm < 700 || baseRpm > 2000 ||
            !std::isfinite(load) || load < 0 || load > 1) {
            throw std::runtime_error("Invalid reference-render request");
        }
        if (ignition && !wasRunning) contactTime = 0;
        wasRunning = ignition;
        auto parameters = simulator.synthesizer().getAudioParameters();
        parameters.airNoise = texture * engine.getInitialNoise();
        parameters.inputSampleNoise = texture * engine.getInitialJitter();
        parameters.convolution = convolution;
        parameters.volume = 0.5;
        simulator.synthesizer().setAudioParameters(parameters);
        while (pending.size() < static_cast<size_t>(frames)) {
            const bool starter = ignition && contactTime < 1.2 && engine.getRpm() < 650;
            simulator.m_starterMotor.m_enabled = starter;
            engine.getIgnitionModule()->m_enabled = ignition;
            const double requestedThrottle = ignition && !starter ? 0.35 * pedal : 0;
            throttle += 0.16 * (requestedThrottle - throttle);
            engine.setSpeedControl(throttle);
            const bool heldSpeed = ignition && pedal == 0 && baseRpm > 800 && engine.getRpm() > 600;
            simulator.m_dyno.m_hold = heldSpeed;
            simulator.m_dyno.m_enabled = heldSpeed || (ignition && pedal > 0 && load > 0 && engine.getRpm() > 900);
            simulator.m_dyno.m_rotationSpeed = units::rpm(baseRpm);
            simulator.m_dyno.m_maxTorque = heldSpeed ? 10000 : load * 250;
            renderQuantum(simulator, engine, pending);
            if (ignition) contactTime += 0.01;
        }
        writeInteger(std::cout, 0x34563845, 4);
        writeInteger(std::cout, frames, 4);
        writeInteger(std::cout, static_cast<uint32_t>(std::round(engine.getRpm() * 1000)), 4);
        writeInteger(std::cout, ignition && (contactTime < 1.2 || engine.getRpm() < 650), 4);
        for (int index = 0; index < frames; ++index) writeInteger(std::cout, static_cast<uint16_t>(pending[index]), 2);
        std::cout.flush();
        if (!std::cout) throw std::runtime_error("Reference output pipe closed");
        pending.erase(pending.begin(), pending.begin() + frames);
    }
    if (!std::cin.eof()) throw std::runtime_error("Malformed reference-render request");
}

// -----------------------------------------------------------------------------

static void renderOffline(CapturingSimulator& simulator, Engine& engine, const std::string& prefix) {
    std::vector<int16_t> samples;
    std::ofstream states(prefix + ".csv");
    if (!states) throw std::runtime_error("Cannot open state output");
    states << "seconds,rpm,throttle,ignition,starter\n";
    simulator.recording = true;
    for (int block = 0; block < 1400; ++block) {
        const double time = block * 0.01;
        const bool ignition = time >= 0.3 && time < 11.5;
        const bool starter = time >= 0.3 && time < 1.5;
        const double pedal = time >= 5 && time < 7 ? 0.35 : 0;
        engine.getIgnitionModule()->m_enabled = ignition;
        simulator.m_starterMotor.m_enabled = starter;
        engine.setSpeedControl(pedal);
        renderQuantum(simulator, engine, samples);
        states << time << ',' << engine.getRpm() << ',' << pedal << ',' << ignition << ',' << starter << '\n';
        if (block % 100 == 0) {
            std::printf("t=%.1f, rpm=%.1f\n", time, engine.getRpm());
            std::fflush(stdout);
        }
    }
    writeWave(prefix + ".wav", samples);
    std::ofstream trace(prefix + ".f32", std::ios::binary);
    trace.write(reinterpret_cast<const char*>(simulator.trace.data()), simulator.trace.size() * sizeof(float));
    std::printf("Output: %zu frames, %.6f seconds\n", samples.size(), samples.size() / 44100.0);
    if (!states || !trace) throw std::runtime_error("Cannot write diagnostic trace");
}

// -----------------------------------------------------------------------------

int main(int count, char** arguments) {
    try {
        if (count != 5) {
            std::fprintf(stderr, "Usage: RenderReference profile.mr impulse.pcm output-prefix full|base|serve\n");
            return 2;
        }
        const std::string mode = arguments[4];
        if (mode != "full" && mode != "base" && mode != "serve") throw std::runtime_error("Unknown rendering mode");
        const auto impulse = readImpulse(arguments[2]);
        std::srand(42);
        es_script::Compiler compiler;
        compiler.initialize();
        if (!compiler.compile(arguments[1])) {
            compiler.destroy();
            throw std::runtime_error("Profile compile failed; see error_log.log");
        }
        const auto output = compiler.execute();
        compiler.destroy();
        if (!output.engine) throw std::runtime_error("Profile did not produce an engine");
        Engine& engine = *output.engine;
        std::fprintf(stderr, "Engine: %s, mode: %s\n", engine.getName().c_str(), mode.c_str());
        std::fflush(stderr);
        Vehicle vehicle;
        Vehicle::Parameters vehicleParameters;
        vehicleParameters.mass = 1597;
        vehicleParameters.diffRatio = 3.42;
        vehicleParameters.tireRadius = 10 * units::inch;
        vehicleParameters.dragCoefficient = 0.25;
        vehicleParameters.crossSectionArea = 36 * units::foot * units::foot;
        vehicleParameters.rollingResistance = 2000;
        vehicle.initialize(vehicleParameters);
        Transmission transmission;
        const double ratios[] = {2.97, 2.07, 1.43, 1.0, 0.84, 0.56};
        Transmission::Parameters transmissionParameters;
        transmissionParameters.GearCount = 6;
        transmissionParameters.GearRatios = ratios;
        transmissionParameters.MaxClutchTorque = 1000 * units::ft_lb;
        transmission.initialize(transmissionParameters);
        CapturingSimulator simulator;
        Simulator::Parameters simulatorParameters;
        simulator.initialize(simulatorParameters);
        simulator.setSimulationFrequency(static_cast<int>(engine.getSimulationFrequency()));
        simulator.loadSimulation(&engine, &vehicle, &transmission);
        simulator.setFluidSimulationSteps(8);
        simulator.setTargetSynthesizerLatency(0);
        Synthesizer& synthesizer = simulator.synthesizer();
        synthesizer.m_latency = 0;
        auto parameters = synthesizer.getAudioParameters();
        parameters.inputSampleNoise = mode == "base" ? 0 : engine.getInitialJitter();
        parameters.airNoise = mode == "base" ? 0 : engine.getInitialNoise();
        parameters.dF_F_mix = mode == "base" ? 0 : engine.getInitialHighFrequencyGain();
        parameters.convolution = mode == "base" ? 0 : 1;
        parameters.volume = 0.7;
        synthesizer.setAudioParameters(parameters);
        for (int index = 0; index < engine.getExhaustSystemCount(); ++index) {
            const double volume = engine.getExhaustSystem(index)->getImpulseResponse()->getVolume();
            synthesizer.initializeImpulseResponse(impulse.data(), impulse.size(), volume, index);
        }
        if (mode == "serve") serve(simulator, engine);
        else renderOffline(simulator, engine, arguments[3]);
        synthesizer.destroy();
        simulator.destroy();
        engine.destroy();
        delete output.engine;
        for (Function* function : output.functions) {
            function->destroy();
            delete function;
        }
        return 0;
    } catch (const std::exception& error) {
        std::fprintf(stderr, "%s\n", error.what());
        return 1;
    }
}
