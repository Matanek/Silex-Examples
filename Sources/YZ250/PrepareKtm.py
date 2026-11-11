"""Package the E/G comparison, KTM idle and recorded throttle opening."""
import argparse
import array
import hashlib
import json
import math
from pathlib import Path
import sys
import wave

RATE = 44100
JOIN = 441
# The first opening reaches the cadence of H's rise around 14.8 s. These
# two frames match the stereo waveform over the 10 ms overlap at native speed.
OPENING_START = round(12.92 * RATE)
OPENING_JOIN = 652729
RISE = 10429
COAST = round((18.692267573696146 - 17.85) * RATE) + 20944


def read(path):
    with wave.open(str(path), 'rb') as source:
        if (source.getframerate(), source.getnchannels(), source.getsampwidth()) != (RATE, 2, 2):
            raise ValueError(f'{path}: expected 44.1 kHz stereo PCM16')
        samples = array.array('h', source.readframes(source.getnframes()))
    if sys.byteorder != 'little':
        samples.byteswap()
    return samples


def join_metrics(a, b):
    aa = sum(x * x for x in a)
    bb = sum(y * y for y in b)
    corr = sum(x * y for x, y in zip(a, b)) / math.sqrt(aa * bb)
    return corr, 10 * math.log10(bb / aa)


def best_join(samples, outgoing, first, last):
    a = samples[2 * outgoing:2 * (outgoing + JOIN)]
    best = None
    for incoming in range(first, last):
        b = samples[2 * incoming:2 * (incoming + JOIN)]
        corr, difference = join_metrics(a, b)
        candidate = (corr - .06 * abs(difference), incoming, corr, difference)
        if best is None or candidate > best:
            best = candidate
    return best[1:]


def shorten_opening(samples, seconds):
    """Skip recorded time at correlated stereo overlaps; play all spans at 1×."""
    hop = round(.043 * RATE)
    overlap = round(.017 * RATE)
    search = round(.032 * RATE)
    frames = len(samples) // 2
    tail = round(.055 * RATE) + JOIN
    steps = round((seconds * RATE - tail + JOIN) / hop)
    last_target = frames - tail
    result = array.array('h')
    joins = []
    previous = 0
    for step in range(1, steps + 1):
        target = round(last_target * step / steps)
        outgoing = previous + hop
        # Compare on a sparse stereo window, then render at full resolution.
        a = samples[2 * outgoing:2 * (outgoing + overlap):8]
        a_right = samples[2 * outgoing + 1:2 * (outgoing + overlap):8]
        first = max(outgoing, target - search)
        last = min(target + search, frames - hop - overlap)
        best = None
        for incoming in range(first, last + 1, 4):
            b = samples[2 * incoming:2 * (incoming + overlap):8]
            b_right = samples[2 * incoming + 1:2 * (incoming + overlap):8]
            corr, db = join_metrics(a + a_right, b + b_right)
            candidate = (corr - .23 * abs(db) - .16 * abs(incoming - target) / search, incoming)
            if best is None or candidate > best:
                best = candidate
        incoming = best[1]
        if step == 1:
            result.extend(samples[:2 * hop])
        else:
            result.extend(samples[2 * (previous + overlap):2 * outgoing])
        a = samples[2 * outgoing:2 * (outgoing + overlap)]
        b = samples[2 * incoming:2 * (incoming + overlap)]
        aa = sum(v * v for v in a)
        bb = sum(v * v for v in b)
        ab = sum(x * y for x, y in zip(a, b))
        for i in range(overlap):
            mix = .5 - .5 * math.cos(math.pi * i / (overlap - 1))
            keep = 1 - mix
            # A plain crossfade can lose 3 dB between poorly correlated spans.
            # Match the expected overlap power with a smooth, bounded gain.
            power = keep * keep * aa + mix * mix * bb + 2 * keep * mix * ab
            gain = min(1.45, math.sqrt((keep * aa + mix * bb) / power))
            for channel in (0, 1):
                index = 2 * i + channel
                result.append(round(gain * (keep * a[index] + mix * b[index])))
        joins.append([outgoing, incoming])
        previous = incoming
    result.extend(samples[2 * (previous + overlap):])
    assert result[:2 * hop] == samples[:2 * hop]
    assert result[-2 * JOIN:] == samples[-2 * JOIN:]
    return result, joins


