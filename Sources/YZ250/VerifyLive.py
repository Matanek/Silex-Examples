"""Check actual device output captured during simulated GUI stalls."""
import argparse
import array
import json
import math
from pathlib import Path
import sys


def verify(prefix):
    meta=json.loads(Path(str(prefix)+'.json').read_text())
    samples=array.array('f',Path(str(prefix)+'.f32le').read_bytes())
    if sys.byteorder!='little': samples.byteswap()
    rate,channels=meta['sample_rate'],meta['channels']
    assert len(samples)==meta['frames']*channels
    # Empty input queues are a scheduling diagnostic, not proof of output silence.
    assert meta['dropped_frames']==0 and meta['stalls']>=5
    assert all(math.isfinite(v) and abs(v)<=1 for v in samples)
    # Exclude device startup and the intentional final stop, not GUI stalls.
    end=min(meta['frames']-rate//2,7*rate)
    window=rate//100
    levels=[]; longest=run=0
    for frame in range(rate,end):
        if all(abs(samples[frame*channels+c])<1e-6 for c in range(channels)):
            run+=1; longest=max(longest,run)
        else: run=0
    for frame in range(rate,end-window,window):
        block=samples[frame*channels:(frame+window)*channels]
        levels.append(math.sqrt(sum(v*v for v in block)/len(block)))
    assert longest<rate*.005,('device produced a silence gap',longest/rate)
    assert min(levels)>.001,('10 ms device-output dropout',min(levels))
    report=dict(meta,minimum_10ms_rms=min(levels),longest_near_silent_seconds=longest/rate)
    Path(str(prefix)+'-Verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('prefix',type=Path)
    verify(p.parse_args().prefix)
