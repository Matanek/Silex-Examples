"""Offline acoustic calibration. Emits spectral parameters, never PCM or cycles.

Uses the earlier pitch path only as an acoustic estimate. Absolute RPM and
rising/falling load proxies are not tachometer or torque measurements.
Python standard library only; no runtime dependency on this tool or recording.
"""
import argparse
import array
import bisect
import cmath
import hashlib
import json
import math
from pathlib import Path
import sys
import wave


def fft(values, inverse=False):
    data = list(map(complex, values))
    n = len(data)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            data[i], data[j] = data[j], data[i]
    length = 2
    while length <= n:
        step = cmath.exp((2j if inverse else -2j) * math.pi / length)
        for start in range(0, n, length):
            factor = 1
            for k in range(length // 2):
                a, b = data[start+k], data[start+k+length//2] * factor
                data[start+k], data[start+k+length//2] = a+b, a-b
                factor *= step
        length *= 2
    return [v/n for v in data] if inverse else data


RPMS = [3660, 4500, 6000, 7500, 9000, 10500]
BANDS = [250, 500, 1000, 2000, 4000, 8000]
PARTIALS = 64
RATE = 44100


def filter_parameters(frequency):
    w = 2*math.pi*frequency/RATE
    alpha = math.sin(w)/(2*0.7)
    b0, b2 = alpha/(1+alpha), -alpha/(1+alpha)
    a1, a2 = -2*math.cos(w)/(1+alpha), (1-alpha)/(1+alpha)
    # Unit-white-noise RMS from impulse energy, including PRNG variance 1/3.
    x1 = x2 = y1 = y2 = energy = 0.0
    for i in range(8192):
        x = float(i == 0)
        y = b0*x + b2*x2 - a1*y1 - a2*y2
        x2, x1, y2, y1 = x1, x, y1, y
        energy += y*y
    return [b0, b2, a1, a2, math.sqrt(3/energy)]


def calibrate(wav_path, analysis_path, source_path, output):
    with wave.open(str(wav_path), 'rb') as w:
        assert (w.getframerate(), w.getnchannels(), w.getsampwidth()) == (RATE, 2, 2)
        raw = w.readframes(w.getnframes())
    analysis_bytes = analysis_path.read_bytes()
    analysis = json.loads(analysis_bytes)
    assert hashlib.sha256(raw).hexdigest() == analysis['decoded_pcm_sha256']
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == analysis['source_sha256']
    pcm = array.array('h', raw)
    if sys.byteorder != 'little':
        pcm.byteswap()
    mono = [(pcm[i]+pcm[i+1])/65536 for i in range(0, len(pcm), 2)]
    path = analysis['analysis']
    centres = [p['frame'] for p in path]

    def pitch(frame):
        i = max(0, min(len(path)-2, bisect.bisect_right(centres, frame)-1))
        t = max(0, min(1, (frame-centres[i])/(centres[i+1]-centres[i])))
        return (path[i]['rpm']*(1-t)+path[i+1]['rpm']*t)/60

    observations = []
    for p in path[::6]:
        if not p['usable']:
            continue
        f0 = p['rpm']/60
        # Follow local crank order over six cycles, rather than treating a
        # pitch-changing 120 ms excerpt as stationary.
        start = max(0, round(p['frame']-3*RATE/f0))
        phase, positions = 0.0, [float(start)]
        cursor = start
        while phase < 6 and cursor+1 < len(mono):
            following = phase + pitch(cursor)/RATE
            while len(positions) < 4096 and len(positions)*6/4096 <= following:
                target = len(positions)*6/4096
                positions.append(cursor+(target-phase)/(following-phase))
            phase = following
            cursor += 1
        if len(positions) != 4096:
            continue
        values = []
        for position in positions:
            i = int(position)
            t = position-i
            values.append(mono[i]*(1-t)+mono[i+1]*t)
        rms = math.sqrt(sum(v*v for v in values)/len(values))
        windowed = [v*(.5-.5*math.cos(2*math.pi*i/4096)) for i,v in enumerate(values)]
        power = [abs(v)**2 for v in fft(windowed)[:2048]]
        total = sum(power[1:])+1e-20
        assigned = set()
        harmonics = []
        for order in range(1, PARTIALS+1):
            bins = range(order*6-2, order*6+3)
            # Local inter-order background is left stochastic. Do not force
            # every bit of recorded energy into a perfectly periodic buzz.
            floor = min(power[order*6-3], power[order*6+3])
            energy = sum(max(0, power[k]-floor) for k in bins)
            assigned.update(bins)
            harmonics.append(energy/total*rms*rms)
        noise = [0.0]*len(BANDS)
        residual = max(0, rms*rms-sum(harmonics))
        for k, value in enumerate(power[1:], 1):
            if k in assigned:
                continue
            frequency = k*f0/6
            band = min(range(len(BANDS)), key=lambda b: abs(math.log2(max(1, frequency)/BANDS[b])))
            noise[band] += value
        scale = residual/(sum(noise)+1e-20)
        noise = [v*scale for v in noise]
        observations.append(dict(frame=p['frame'], rpm=p['rpm'], load=p['load'],
                                 rms=rms, harmonic_energy=harmonics, noise_energy=noise,
                                 crest=max(map(abs, values))/max(rms, 1e-9)))
    nodes, support = [], []
    for rpm in RPMS:
        for load in [0, 1]:
            weights = [math.exp(-.5*(math.log2(o['rpm']/rpm)/.19)**2)*(.15+.85*(o['load'] if load else 1-o['load'])) for o in observations]
            total = sum(weights)
            harmonics = [math.sqrt(2*sum(w*o['harmonic_energy'][h] for w,o in zip(weights, observations))/total) for h in range(PARTIALS)]
            noise = [math.sqrt(sum(w*o['noise_energy'][b] for w,o in zip(weights, observations))/total) for b in range(len(BANDS))]
            nodes.append(harmonics+noise)
            support.append(dict(rpm=rpm, load_proxy=load, effective_observations=round(total, 3),
                                rms=math.sqrt(sum(v*v/2 for v in harmonics)+sum(v*v for v in noise))))
    # One minimum-phase pressure-pulse shape from the average magnitude.
    # No phase or single-cycle waveform is copied from the recording.
    envelope = [sum(node[h] for node in nodes)/len(nodes) for h in range(PARTIALS)]
    log_spectrum = [math.log(max(1e-7, envelope[0]))]+[math.log(max(1e-7, v)) for v in envelope]
    log_spectrum += log_spectrum[-2:0:-1]
    cepstrum = fft(log_spectrum, inverse=True)
    causal = [cepstrum[0]]+[2*v for v in cepstrum[1:64]]+[cepstrum[64]]+[0]*63
    minimum = fft(causal)
    phases = [minimum[h].imag-h*minimum[1].imag for h in range(1, 65)]
    crest = sorted(o['crest'] for o in observations)[len(observations)//2]
    width = max(.035, min(.25, 1/(crest*crest)))
    coefficients = [filter_parameters(f) for f in BANDS]
    # E[(.3+.7*exp(-phase/width))^2] for phase uniformly in [0,1].
    envelope_rms = math.sqrt(.09+.42*width*(1-math.exp(-1/width))+.49*width/2*(1-math.exp(-2/width)))
    def numbers(values):
        return ', '.join(format(v, '.10g') if v != 0 else '0.0' for v in values)
    sx = ('// Generated by Calibrate.py: acoustic parameters only, no waveform samples.\n'
          'public class Calibration {\n'
          '    let rpms:float64[] = ['+numbers(RPMS)+']\n'
          '    let nodes:float64[] = [\n'+''.join('        '+numbers(node)+',\n' for node in nodes)+'    ]\n'
          '    let cosine:float64[] = ['+numbers([math.cos(v) for v in phases])+']\n'
          '    let sine:float64[] = ['+numbers([math.sin(v) for v in phases])+']\n'
          '    let filters:float64[] = ['+numbers([v for c in coefficients for v in c])+']\n'
          f'    let burst_width:float64 = {width:.10g}\n'
          f'    let burst_rms:float64 = {envelope_rms:.10g}\n'
          '}\n')
    output.mkdir(parents=True, exist_ok=True)
    (output/'Calibration.sx').write_text(sx)
    report = dict(source=source_path.name, source_sha256=analysis['source_sha256'],
                  decoded_pcm_sha256=analysis['decoded_pcm_sha256'], pitch_path_sha256=hashlib.sha256(analysis_bytes).hexdigest(),
                  calibration_sha256=hashlib.sha256(sx.encode()).hexdigest(),
                  method='six-cycle order-domain energy; 64 harmonic magnitudes + 6 stochastic bands; shared analytic minimum phase',
                  rpm_calibrated=False, load_measured=False,
                  load_description='rising/falling pitch proxy, not measured torque',
                  observations=len(observations), source_rms=math.sqrt(sum(v*v for v in mono)/len(mono)),
                  median_crest=crest, burst_width_cycles=width, nodes=support)
    (output/'Calibration.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('wav', type=Path)
    p.add_argument('pitch_analysis', type=Path)
    p.add_argument('source', type=Path)
    p.add_argument('output', type=Path)
    a = p.parse_args()
    calibrate(a.wav, a.pitch_analysis, a.source, a.output)
