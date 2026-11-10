"""Prepare the isolated YZ250 listening prototype from the supplied recording.

Keeps every decoded stereo sample. RPM and load are acoustic estimates, not
tachometer/torque measurements. No per-grain normalization or cycle extraction.
"""
import argparse
import array
import cmath
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import wave


def fft(values):
    data = [complex(value) for value in values]
    size = len(data)
    j = 0
    for i in range(1, size):
        bit = size >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            data[i], data[j] = data[j], data[i]
    length = 2
    while length <= size:
        step = cmath.exp(-2j * math.pi / length)
        for start in range(0, size, length):
            factor = 1
            for offset in range(length // 2):
                a, b = data[start+offset], data[start+offset+length//2] * factor
                data[start+offset], data[start+offset+length//2] = a+b, a-b
                factor *= step
        length *= 2
    return data


def prepare(source, recording, output):
    with wave.open(str(source), 'rb') as audio:
        assert (audio.getframerate(), audio.getnchannels(), audio.getsampwidth()) == (44100, 2, 2)
        raw = audio.readframes(audio.getnframes())
    samples = array.array('h', raw)
    if sys.byteorder != 'little':
        samples.byteswap()
    mono = [(samples[i]+samples[i+1])/65536 for i in range(0, len(samples), 2)]
    # Anti-aliased decimation is only used for analysis. Playback uses raw PCM.
    reduced, low = [], 0.0
    for i,value in enumerate(mono):
        low += 0.22*(value-low)
        if i % 4 == 0:
            reduced.append(low)
    size, rate, hop = 2048, 11025, 882
    frequencies = list(range(35, 231, 2))
    frames = []
    for centre in range(5000, len(mono)-5000, hop):
        begin = centre//4-size//2
        if begin < 0 or begin+size > len(reduced):
            continue
        block = reduced[begin:begin+size]
        spectrum = fft([value*(0.5-0.5*math.cos(2*math.pi*i/(size-1))) for i,value in enumerate(block)])
        power = [abs(value)**2 for value in spectrum[:size//2]]
        # Local spectral contrast follows multiple harmonics instead of simply
        # interpreting the loudest exhaust resonance as the firing frequency.
        contrast = []
        for i,value in enumerate(power):
            neighbours = power[max(1,i-12):min(len(power),i+13)]
            floor = sum(neighbours)/max(1,len(neighbours))
            contrast.append(math.log1p(value/(floor+1e-12)))
        scores = []
        for frequency in frequencies:
            score = 0.0
            for harmonic in range(1, 13):
                index = round(frequency*harmonic*size/rate)
                score += max(contrast[max(1,index-1):index+2]) / harmonic**0.8
            scores.append(score)
        rms = math.sqrt(sum(value*value for value in block)/size)
        frames.append({'frame': centre, 'rms': rms, 'scores': scores})
    # Continuous pitch path; octave jumps are penalized, not silently relabelled.
    costs, parents = [], []
    for t,frame in enumerate(frames):
        local = frame['scores']
        scale = max(local) or 1
        observation = [-value/scale for value in local]
        if t == 0:
            costs = observation
            parents.append([0]*len(frequencies))
        else:
            following, links = [], []
            for j,frequency in enumerate(frequencies):
                candidates = [(costs[k]+2.5*abs(math.log2(frequency/previous)),k)
                              for k,previous in enumerate(frequencies)]
                value,k = min(candidates)
                following.append(value+observation[j]); links.append(k)
            costs = following; parents.append(links)
    path = [min(range(len(costs)),key=costs.__getitem__)]
    for t in range(len(frames)-1,0,-1):
        path.append(parents[t][path[-1]])
    path.reverse()
    peak = max(frame['rms'] for frame in frames)
    for i,(frame,index) in enumerate(zip(frames,path)):
        frame['rpm'] = frequencies[index]*60
        frame['confidence'] = frame['scores'][index]/max(frame['scores'])
        a,b = max(0,i-3),min(len(frames)-1,i+3)
        slope = (frequencies[path[b]]-frequencies[path[a]])*60 / max(0.02,(frames[b]['frame']-frames[a]['frame'])/44100)
        frame['load'] = max(0.0,min(1.0,0.5+slope/10000))
        frame['usable'] = frame['rms'] > peak*0.08 and frame['confidence'] > 0.7
        del frame['scores']
    usable = [frame for frame in frames if frame['usable']]
    assert len(usable) > 30
    minimum,maximum = min(f['rpm'] for f in usable),max(f['rpm'] for f in usable)
    output.mkdir(parents=True,exist_ok=True)
    (output/'Reference.pcm').write_bytes(raw)
    packed = b''.join(struct.pack('<IHHHH',frame['frame'],frame['rpm'],round(frame['load']*1000),round(frame['confidence']*1000),round(frame['rms']*32768)) for frame in usable)
    (output/'Grains.bin').write_bytes(packed)
    report = {'source':recording.name,'source_sha256':hashlib.sha256(recording.read_bytes()).hexdigest(),
              'decoded_pcm_sha256':hashlib.sha256(raw).hexdigest(),'sample_rate':44100,'channels':2,
              'frames':len(mono),'duration_seconds':len(mono)/44100,'grain_samples':5292,'hop_samples':1323,
              'rpm_estimated_min':minimum,'rpm_estimated_max':maximum,'rpm_calibrated':False,
              'load_measured':False,'load_description':'pitch-rise versus pitch-fall proxy; not measured torque',
              'analysis':frames}
    (output/'Analysis.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Decoded stereo retained:',len(mono)/44100,'s; usable centres:',len(usable),'estimated RPM:',minimum,maximum)
    for frame in frames[::25]:
        print(round(frame['frame']/44100,2),'s',frame['rpm'],'rpm',round(frame['load'],2),'load',round(frame['rms'],3),'rms')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wav',type=Path); parser.add_argument('recording',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    prepare(args.wav,args.recording,args.output)
