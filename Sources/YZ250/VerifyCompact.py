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
    for name,rpm in [('Fixed-4500',4500),('Fixed-7000',7000),('Fixed-9500',9500),('Load-Low',7000),('Load-High',7000),('Idle',3660)]:
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
    progressive=read(Path(str(prefix)+'-Progressive.wav'))
    assert len(progressive)==12*RATE
    with Path(str(prefix)+'-Progressive.csv').open() as f: progressive_rows=list(csv.DictReader(f))
    rising=[r for r in progressive_rows if 1<int(r['frame'])/RATE<5]
    assert all(float(b['rpm'])>=float(a['rpm']) for a,b in zip(rising,rising[1:]))
    assert float(rising[-1]['rpm'])>9900
    report['Progressive']=dict(rpm_min=float(rising[0]['rpm']),rpm_max=float(rising[-1]['rpm']))
    micro=read(Path(str(prefix)+'-Micro.wav'))
    assert len(micro)==4*RATE
    with Path(str(prefix)+'-Micro.csv').open() as f: micro_rows=list(csv.DictReader(f))
    peak_rpm=max(float(r['rpm']) for r in micro_rows)
    assert 4500<peak_rpm<5500
    report['Micro']=dict(peak_rpm=peak_rpm)
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
    report['Idle']['cycle_rms_variation']=idle_variation
    assert hashlib.sha256((directory/'BlendEnergy.sx').read_bytes()).hexdigest()==metadata['blend_energy_sha256']
    assert 'Reference.pcm' not in (directory/'Bank.sx').read_text()
    assert 'Grains.bin' not in (directory/'Bank.sx').read_text()
    assert report['Load-High']['rms']>report['Load-Low']['rms']*1.2
    Path(str(prefix)+'-Verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    print('H2 audio/bank verification passed; listening approval remains required.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('prefix',type=Path)
    verify(p.parse_args().prefix)
