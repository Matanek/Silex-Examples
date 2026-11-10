"""Prepare short, phase-aligned multi-cycle loops from the supplied YZ250.

Offline pitch flattening preserves recorded PCM texture, including stochastic
and mechanical detail. No harmonic reconstruction or isolated-cycle synthesis.
Original archives and the earlier analysis remain read-only inputs.
"""
import argparse
import array
import bisect
import cmath
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import wave

RATE = 44100
RPMS = [3660, 4500, 6000, 7500, 9000, 10500]
CYCLES = 32
OVERLAP = 4
POINTS = 512


def fft(values, inverse=False):
    data = list(map(complex, values)); n = len(data); j = 0
    for i in range(1,n):
        bit = n>>1
        while j & bit:
            j ^= bit; bit >>= 1
        j ^= bit
        if i < j:
            data[i],data[j] = data[j],data[i]
    length = 2
    while length <= n:
        step = cmath.exp((2j if inverse else -2j)*math.pi/length)
        for start in range(0,n,length):
            factor = 1
            for k in range(length//2):
                a,b = data[start+k],data[start+k+length//2]*factor
                data[start+k],data[start+k+length//2] = a+b,a-b
                factor *= step
        length *= 2
    return [v/n for v in data] if inverse else data


def smooth(values, coefficient, passes=2):
    result = list(values)
    for _ in range(passes):
        value = result[0]
        for i in range(len(result)):
            value += coefficient*(result[i]-value); result[i] = value
        value = result[-1]
        for i in range(len(result)-1,-1,-1):
            value += coefficient*(result[i]-value); result[i] = value
    return result


def prepare(wav, analysis_path, original, output):
    analysis = json.loads(analysis_path.read_text())
    with wave.open(str(wav),'rb') as w:
        assert (w.getframerate(),w.getnchannels(),w.getsampwidth()) == (RATE,2,2)
        raw = w.readframes(w.getnframes())
    assert hashlib.sha256(raw).hexdigest() == analysis['decoded_pcm_sha256']
    assert hashlib.sha256(original.read_bytes()).hexdigest() == analysis['source_sha256']
    pcm = array.array('h',raw)
    if sys.byteorder != 'little':
        pcm.byteswap()
    mono = [(pcm[2*i]+pcm[2*i+1])/65536 for i in range(len(pcm)//2)]
    path = analysis['analysis']; centres = [p['frame'] for p in path]
    predicted, phase, cursor = [], 0.0, 0
    for i in range(len(mono)):
        while cursor+1 < len(path)-1 and i > centres[cursor+1]:
            cursor += 1
        mix = max(0,min(1,(i-centres[cursor])/(centres[cursor+1]-centres[cursor])))
        frequency = (path[cursor]['rpm']*(1-mix)+path[cursor+1]['rpm']*mix)/60
        phase += frequency/RATE
        predicted.append(phase)
    # Demodulate the fundamental around the coarse pitch path; a zero-phase
    # low-pass suppresses neighboring harmonics. Unwrapped residual phase
    # corrects the pitch drift hidden inside the earlier 120 ms grains.
    demodulated = [v*cmath.exp(-2j*math.pi*p) for v,p in zip(mono,predicted)]
    fundamental = smooth(demodulated,1-math.exp(-2*math.pi*16/RATE))
    residual, unwrapped, previous = [], 0.0, cmath.phase(fundamental[0])
    for value in fundamental:
        angle = cmath.phase(value)
        change = (angle-previous+math.pi)%(2*math.pi)-math.pi
        unwrapped += change; residual.append(unwrapped/(2*math.pi)); previous = angle
    # Residual is a continuous phase correction, never a fresh phase per grain.
    corrected = [p+r for p,r in zip(predicted,residual)]
    # Phase is undefined when this partial nearly disappears. Select the
    # longest monotonic analysis interval instead of clamping phase jumps and
    # baking fake timing into the loops. Record the excluded interval below.
    breaks = [0]+[i for i in range(1,len(corrected)) if corrected[i]<=corrected[i-1]]+[len(corrected)-1]
    left,right = max(zip(breaks,breaks[1:]),key=lambda pair: pair[1]-pair[0])
    analysis_begin = left + RATE//10
    analysis_end = right - RATE//10
    assert analysis_end-analysis_begin > 8*RATE

    def sample(channel,turn):
        i = max(0,min(len(corrected)-2,bisect.bisect_right(corrected,turn,analysis_begin,analysis_end)-1))
        mix = (turn-corrected[i])/(corrected[i+1]-corrected[i])
        return (pcm[2*i+channel]*(1-mix)+pcm[2*(i+1)+channel]*mix)/32768

    def joined(a,b):
        # Equal expected energy through a join, accounting for correlation.
        # This is a fixed offline window calibration, not an audio limiter.
        ea=sum(v*v for v in a)/len(a); eb=sum(v*v for v in b)/len(b)
        covariance=sum(x*y for x,y in zip(a,b))/len(a)
        output=[]
        for i,(x,y) in enumerate(zip(a,b)):
            mix=.5-.5*math.cos(math.pi*i/len(a))
            measured=(1-mix)**2*ea+mix**2*eb+2*mix*(1-mix)*covariance
            desired=(1-mix)*ea+mix*eb
            gain=math.sqrt(desired/max(1e-20,measured))
            output.append(((1-mix)*x+mix*y)*gain)
        return output

    rising_regions=[]
    for observation in path:
        if observation['load'] < .7:
            continue
        time=observation['frame']/RATE
        if rising_regions and time-rising_regions[-1][1] < .15:
            rising_regions[-1][1]=time
        else:
            rising_regions.append([time,time])
    packed, entries, all_loops = bytearray(), [], []
    for node,rpm in enumerate(RPMS):
        for loaded in [False,True]:
            # Keep the accepted low/mid loaded material unchanged. Refine only
            # the coast floor and upper loaded nodes, using short rising spans.
            refined_idle = node == 0 and not loaded
            refined_loaded = node >= 3 and loaded
            source_cycles = 16 if refined_idle or refined_loaded else CYCLES
            candidates = []
            for p in path:
                centre = p['frame']
                start = math.ceil(corrected[centre]-(source_cycles+OVERLAP)/2)
                begin = bisect.bisect_left(corrected,start)
                end = bisect.bisect_left(corrected,start+source_cycles+OVERLAP)
                if start < corrected[analysis_begin] or begin < analysis_begin or end >= analysis_end:
                    continue
                within = [q for q in path if begin <= q['frame'] < end]
                if not within:
                    continue
                distance = sum(math.log2(q['rpm']/rpm)**2 for q in within)/len(within)
                load = sum(q['load'] for q in within)/len(within)
                if refined_loaded and load < .85:
                    continue
                cost = 5*distance + .5*abs(load-int(loaded))
                mean=0.0
                if refined_idle or refined_loaded:
                    # Prefer an even recorded cadence, not an accelerating or
                    # swelling portion merely labelled as low RPM.
                    preview=[sample(0,start+i/128)/2+sample(1,start+i/128)/2 for i in range(source_cycles*128)]
                    levels=[math.sqrt(sum(v*v for v in preview[i:i+128])/128) for i in range(0,len(preview),128)]
                    mean=sum(levels)/len(levels)
                    variation=math.sqrt(sum((v-mean)**2 for v in levels)/len(levels))/max(1e-9,mean)
                    cost += variation if refined_idle else .5*variation
                candidates.append((cost,start,begin,end,load,mean))
            primary=candidates
            if refined_loaded:
                reference=entries[5]['source_spans'][0]
                anchor=(reference['start_seconds']+reference['end_seconds'])/2
                region=next(region for region in rising_regions if region[0]-.05<=anchor<=region[1]+.05)
                primary=[c for c in candidates if c[2]/RATE>=region[0]-.05 and c[3]/RATE<=region[1]+.05]
                assert primary, 'accepted acceleration must cover upper nodes'
            selected=[min(primary)]
            if refined_loaded:
                first=selected[0]
                alternatives=[c for c in candidates if abs(c[1]-first[1])>=source_cycles]
                assert alternatives, 'two distinct loaded spans required'
                selected.append(min(alternatives,key=lambda c:c[0]+abs(math.log(c[5]/first[5]))))
            channels=[]
            for channel in range(2):
                spans=[[sample(channel,item[1]+i/POINTS) for i in range((source_cycles+OVERLAP)*POINTS)] for item in selected]
                if refined_loaded:
                    result=[]
                    for part,span in enumerate(spans):
                        previous=spans[(part-1)%2]
                        piece=span[:source_cycles*POINTS]
                        width=OVERLAP*POINTS
                        piece[:width]=joined(previous[source_cycles*POINTS:(source_cycles+OVERLAP)*POINTS],piece[:width])
                        result.extend(piece)
                else:
                    values=spans[0]
                    result=values[:source_cycles*POINTS]
                    width=OVERLAP*POINTS
                    if refined_idle:
                        result[:width]=joined(values[source_cycles*POINTS:(source_cycles+OVERLAP)*POINTS],result[:width])
                    else:
                        # Keep these H1 segments byte-for-byte reproducible.
                        for i in range(width):
                            mix=.5-.5*math.cos(math.pi*i/width)
                            result[i]=values[CYCLES*POINTS+i]*(1-mix)+values[i]*mix
                    if refined_idle:
                        result=result*2
                # Band-limit for the highest RPM where this node participates.
                maximum = RPMS[min(node+1,len(RPMS)-1)]
                limit = 21000/(maximum/60)*CYCLES
                spectrum = fft(result)
                for k in range(len(spectrum)):
                    frequency = min(k,len(spectrum)-k)
                    gain = max(0,min(1,(limit-frequency)/(limit*.08)))
                    spectrum[k] *= gain
                channels.append([v.real for v in fft(spectrum,inverse=True)])
            maximum = max(abs(v) for channel in channels for v in channel)
            assert maximum < 1, 'source loop needs explicit fixed headroom'
            loop = bytearray()
            for i in range(CYCLES*POINTS):
                for channel in range(2):
                    loop += struct.pack('<h',round(channels[channel][i]*32767))
            packed += loop
            # Coherence at the fundamental, before engine-wide interpolation.
            all_loops.append(channels)
            combined = [(a+b)/2 for a,b in zip(*channels)]
            spectrum = fft(combined)
            first = spectrum[CYCLES]
            adjacent = sum(abs(spectrum[k])**2 for k in range(CYCLES-3,CYCLES+4) if k != CYCLES)
            entries.append(dict(rpm=rpm,load_proxy=int(loaded),
                                source_spans=[dict(start_seconds=item[2]/RATE,end_seconds=item[3]/RATE,mean_load_proxy=item[4]) for item in selected],
                                recorded_cycles_per_span=source_cycles,
                                refined_idle=refined_idle,refined_loaded=refined_loaded,
                                bytes=len(loop),rms=math.sqrt(sum(v*v for v in combined)/len(combined)),
                                fundamental_sideband_ratio=adjacent/(abs(first)**2+1e-20)))
    output.mkdir(parents=True,exist_ok=True)
    (output/'Compact.pcm').write_bytes(packed)
    covariance=[]
    for a in all_loops:
        for b in all_loops:
            covariance.append(sum(x*y for ac,bc in zip(a,b) for x,y in zip(ac,bc))/(2*CYCLES*POINTS))
    # Numeric energy calibration only. The bank remains recorded PCM.
    data='// Generated by PrepareCompact.py: stereo loop covariance for blend energy.\npublic class BlendEnergy {\n    let covariance:float64[] = [\n'
    for i in range(12):
        data+='        '+', '.join(format(v,'.12g') for v in covariance[i*12:(i+1)*12])+',\n'
    data+='    ]\n}\n'
    (output.parent/'BlendEnergy.sx').write_text(data)
    report = dict(source=original.name,source_sha256=analysis['source_sha256'],
                  decoded_pcm_sha256=analysis['decoded_pcm_sha256'],
                  pcm_sha256=hashlib.sha256(packed).hexdigest(),bytes=len(packed),
                  rpms=RPMS,cycles_per_loop=CYCLES,points_per_cycle=POINTS,channels=2,
                  overlap_cycles=OVERLAP,rpm_calibrated=False,load_measured=False,
                  phase_valid_interval_seconds=[analysis_begin/RATE,analysis_end/RATE],
                  blend_energy_sha256=hashlib.sha256(data.encode()).hexdigest(),
                  method='recorded multi-cycle PCM; refined coast floor and upper rising spans; offline fundamental phase correction; shared crank phase; integer-cycle loop overlap',
                  entries=entries)
    (output/'Compact.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('wav',type=Path); p.add_argument('analysis',type=Path)
    p.add_argument('original',type=Path); p.add_argument('output',type=Path)
    a=p.parse_args(); prepare(a.wav,a.analysis,a.original,a.output)
