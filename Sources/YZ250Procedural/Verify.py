"""Verify rendered audio, not just the oscillator's internal counters.

Run after --render. Reports fixed-RPM pitch and short-term level variation,
then checks the rendered sweeps and their indefinite end-RPM holds.
Uses only Python's standard library. Listening remains the timbre test.
"""
import argparse
import array
import csv
import json
import math
from pathlib import Path
import statistics
import sys
import wave
sys.dont_write_bytecode = True
from Calibrate import fft

RATE = 44100


def read(path):
    with wave.open(str(path), 'rb') as w:
        assert (w.getframerate(), w.getnchannels(), w.getsampwidth()) == (RATE, 2, 2)
        pcm = array.array('h', w.readframes(w.getnframes()))
    if sys.byteorder != 'little':
        pcm.byteswap()
    assert all(pcm[i] == pcm[i+1] for i in range(0, len(pcm), 2)), 'unexpected stereo phase difference'
    values = [pcm[i]/32768 for i in range(0, len(pcm), 2)]
    assert max(map(abs, values)) < .99
    return values


def pitch(values, expected):
    n = len(values)
    power = [abs(v)**2 for v in fft([v*(.5-.5*math.cos(2*math.pi*i/n)) for i,v in enumerate(values)])[:n//2]]
    estimates = []
    # Independent spectral peaks across multiple combustion harmonics.
    for order in range(1, 13):
        index = round(expected/60*order*n/RATE)
        k = max(range(max(2,index-2), index+3), key=power.__getitem__)
        a,b,c = [math.log(max(1e-20, power[j])) for j in (k-1,k,k+1)]
        offset = max(-.5, min(.5, .5*(a-c)/(a-2*b+c)))
        rpm = (k+offset)*RATE/n*60/order
        estimates.append((power[k], rpm))
    # The strongest four peaks avoid weak orders buried in the noisy texture.
    strongest = sorted(estimates, reverse=True)[:4]
    return sum(w*r for w,r in strongest)/sum(w for w,r in strongest)


def verify(prefix):
    report = {}
    for name, rpm in [('Fixed-4500',4500), ('Fixed-7000',7000), ('Fixed-9500',9500), ('Load-Low',7000), ('Load-High',7000)]:
        values = read(Path(str(prefix)+'-'+name+'.wav'))
        assert len(values) == 8*RATE
        estimates = [pitch(values[i:i+16384], rpm) for i in range(RATE, len(values)-16384, RATE//2)]
        rms = [math.sqrt(sum(v*v for v in values[i:i+8820])/8820) for i in range(RATE, len(values)-8820, 8820)]
        maximum_error = max(abs(v/rpm-1) for v in estimates)
        variation = statistics.pstdev(rms)/statistics.mean(rms)
        assert maximum_error < .007, (name, 'unstable spectral pitch', estimates)
        assert variation < .15, (name, 'unstable short-term level', variation)
        report[name] = dict(spectral_rpm_min=min(estimates), spectral_rpm_max=max(estimates),
                            max_pitch_error_percent=maximum_error*100,
                            rms_coefficient_of_variation=variation, rms=statistics.mean(rms),
                            peak=max(map(abs, values)))
    assert report['Load-High']['rms'] > report['Load-Low']['rms']*1.2, 'inaudible load energy change'
    for name, seconds in [('Ramp-Slow',5), ('Ramp-Fast',1)]:
        values = read(Path(str(prefix)+'-'+name+'.wav'))
        assert len(values) == 12*RATE
        with Path(str(prefix)+'-'+name+'.csv').open() as f:
            rows = list(csv.DictReader(f))
        previous = 0
        max_rpm_error = 0
        for row in rows:
            time = int(row['frame'])/RATE
            actual = float(row['rpm'])
            expected = 3660+6840*max(0, min(1,(time-1)/seconds))
            max_rpm_error = max(max_rpm_error, abs(actual-expected))
            assert actual >= previous, 'non-monotonic ramp'
            previous = actual
        assert max_rpm_error < .02
        # Validate moving pitch in the waveform using dechirped order-domain
        # analysis. No telemetry is used to resample the audio: the prescribed
        # test trajectory analytically determines crank phase.
        estimates = []
        for fraction in [.2,.4,.6,.8]:
            time = 1+seconds*fraction
            centre_rpm = 3660+6840*fraction
            # 0.12 s window; phase-domain sampling removes deterministic chirp.
            start = round((time-.06)*RATE)
            phase = 0.0
            phases = []
            for i in range(start, start+round(.12*RATE)):
                t = i/RATE
                phase += (3660+6840*max(0,min(1,(t-1)/seconds)))/60/RATE
                phases.append(phase)
            count = 4096
            cycles = phases[-1]
            positions, cursor = [], 0
            for j in range(count):
                target = j*cycles/count
                while cursor+1 < len(phases)-1 and phases[cursor+1] < target:
                    cursor += 1
                mix = max(0, min(1,(target-phases[cursor])/(phases[cursor+1]-phases[cursor])))
                positions.append(values[start+cursor]*(1-mix)+values[start+cursor+1]*mix)
            spectrum = [abs(v)**2 for v in fft([v*(.5-.5*math.cos(2*math.pi*j/count)) for j,v in enumerate(positions)])[:count//2]]
            peak = max(range(round(cycles*.8), round(cycles*1.2)+1), key=spectrum.__getitem__)
            # Search the first combustion order, allowing one FFT bin due to
            # this short window. Gross pitch jumps would fail this check.
            assert abs(peak-cycles) < 1.5, (name, 'sweep audio pitch mismatch', fraction)
            estimates.append(dict(fraction=fraction, expected_rpm=centre_rpm, first_order_peak=peak, expected_order_bin=cycles))
        hold = [pitch(values[i:i+16384],10500) for i in range(8*RATE,11*RATE,RATE//2)]
        assert max(abs(v/10500-1) for v in hold) < .007
        report[name] = dict(max_command_error_rpm=max_rpm_error,
                            hold_spectral_rpm_min=min(hold), hold_spectral_rpm_max=max(hold),
                            sweep_audio_checks=estimates, peak=max(map(abs, values)))
    # The runtime closure may contain numeric parameters, but no sample read or
    # import of the earlier granular voice. Offline.sx writes exports only.
    directory = Path(__file__).parent
    for name in ['Main.sx','Voice.sx','Calibration.sx','Session.sx']:
        source = (directory/name).read_text()
        assert all(token not in source for token in ['embed_bytes', 'File.read', 'Module.Bank', 'Module.YZ250', 'Reference.pcm', 'Grains.bin'])
    destination = Path(str(prefix)+'-Verification.json')
    destination.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    print('Audio verification passed; listening approval remains required.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prefix', type=Path)
    verify(parser.parse_args().prefix)
