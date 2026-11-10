# Drive the YZ250 with a small sound bank

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

The **YZ250 · explosions pilotées · H6 · ESPACE = gaz** window uses about
**1.25 MiB** of stereo PCM16. Idle and closed-gas textures come from the nearby
opening of **2018_Yamaha_YZ_250x.mp3**; attacks and isolated G keep the previous
YZ250/FMF reference. It replaces
the previous A/B/C grain bench at this entry. The spectral P1 experiment remains
separate and is no longer the proposed listening candidate. Chevrolet 454,
500 four-stroke and GFX.Audio are unchanged.

## Blip the throttle

- Hold **Space** to start the engine if necessary and open the throttle.
- Release **Space** to return to the throttle slider position, zero by default.
  RPM falls automatically.
- **Accélérateur** starts slider driving mode. Load slows acceleration but
  does not cap full-throttle RPM.
- **Banc à régime fixe** imposes the RPM slider's speed. Space returns to
  throttle mode for an immediate live response test.
- **M** or **Lecture / arrêt** stops or resumes. Repeated Space events after
  stopping do not restart the engine: release and press again.

Losing focus releases Space. The slider's throttle position is retained.
Status displays mode, actual throttle and RPM. Start with short throttle blips,
then hold for several seconds and listen to the release. Compare different
loads and check steady RPM. **Montée longue · ×4** is the initial inertia setting: at default load, full
throttle takes about four seconds to cover 95% of the RPM range.
**Réponse vive · ×1** retains a quick response; ×4 provides a prolonged rise. The slider spans ×1 to
×10. Inertia lengthens acceleration only. Release uses a 0.62 s time constant:
about 1.86 s to cover 95% of the return to base RPM after closing the throttle.
Status shows **retombée / claquements** while this distinct texture is active.
This setting does not simulate a gearbox or add automatic gear changes.

**Return RPM** is **1,800** on the control scale, adjustable from 1,800 to
3,500. It moves the point at which recorded idle returns; it does not transpose
that recording. Values remain indicative, without tachometer calibration.
All eleven exports use the initial setting.

**Explosions pilotées · H6** is the default. G supplies the pressure body during
both acceleration and holds; closing gas selects recorded clacks for subsequent
firings. **Ancienne lecture · H5** compares the old sequence of pitched loops.
Mode changes are smoothed; both modes keep the same driving controls.

Volume does not change engine response.

## Change firing cadence without sweeping the recorded pressure body

H6 separates firing spacing from recorded pressure duration. Each packet lasts
756 frames, about 17 ms at 44.1 kHz. Overlapping Hann windows use G's 32 cycles.
At 7,000 RPM they reconstruct G; elsewhere only packet start times follow RPM.
Acceleration therefore does not transpose the complete sound band or its
mechanical resonances.

Closing gas selects overrun material at packet starts, without adding a breath
loop. Overlap is normalized only when window weights sum to more than one;
a small packet edge is never amplified. A recorded G residual with its mean
cycle removed stays very quiet below 6,000 RPM to avoid digital silence between
widely spaced firings. Its peak is bounded to 0.025 and it vanishes at 6,000.

This experiment addresses the change of character heard while driving H5.
Waveform checks prove G preservation; the character during throttle gestures
still needs live listening judgment.

## Retain the recorded references

The new idle take uses **4.06–4.70 s** of the YZ250X file: the idle return
identified in the first 4.7 seconds. Startup around 1 s and the receding-motor
section are excluded. PCM retains native timing, with a 20 ms loop join
and fixed gain. Three offline-prepared bandwidths remain available for pitch-up
in the H5 comparison. In H6, the take keeps native
tempo, fades out when gas opens, and returns at the end of deceleration within
150 RPM of the return setting.

Overrun uses **3.64–4.00 s**, the last nearby blip's throttle closure. Offline
preparation tracks the second partial to correct internal pitch without
aligning firing shapes to each other. The take retains 32 cycles with their
clacks. Closing loaded throttle triggers this path even when acoustic load
becomes zero; it fades toward idle and when gas reopens. Its level is not
multiplied by throttle opening. Lengthening the RPM fall while muting the
engine at closure would not reproduce audible deceleration.

The H5 comparison reads twelve short loops from the actual PCM of **2023 YZ250 +
FMF Full Exhaust PURE SOUND.mp3**. Each segment stores **32 revolutions** with their firings, noise and mechanical
texture. The floor uses sixteen more even revolutions, repeated twice. The
three upper loaded nodes assemble two sixteen-revolution spans from clear RPM
rises. They are neither reduced to one cycle
nor reconstructed from a few harmonics.

Offline preparation corrects pitch within each excerpt. It tracks fundamental
phase around the estimated pitch path, excludes the interval where that phase
becomes ambiguous, then resamples PCM by engine revolutions. Four extra
revolutions provide the loop join. Filtering limits frequencies that could
alias during transposition to neighboring RPM nodes.

