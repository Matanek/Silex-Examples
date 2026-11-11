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
    frames = len(mix) // 2
    idle_offset = frames + len(original) // 2
    opening_offset = idle_offset + len(idle) // 2
    opening_join = opening_offset + len(opening) // 2 - JOIN
    packed = mix + original + idle + opening
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
        opening_to_mix_seconds=[OPENING_JOIN / RATE, RISE / RATE],
        opening_correlation=opening_corr, opening_level_difference_db=opening_db,
    )
    (args.output / 'Ktm.json').write_text(json.dumps(metadata, indent=2) + '\n')
    constants = dict(mix_frames=frames, original_begin=frames, idle_begin=idle_offset,
                     idle_end=idle_offset + idle_end - idle_start, join_frames=JOIN,
                     rise_begin=RISE, coast_begin=COAST, hold_begin=hold_start,
                     opening_begin=opening_offset, opening_join=opening_join)
    declarations = ''.join(f'    let {name}:int = {value}\n' for name, value in constants.items())
    (args.output.parent / 'KtmData.sx').write_text(
        '// Generated by PrepareKtm.py from Assets/Ktm.json inputs.\n'
        'public static struct KtmData {\n' + declarations + '}\n'
    )
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
