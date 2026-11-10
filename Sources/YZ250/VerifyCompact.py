"""Inspect the compact bank and its rendered audio; listening judges timbre."""
import argparse
import array
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import wave
sys.dont_write_bytecode = True
from PrepareCompact import fft
from PrepareRegistered import pressure

RATE=44100


def read(path):
    with wave.open(str(path),'rb') as w:
        assert (w.getframerate(),w.getnchannels(),w.getsampwidth()) == (RATE,2,2)
        samples=array.array('h',w.readframes(w.getnframes()))
    if sys.byteorder != 'little': samples.byteswap()
    stereo=[v/32768 for v in samples]
    assert max(map(abs,stereo)) < .99
    return [(stereo[i]+stereo[i+1])/2 for i in range(0,len(stereo),2)]


def pitch(values,expected):
    n=len(values)
    power=[abs(v)**2 for v in fft([v*(.5-.5*math.cos(2*math.pi*i/n)) for i,v in enumerate(values)])[:n//2]]
    estimates=[]
    for order in range(1,9):
        index=round(expected/60*order*n/RATE)
        k=max(range(max(2,index-2),index+3),key=power.__getitem__)
        a,b,c=[math.log(max(1e-20,power[j])) for j in [k-1,k,k+1]]
        offset=max(-.5,min(.5,.5*(a-c)/(a-2*b+c)))
        estimates.append((power[k],(k+offset)*RATE/n*60/order))
    strongest=sorted(estimates,reverse=True)[:4]
    return sum(w*r for w,r in strongest)/sum(w for w,r in strongest)


def verify(prefix):
    report={}
    for name,rpm in [('Fixed-4500',4500),('Fixed-7000',7000),('Fixed-9500',9500),('Load-Low',7000),('Load-High',7000)]:
        values=read(Path(str(prefix)+'-'+name+'.wav'))
        assert len(values)==8*RATE
        estimates=[pitch(values[i:i+16384],rpm) for i in range(RATE,len(values)-16384,RATE//3)]
        rms=[math.sqrt(sum(v*v for v in values[i:i+8820])/8820) for i in range(RATE,len(values)-8820,8820)]
        error=max(abs(v/rpm-1) for v in estimates)
        variation=statistics.pstdev(rms)/statistics.mean(rms)
        report[name]=dict(spectral_rpm_min=min(estimates),spectral_rpm_max=max(estimates),
                          max_pitch_error_percent=error*100,rms_variation=variation,rms=statistics.mean(rms))
        # Measured waveform stability, separate from the exact crank clock.
        assert error < .02,(name,'unstable pitch',report[name])
        assert variation < .20,(name,'unstable level',report[name])
    values=read(Path(str(prefix)+'-Throttle.wav'))
    assert len(values)==12*RATE
    with Path(str(prefix)+'-Throttle.csv').open() as f: rows=list(csv.DictReader(f))
    hold=[r for r in rows if 5 < int(r['frame'])/RATE < 6.8]
    assert min(float(r['rpm']) for r in hold) > 10490
    release=[r for r in rows if 8.8 < int(r['frame'])/RATE < 9]
    assert max(float(r['rpm']) for r in release) < 3670
    hold_pitch=[pitch(values[i:i+16384],10500) for i in range(5*RATE,6*RATE,RATE//4)]
    assert max(abs(v/10500-1) for v in hold_pitch)<.02
    report['Throttle']=dict(hold_spectral_rpm_min=min(hold_pitch),hold_spectral_rpm_max=max(hold_pitch),
                            release_rpm_max=max(float(r['rpm']) for r in release))
    closed=[r for r in rows if 7.15<int(r['frame'])/RATE<7.85]
    assert min(float(r['coast']) for r in closed)>.98, 'closing gas lost the recorded overrun'
    after_half=min(rows,key=lambda r:abs(int(r['frame'])/RATE-7.5))
    assert 5500<float(after_half['rpm'])<6500, 'RPM fall is not progressive'
    coast_rms=math.sqrt(sum(v*v for v in values[int(7.2*RATE):int(7.9*RATE)])/int(.7*RATE))
    assert coast_rms>.06,('overrun went quiet',coast_rms)
    report['Throttle'].update(coast_rms=coast_rms,rpm_half_second_after_release=float(after_half['rpm']))
    progressive=read(Path(str(prefix)+'-Progressive.wav'))
    assert len(progressive)==12*RATE
    with Path(str(prefix)+'-Progressive.csv').open() as f: progressive_rows=list(csv.DictReader(f))
    rising=[r for r in progressive_rows if 1<int(r['frame'])/RATE<5]
    assert all(float(b['rpm'])>=float(a['rpm']) for a,b in zip(rising,rising[1:]))
    assert (float(rising[-1]['rpm'])-1800)/(10500-1800)>.90
    report['Progressive']=dict(rpm_min=float(rising[0]['rpm']),rpm_max=float(rising[-1]['rpm']))
    micro=read(Path(str(prefix)+'-Micro.wav'))
    assert len(micro)==4*RATE
    with Path(str(prefix)+'-Micro.csv').open() as f: micro_rows=list(csv.DictReader(f))
    peak_rpm=max(float(r['rpm']) for r in micro_rows)
    assert 3300<peak_rpm<4200
    report['Micro']=dict(peak_rpm=peak_rpm)
    long=read(Path(str(prefix)+'-Long.wav'))
    assert len(long)==20*RATE
    with Path(str(prefix)+'-Long.csv').open() as f: long_rows=list(csv.DictReader(f))
    reached=next(int(r['frame'])/RATE-1 for r in long_rows if float(r['rpm'])>=10065)
    assert 3.6<reached<4.2
    report['Long']=dict(seconds_to_95_percent_rpm=reached)
    directory=Path(__file__).parent
    metadata=json.loads((directory/'Assets/Compact.json').read_text())
    pcm=(directory/'Assets/Compact.pcm').read_bytes()
    assert len(pcm)==786432 and hashlib.sha256(pcm).hexdigest()==metadata['pcm_sha256']
    # The user accepted H1's micro-blip: protect its low/mid loaded PCM.
    accepted=b''.join(pcm[n*65536:(n+1)*65536] for n in [1,3,5])
    assert hashlib.sha256(accepted).hexdigest()=='5b76cd3a81651f3ce69e9828c54faa73ccb312cb68af1f4e64cc7533ba722283'
    floor=array.array('h',pcm[:65536])
    levels=[]
    for cycle in range(32):
        values=[(floor[i*2]+floor[i*2+1])/65536 for i in range(cycle*512,(cycle+1)*512)]
        levels.append(math.sqrt(sum(v*v for v in values)/len(values)))
    idle_variation=statistics.pstdev(levels)/statistics.mean(levels)
    assert idle_variation<.09,'recorded floor lost its even cadence'
    assert hashlib.sha256((directory/'BlendEnergy.sx').read_bytes()).hexdigest()==metadata['blend_energy_sha256']
    bounds=json.loads((directory/'PeakBounds.json').read_text())
    assert bounds['pcm_sha256']==metadata['pcm_sha256']
    assert hashlib.sha256((directory/'PeakBounds.sx').read_bytes()).hexdigest()==bounds['source_sha256']
    registered=json.loads((directory/'Assets/Registered.json').read_text())
    aligned=(directory/'Assets/Registered.pcm').read_bytes()
    assert len(aligned)+len(pcm)==917_504
    assert registered['original_sha256']==metadata['pcm_sha256']
    assert hashlib.sha256(aligned).hexdigest()==registered['pcm_sha256']
    assert hashlib.sha256((directory/'RegisteredData.sx').read_bytes()).hexdigest()==registered['source_sha256']
    # G's improvement comes from pressure-shape alignment, not level/EQ.
    # Guard that independently of the exact playback clock and PCM hashes.
    blocks=[]
    for raw,node in [(pcm,5),(aligned,0)]:
        words=array.array('h',raw)
        if sys.byteorder!='little':words.byteswap()
        mono=[(words[(node*16384+i)*2]+words[(node*16384+i)*2+1])/65536 for i in range(16384)]
        blocks.append([pressure(mono[i*512:(i+1)*512]) for i in range(32)])
    template=[sum(block[i] for block in blocks[0])/32 for i in range(512)]
    coherence=[]
    for cycles in blocks:
        coherence.append(statistics.mean(sum(a*b for a,b in zip(cycle,template))/math.sqrt(sum(a*a for a in cycle)*sum(b*b for b in template)) for cycle in cycles))
    assert coherence[1]>coherence[0]+.05,('recorded firing alignment regressed',coherence)
    report['Recorded-Alignment']=dict(original_coherence=coherence[0],registered_coherence=coherence[1],audio_bytes=len(pcm)+len(aligned))
    low_meta=json.loads((directory/'Assets/LowSpeed.json').read_text())
    low_raw=(directory/'Assets/LowSpeed.pcm').read_bytes()
    assert hashlib.sha256(low_raw).hexdigest()==low_meta['pcm_sha256']
    assert hashlib.sha256((directory/'LowSpeedData.sx').read_bytes()).hexdigest()==low_meta['source_data_sha256']
    assert len(low_raw)==low_meta['audio_bytes'] and len(pcm)+len(aligned)+len(low_raw)==1_311_156
    assert low_meta['stationary_only'] and max(low_meta['idle_source_seconds']+low_meta['coast_source_seconds'])<=4.7
    idle_words=array.array('h',low_raw)
    if sys.byteorder!='little':idle_words.byteswap()
    frames=low_meta['idle_frames']
    native=[(idle_words[i*2]+idle_words[i*2+1])/65536 for i in range(frames)]
    actual_idle=read(Path(str(prefix)+'-Idle.wav'))
    assert len(actual_idle)==8*RATE
    expected=[native[(frame+1)%frames] for frame in range(2*RATE,7*RATE)]
    rendered_idle=actual_idle[2*RATE:7*RATE]
    corr=sum(a*b for a,b in zip(expected,rendered_idle))/math.sqrt(sum(a*a for a in expected)*sum(b*b for b in rendered_idle))
    assert corr>.99999,('idle was transposed or replaced by the old synthetic floor',corr)
    report['Idle']=dict(native_reference_correlation=corr,rms=math.sqrt(sum(v*v for v in rendered_idle)/len(rendered_idle)),source_seconds=low_meta['idle_source_seconds'],control_rpm=1800,rpm_calibrated=False)
    nearby=read(Path(str(prefix)+'-Nearby.wav'))
    assert len(nearby)==10*RATE
    with Path(str(prefix)+'-Nearby.csv').open() as f:nearby_rows=list(csv.DictReader(f))
    falling=[r for r in nearby_rows if 6.2<int(r['frame'])/RATE<7.2]
    assert min(float(r['coast']) for r in falling)>.5
    report['Nearby']=dict(seconds=10,coast_min=min(float(r['coast']) for r in falling))
    # A mixture of registered takes passed clock/level tests but lost G's timbre
    # in listening. Protect the actual rendered waveform against that regression.
    words=array.array('h',aligned)
    if sys.byteorder!='little':words.byteswap()
    source=[(words[i*2]+words[i*2+1])/65536 for i in range(16384)]
    reference=[]
    for frame in range(2*RATE,6*RATE):
        position=((frame+1)*7000/2646000*512)%16384
        index=int(position);fraction=position-index
        reference.append(source[index]*(1-fraction)+source[(index+1)%16384]*fraction)
    for name in ['Fixed-7000','Load-Low','Load-High']:
        rendered=read(Path(str(prefix)+'-'+name+'.wav'))[2*RATE:6*RATE]
        corr=sum(a*b for a,b in zip(reference,rendered))/math.sqrt(sum(a*a for a in reference)*sum(b*b for b in rendered))
        assert corr>.99999,(name,'playable hold no longer preserves isolated G',corr)
        report[name]['correlation_to_isolated_g']=corr
    assert 'Reference.pcm' not in (directory/'Bank.sx').read_text()
    assert 'Grains.bin' not in (directory/'Bank.sx').read_text()
    assert report['Load-High']['rms']>report['Load-Low']['rms']*1.2
    Path(str(prefix)+'-Verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    print('H5 audio/bank verification passed; listening approval remains required.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('prefix',type=Path)
    verify(p.parse_args().prefix)