The three low/mid loaded excerpts remain unchanged. Preparation separately
selects a steadier floor and rising upper textures, preferring the same reference
acceleration as the accepted material.

The bank spans six estimated RPMs and two textures: falling and rising RPM.
Neighboring loops blend gradually on a shared engine phase. Their position
stays continuous even at zero gain. This common phase avoids the internal
pitch sweeps that made the earlier mode C unstable.

Between upper nodes, blending compensates energy lost when weakly correlated
loops overlap. `BlendEnergy.sx` contains their offline-measured stereo covariance.
Gain depends on blend weights, never instantaneous audio level: this is not a
compressor. In H5, the low/mid group keeps its H1 blend to preserve the accepted attack.

The original bank stays unchanged. An additional take applies listening test G's
alignment only to the loaded 6,000-RPM recording. Correlation of the first twelve orders determines a
shift of at most a quarter turn per cycle; overlapping two-turn windows apply
that shift to the full stereo PCM. This retains recorded noise and firings.
Alignment acts on firing placement independently of level and the loop join.
The playable blend still requires listening validation.

In the H5 comparison, after 0.35 s of steady running above 6,000 RPM, a gradual transition introduces
G alone. Rises in that mode keep the original takes; other takes are not layered with G
during holds. Random phrase shifts are disabled to preserve the isolated timbre.
The 32 cycles keep their recorded differences, but the loop still repeats:
this prototype does not resolve that point. Above 7,200 RPM, a filtered view of
the same take fades in, fully at 7,500, to prevent aliasing up to 10,500 RPM.
At 7,000 RPM, G retains its original bandwidth.

`PeakBounds.sx` contains a conservative envelope of original mix peaks.
G uses the maximum peak across its two bandwidths. Both paths are bounded
separately, as are idle and overrun, before their convex transitions. Gain respects a
0.98 ceiling at every reading phase, including residual
weights during transitions. Protection uses data peaks and blend weights,
not instantaneous signal level: peaks are not flattened by a clipper.

A dedicated worker feeds audio independently of GUI rendering. The small 2,048-frame queue,
about 46 ms, stays unchanged to retain command responsiveness. Shared commands
and render blocks are protected by `mutex`; device backpressure waits happen
outside that critical section. Closing the window requests worker shutdown
and joins it before releasing resources.

The **Réserve audio** counter reports observations of an empty input queue.
The mixer may still hold prefetched audio: this counter alone does not prove
an audible gap. The device-output test below checks actual emitted PCM.
RPM and load control run on the audio clock. Throttle response is simplified,
without identified torque or inertia. High load lengthens acceleration without
lowering the full-throttle target. Texture follows throttle opening and its
evolution. Sound stays stereo, without automatic normalization or compression.

## Size and limits

`Assets/Compact.pcm` contains twelve 64 KiB segments; `Assets/Registered.pcm`
contains G alone and its filtered view, two 64 KiB segments. `Assets/LowSpeed.pcm`
adds **393,652 bytes** of idle and overrun. The total is **1,311,156 bytes**.
These are the only embedded audio data. Loading decodes them once to float32:
about 2.50 MiB in memory. Earlier `Reference.pcm` and `Grains.bin` assets remain
historical preparation data; H6 neither embeds nor reads them.

The FMF reference spans acoustically estimated **3,660–10,500 RPM**. The demo
accepts **1,800–10,500** as an indicative control scale. The YZ250X idle is an
actual recording without tachometer measurement: preserving native tempo takes
precedence over a pitch inferred from the displayed number. Load textures remain
rising/falling proxies without measured torque. These two short recordings do
not cover every situation; repetition and timbre differences need listening
judgment. The 2018 YZ250X and 2023 YZ250/FMF have different recordings and
exhausts: their join remains a prototype limitation. Listening approval is
required before generalization.

`Assets/Compact.json` records original/PCM hashes, selected windows, the usable
phase interval, levels and bank size. Preparation only reads the archives.