def partial_hold(samples, earliest, latest):
    best = None
    for outgoing in range(round(earliest * RATE), round(latest * RATE), round(.003 * RATE)):
        a = samples[2 * outgoing:2 * (outgoing + JOIN)]
        for duration in range(round(.11 * RATE), round(.18 * RATE), 4):
            incoming = outgoing - duration
            b = samples[2 * incoming:2 * (incoming + JOIN)]
            corr, db = join_metrics(a[::4] + a[1::4], b[::4] + b[1::4])
            candidate = (corr - .20 * abs(db), incoming, outgoing)
            if best is None or candidate > best:
                best = candidate
    _, incoming, outgoing = best
    corr, db = join_metrics(samples[2 * outgoing:2 * (outgoing + JOIN)],
                            samples[2 * incoming:2 * (incoming + JOIN)])
    return incoming, outgoing, corr, db


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comparison', type=Path, help='folder with A-Source.wav, H-Mix-E-G.wav and Decoded.wav')
    parser.add_argument('output', type=Path, help='destination Assets folder')
    args = parser.parse_args()
    names = ['H-Mix-E-G.wav', 'A-Source.wav', 'Decoded.wav']
    mix, original, decoded = (read(args.comparison / name) for name in names)
    assert len(mix) == 2 * 95914 and len(original) == 2 * 74970
    start = round(17.85 * RATE) * 2
    trimmed = original[2 * JOIN:-2 * JOIN]
    captured = decoded[start + 2 * JOIN:start + len(original) - 2 * JOIN]
    gain = sum(x * y for x, y in zip(trimmed, captured)) / sum(y * y for y in captured)
    assert 0 < gain <= 1

    hold_start, hold_corr, hold_db = best_join(mix, COAST, round(1.09 * RATE), round(1.16 * RATE))
    idle_end = round(7.3 * RATE)
    idle_start, idle_corr, idle_db = best_join(decoded, idle_end, round(6.3 * RATE), round(6.5 * RATE))
    # Keep incoming and outgoing windows in the PCM so the live cursor can
    # read the overlap from both sides at native speed.
    idle = array.array('h', (round(v * gain) for v in decoded[2 * idle_start:2 * (idle_end + JOIN)]))
    opening = array.array('h', (
        round(v * gain) for v in decoded[2 * OPENING_START:2 * (OPENING_JOIN + JOIN)]
    ))
    opening_corr, opening_db = join_metrics(opening[-2 * JOIN:], mix[2 * RISE:2 * (RISE + JOIN)])
    assert opening_corr > .5 and abs(opening_db) < .5
    progressive, progressive_joins = shorten_opening(opening, .98)
    quick, quick_joins = shorten_opening(opening, .42)
    low_start, low_end, low_corr, low_db = partial_hold(progressive, .37, .43)
    mid_start, mid_end, mid_corr, mid_db = partial_hold(progressive, .67, .73)
    frames = len(mix) // 2
    idle_offset = frames + len(original) // 2
    opening_offset = idle_offset + len(idle) // 2
    opening_join = opening_offset + len(progressive) // 2 - JOIN
    quick_offset = opening_join + JOIN
    quick_join = quick_offset + len(quick) // 2 - JOIN
    packed = mix + original + idle + progressive + quick
    assert max(map(abs, packed)) < 32768
    if sys.byteorder != 'little':
        packed.byteswap()
    data = packed.tobytes()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'Ktm.pcm').write_bytes(data)
    metadata = dict(
        reference='2 Stroke Sound - KTM 250 SX.mp3',
        input_sha256={name: hashlib.sha256((args.comparison / name).read_bytes()).hexdigest() for name in names},
        pcm_sha256=hashlib.sha256(data).hexdigest(),
        sample_rate=RATE, mix_frames=frames, original_frames=len(original) // 2,
        ride_frames=[RISE, COAST], crossfade_frames=JOIN,
        hold_begin=hold_start, hold_correlation=hold_corr, hold_level_difference_db=hold_db,
        idle_frames=[idle_offset, idle_offset + idle_end - idle_start],
        idle_source_seconds=[idle_start / RATE, (idle_end + JOIN) / RATE],
        idle_correlation=idle_corr, idle_level_difference_db=idle_db,
        opening_frames=[opening_offset, opening_join],
        opening_source_seconds=[OPENING_START / RATE, (OPENING_JOIN + JOIN) / RATE],
        progressive_opening_seconds=(opening_join - opening_offset) / RATE,
        quick_frames=[quick_offset, quick_join],
        quick_opening_seconds=(quick_join - quick_offset) / RATE,
        opening_splices_from_start_frames=dict(progressive=progressive_joins, quick=quick_joins),
        partial_hold=[
            dict(frames=[opening_offset + low_start, opening_offset + low_end],
                 correlation=low_corr, level_difference_db=low_db),
            dict(frames=[opening_offset + mid_start, opening_offset + mid_end],
                 correlation=mid_corr, level_difference_db=mid_db),
        ],
        opening_to_mix_seconds=[OPENING_JOIN / RATE, RISE / RATE],
        opening_correlation=opening_corr, opening_level_difference_db=opening_db,
    )
    (args.output / 'Ktm.json').write_text(json.dumps(metadata, indent=2) + '\n')
    constants = dict(mix_frames=frames, original_begin=frames, idle_begin=idle_offset,
                     idle_end=idle_offset + idle_end - idle_start, join_frames=JOIN,
                     rise_begin=RISE, coast_begin=COAST, hold_begin=hold_start,
                     opening_begin=opening_offset, opening_join=opening_join,
                     quick_begin=quick_offset, quick_join=quick_join,
                     low_begin=opening_offset + low_start, low_end=opening_offset + low_end,
                     mid_begin=opening_offset + mid_start, mid_end=opening_offset + mid_end)
    declarations = ''.join(f'    let {name}:int = {value}\n' for name, value in constants.items())
    (args.output.parent / 'KtmData.sx').write_text(
        '// Generated by PrepareKtm.py from Assets/Ktm.json inputs.\n'
        'public static struct KtmData {\n' + declarations + '}\n'
    )
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
