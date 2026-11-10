"""Extract nearby idle and closed-throttle material from the supplied YZ250X.

The user identified startup at 1 s, idle at 1..2 s, then two blips and idle
in the final second of the 4.7 s preview. No receding-motor material is used.
Idle keeps native timing with bandwidths prepared for pitch-up; overrun uses engine order
so its recorded pitch fall is not compounded with the runtime RPM fall.
RPM labels are listening controls, not a tachometer calibration.
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
sys.dont_write_bytecode = True
from PrepareCompact import fft, smooth

RATE=44100


def lowpass(values, cutoff):
    # Circular, zero-phase FIR preparation. Runtime only interpolates two
    # already-filtered views when pitching idle up; no audio-thread FIR work.
    radius=64;kernel=[];frequency=cutoff/RATE
    for i in range(-radius,radius+1):
        value=2*frequency if i==0 else math.sin(2*math.pi*frequency*i)/(math.pi*i)
        kernel.append(value*(.54+.46*math.cos(math.pi*i/radius)))
    total=sum(kernel);kernel=[v/total for v in kernel]
    padded=values[-radius:]+values+values[:radius]
    return [sum(padded[i+j]*weight for j,weight in enumerate(kernel)) for i in range(len(values))]


def prepare(wav, original, output):
    with wave.open(str(wav),'rb') as w:
        assert (w.getframerate(),w.getnchannels(),w.getsampwidth())==(RATE,2,2)
        raw=w.readframes(w.getnframes())
    words=array.array('h',raw)
    if sys.byteorder!='little':words.byteswap()
    pcm=[[words[2*i+c]/32768 for i in range(len(words)//2)] for c in range(2)]
    mono=[(a+b)/2 for a,b in zip(*pcm)]
    # Preserve recorded idle timing; crossfade its seam before preparing views.
    idle_begin,idle_end=int(4.06*RATE),int(4.68*RATE)
    width=round(.02*RATE)
    idle=[channel[idle_begin:idle_end] for channel in pcm]
    for c in range(2):
        for i in range(width):
            t=.5-.5*math.cos(math.pi*i/width)
            idle[c][i]=pcm[c][idle_end+i]*(1-t)+idle[c][i]*t
    # Track the strong second partial across the last stationary blip's fall.
    begin,end=int(3.50*RATE),int(4.68*RATE)
    centres=list(range(begin,end,441))
    frequencies=[];previous=100.0
    for centre in centres:
        n=8192;left=centre-n//2
        spectrum=fft([mono[left+i]*(.5-.5*math.cos(2*math.pi*i/n)) for i in range(n)])
        power=[abs(v)**2 for v in spectrum[:n//2]]
        def score(f):
            value=0.0
            for h in [1,2,3,4,5,6]:
                k=round(f*h*n/RATE)
                peak=max(power[k-1:k+2]);floor=sum(power[max(1,k-8):k+9])/17
                value+=math.log1p(peak/(floor+1e-15))/h**.7
            return value-.8*abs(math.log(f/previous))
        previous=max((55+i*.5 for i in range(161)),key=score)
        frequencies.append(previous)
    path=smooth(frequencies,.35)
    phase=[];p=0.0
    for i in range(begin,end):
        position=(i-begin)/441;index=min(len(path)-2,int(position));t=position-index
        p+=(path[index]*(1-t)+path[index+1]*t)/RATE;phase.append(p)
    fundamental=smooth([mono[begin+i]*cmath.exp(-4j*math.pi*p) for i,p in enumerate(phase)],1-math.exp(-2*math.pi*14/RATE))
    unwrapped=0.0;previous=cmath.phase(fundamental[0]);corrected=[]
    for p,v in zip(phase,fundamental):
        angle=cmath.phase(v);unwrapped+=(angle-previous+math.pi)%(2*math.pi)-math.pi
        corrected.append(p+unwrapped/(4*math.pi));previous=angle
    breaks=[0]+[i for i in range(1,len(corrected)) if corrected[i]<=corrected[i-1]]+[len(corrected)-1]
    left,right=max(zip(breaks,breaks[1:]),key=lambda pair:pair[1]-pair[0])
    left+=RATE//25;right-=RATE//25
    start=max(corrected[left],corrected[int(.14*RATE)])
    assert start+33<corrected[right],('stationary overrun has fewer than 33 usable turns',left,right)
    coast=[]
    for channel in pcm:
        values=[]
        for i in range(32*512):
            turn=start+i/512
            j=bisect.bisect_right(corrected,turn,left,right)-1
            t=(turn-corrected[j])/(corrected[j+1]-corrected[j])
            values.append(channel[begin+j]*(1-t)+channel[begin+j+1]*t)
        # A one-turn seam; retain all recorded firing differences elsewhere.
        for i in range(512):
            t=.5-.5*math.cos(math.pi*i/512)
            turn=start+32+i/512
            j=bisect.bisect_right(corrected,turn,left,right)-1
            f=(turn-corrected[j])/(corrected[j+1]-corrected[j])
            tail=channel[begin+j]*(1-f)+channel[begin+j+1]*f
            values[i]=tail*(1-t)+values[i]*t
        spectrum=fft(values);limit=21000/(10500/60)*32
        for k in range(len(spectrum)):
            spectrum[k]*=max(0,min(1,(limit-min(k,len(spectrum)-k))/(limit*.08)))
        coast.append([v.real for v in fft(spectrum,inverse=True)])
    views=[[lowpass(channel,cutoff) for channel in idle] for cutoff in [20000,9500,6500]]
    packed=array.array('h');levels=[]
    idle_gain=min(.075/math.sqrt(sum(v*v for channel in views[0] for v in channel)/(len(idle[0])*2)),.90/max(abs(v) for view in views for channel in view for v in channel))
    for index,(channels,target) in enumerate([(views[0],.075),(views[1],.075),(views[2],.075),(coast,.16)]):
        power=sum(v*v for channel in channels for v in channel)/(len(channels[0])*2)
        gain=min(target/math.sqrt(power),.90/max(abs(v) for channel in channels for v in channel))
        if index<3:gain=idle_gain
        interleaved=[round(channels[c][i]*gain*32768) for i in range(len(channels[0])) for c in range(2)]
        packed.extend(interleaved);levels.append(dict(rms=math.sqrt(sum(v*v for v in interleaved)/len(interleaved))/32768,peak=max(map(abs,interleaved))/32768))
    if sys.byteorder!='little':packed.byteswap()
    encoded=packed.tobytes()
    source='// Generated by PrepareLowSpeed.py from the stationary YZ250X reference.\npublic class LowSpeedData {\n'
    source+=f'    let idle_frames:int = {len(idle[0])}\n'
    source+='    let idle_peak:float64 = '+format(max(level['peak'] for level in levels[:3])+1e-9,'.14g')+'\n'
    source+='    let coast_peak:float64 = '+format(levels[3]['peak']+1e-9,'.14g')+'\n}\n'
    output.mkdir(parents=True,exist_ok=True);(output/'Assets').mkdir(exist_ok=True)
    (output/'Assets/LowSpeed.pcm').write_bytes(encoded);(output/'LowSpeedData.sx').write_text(source)
    report=dict(source=original.name,source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),decoded_pcm_sha256=hashlib.sha256(raw).hexdigest(),
                pcm_sha256=hashlib.sha256(encoded).hexdigest(),source_data_sha256=hashlib.sha256(source.encode()).hexdigest(),audio_bytes=len(encoded),
                idle_source_seconds=[4.06,4.70],idle_frames=len(idle[0]),idle_native_timing=True,idle_nominal_control_rpm=1800,rpm_calibrated=False,
                idle_views=3,idle_view_cutoffs_hz=[20000,9500,6500],
                coast_source_seconds=[(begin+bisect.bisect_left(corrected,start))/RATE,(begin+bisect.bisect_left(corrected,start+33))/RATE],
                coast_cycles=32,points_per_cycle=512,stationary_only=True,levels=levels,
                pitch_path=[dict(seconds=t/RATE,pressure_frequency=f) for t,f in zip(centres,path)])
    (output/'Assets/LowSpeed.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='pitch_path'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('wav',type=Path);p.add_argument('original',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();prepare(a.wav,a.original,a.output)