## Verify and export

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --debug -o Build/YZ250-H6
Build/YZ250-H6 --check
Build/YZ250-H6 --render Build/YZ250-H6
python3 Silex-Examples/Sources/YZ250/VerifyCompact.py Build/YZ250-H6
```

The eleven stereo PCM16 WAVs use a common 0.7 gain:

| Suffix | Content |
| --- | --- |
| `Fixed-4500`, `Fixed-7000`, `Fixed-9500` | 8 s at steady RPM, load texture 0.7 |
| `Load-Low`, `Load-High` | 8 s at 7,000 RPM, load 0 then 1 |
| `Throttle` | 12 s: two blips, full-throttle rise and hold, release, then partial throttle |
| `Idle` | 8 s at the 1,800 RPM base setting, zero load |
| `Micro` | 4 s with an 80 ms throttle opening |
| `Progressive` | 12 s: progressively open throttle over 4 s, hold, then release |
| `Long` | 20 s: full throttle at inertia ×4, hold, then release |
| `Nearby` | 10 s at inertia ×4: idle, short blip, return, rise, then overrun |

The first nine scenarios use inertia ×1; `Long` and `Nearby` use
the ×4 setting proposed by default in the interface.

Every export includes an RPM, phase, acoustic-load, throttle and overrun-weight
(`coast`) CSV. UI holds
continue indefinitely.

Judge timbre one state at a time: start with `Idle`, then throttle closure
between 7.15 and 8.00 s in `Throttle`. Use `Nearby` afterward to judge joins;
it is not a comparison of isolated timbres.

Checks cover 27 RPM/load points, cadence, finite unclipped output, load slowing
the rise without an artificial cap, hold/release, block independence, stopping
and invalid input. The H5 comparison also measures rendered energy at upper nodes and their
midpoints: H1's roughly 3 dB dip fails this regression. The low/mid group must
retain its existing blend. Checks include the 7,980 RPM/full-load mix that
exceeded the audio range, then 6,000 blocks of RPM/load/inertia changes under
a strict 0.98 ceiling. They also follow keyboard event → throttle: Space press,
repeat, release, loss of focus, M stop and switching from the bench. The UI
runtime checks buttons and three layout widths without opening an audio device.

`VerifyCompact.py` measures pitch and level variation in the WAVs, full RPM and
release. It protects the three accepted H1 excerpts by hash and checks the
floor's evenness, progressive throttle, micro-blip, bank size and hashes,
including peak envelopes and alignment. It checks improved pressure-shape
coherence in listening test G's recording. At 7,000 RPM it compares the actual
rendered waveform to isolated G at three loads, protecting its timbre. Rendered
idle is also compared to native PCM. `--coast-check` verifies that closing gas
retains rotation and audible clacks, returns to idle, and responds to reopening.
It also checks buffer-splitting independence throughout overrun. Results are written to
`*-Verification.json`. `--join-check` also compares rendered sound to G just
46 ms after a rise to 7,000 RPM. It distinguishes immediate timbre preservation
from a delayed voice change at the hold, and reports H5 correlation as well.
These measurements do not replace listening validation
of the sound's character. `--check` also reproduces the old GUI-fed queue's
starvation with an offline mixer: a 120 ms stall exceeds its 46 ms reserve.

To verify actual audio output with the GUI, without screenshots:

```sh
Build/YZ250-H6 --live-check Build/YZ250-H6-Live
python3 Silex-Examples/Sources/YZ250/VerifyLive.py Build/YZ250-H6-Live
```

This automatic test lasts eight seconds and deliberately blocks the GUI thread
six times for 120 ms. It records mixer output in `*.f32le`, with its format in
`*.json`. It requires zero capture loss and reports empty-queue observations.
`VerifyLive.py` also checks captured PCM: no 5 ms silent gaps or 10 ms level
collapse outside startup/shutdown. It writes `*-Verification.json`.
This test requires an audio device and exercises the worker, commands and
termination; `--check` remains usable without an audio device.

To reproduce the bank from the original stereo 44.1 kHz PCM16 decode without
gain:

```sh
python3 Silex-Examples/Sources/YZ250/PrepareCompact.py \
  Build/YZ250-Source.wav \
  Silex-Examples/Sources/YZ250/Assets/Analysis.json \
  '.archives/EngineSounds/2023 YZ250 + FMF Full Exhaust PURE SOUND.mp3' \
  Silex-Examples/Sources/YZ250/Assets
```

The tool writes `Compact.pcm` and `Compact.json` inside the output directory,
and `BlendEnergy.sx` in its parent. For a verification rebuild, use e.g.
`Build/YZ250-H6-Rebuild/Assets`.

After preparing a new bank, regenerate its peak envelope and aligned cycles:

```sh
python3 Silex-Examples/Sources/YZ250/PrepareBounds.py \
  Silex-Examples/Sources/YZ250/Assets/Compact.pcm \
  Silex-Examples/Sources/YZ250
python3 Silex-Examples/Sources/YZ250/PrepareRegistered.py \
  Silex-Examples/Sources/YZ250/Assets/Compact.pcm \
  Silex-Examples/Sources/YZ250
```

`PeakBounds.json` links parameters to PCM by hash. Peak data adds about 17 KiB
of numbers to the program. `Assets/Registered.json` records both bank hashes,
parameters and per-cycle shifts; `RegisteredData.sx` contains aligned PCM
power and peak.

After decoding the new reference to stereo 44.1 kHz PCM16 WAV:

```sh
python3 Silex-Examples/Sources/YZ250/PrepareLowSpeed.py \
  Build/YZ250X-Source.wav \
  .archives/EngineSounds/2018_Yamaha_YZ_250x.mp3 \
  Silex-Examples/Sources/YZ250
```

`Assets/LowSpeed.json` records hashes, nearby windows, levels and pitch path;
`LowSpeedData.sx` contains reading and peak bounds.
Python uses only its standard library and is not needed to play the compiled
demo. Earlier `Prepare.py` prepares historical grain-bench assets only; it does
not rebuild the compact bank.
