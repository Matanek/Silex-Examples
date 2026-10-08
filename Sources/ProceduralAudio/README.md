# Make sounds without a sound bank

This demonstration plays eight `GFX.Audio` recipes, from a beep to a changing
engine and a MIDI score. Silex computes every sample. `Score.mid` holds 218
bytes of musical commands; it embeds neither audio nor an instrument bank.

[Version française](README.fr.md).

## Listen and select a recipe

From the `SilexProject/` root, using the Spec’s local toolchain and packages
until they are delivered:

```sh
silex compile Silex-Examples/Sources/ProceduralAudio/Main.sx --release -o .silex/procedural-audio
.silex/procedural-audio --case laser
.silex/procedural-audio --case midi
.silex/procedural-audio
```

Inside the Spec, use its `Worktree/` root instead. The demo requires Silex
0.47.1 or later and the Spec’s local corrections. `--help` lists the names;
without `--case`, recipes play in table order. Audible playback uses the default
output device. Each name and duration is printed.

| Name | Duration | Composition and parameters to explore |
| --- | ---: | --- |
| `beep` | 0.295 s | 660 Hz sine; 5 ms attack, 120 ms release. |
| `impact` | 0.260 s | 65 Hz bass and white noise filtered at 1,200 Hz; seed 42. |
| `laser` | 0.750 s | Frequency from 2,900 to 100 Hz over 500 ms, ADSR envelope. |
| `explosion` | 1.250 s | White noise filtered at 450 Hz and 48 Hz bass; seed 1985. |
| `engine` | 5.100 s | Modulated fundamental and harmonic, pink noise, four smoothed regime changes. |
| `retro` | 0.500 s | 440 Hz square wave, 8-bit bitcrusher, six-frame sample hold. |
| `melody` | 2.500 s | Polyphonic instrument, chord and four notes at 120 BPM, including ending and release. |
| `midi` | 4.600 s | Two tracks, three explicit bindings, tempo change, sustain, pan and echo. |

The first recipes are mono; MIDI is stereo. Levels are preserved without
normalization. Start at a moderate listening volume. `retro` is a short sound
with a retro texture, rather than an emulation of a particular chip.

## Change the sounds

[Recipes.sx](Recipes.sx) assembles sources and processors. Changing a frequency
in hertz, a linear gain or envelope durations changes the render directly.
Every recipe uses 48,000 frames per second: 240 frames equal 5 ms. The bitcrusher
holds each value for six frames, giving an effective rate of 8,000 Hz. Noise
seeds ensure reproducibility.

[Envelope.sx](Envelope.sx) and [Engine.sx](Engine.sx) are application-owned
generators implementing `Synthesis.Generator`. The former triggers release at
an exact frame; the latter splits rendering at regime changes and uses `Control`
to smooth pitch and gain. You can replace these compositions, write your own
generators and processors, or supply instruments to MIDI bindings without
calling a native boundary.

The direct melody places notes every 24,000 frames: its cadence does not depend
on a timer or the application loop. MIDI follows the score’s tempo changes.
Gain and pan controllers ramp over 240 frames to avoid audible jumps; this
setting is optional in `MIDI.Synthesizer`. No random humanization is applied.
These recipes do not promise a realistic orchestra or a VST host.

## Verify without audio output

```sh
.silex/procedural-audio --check
.silex/procedural-audio --check --case engine
```

`--check` opens no output device. For each recipe it verifies duration, finite
values, headroom, beginning and ending, then compares PCM after reset using
480- and 257-frame blocks. It also compares streamed output with the complete
render, even when a 127-frame capacity forces partial writes. Counters must
show every frame consumed and none discarded. The melody’s last half-second
and MIDI’s last second allow releases and echo to finish.

[Playback.sx](Playback.sx) prepares short sounds with `Audio.create` and supplies
longer sounds with `Synthesis.StreamProducer`. This check establishes render
consistency; listening remains necessary to judge timbre and artifacts. It
measures neither allocations nor the time budget of a block.
