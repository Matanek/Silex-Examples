# Drive the YZ250 with a small sound bank

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

The **YZ250 · banque compacte · H3 · ESPACE = gaz** window uses real texture
from the supplied recording, in a **768 KiB** stereo PCM16 bank. It replaces
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
**Réponse vive · ×1** restores H2's rise and micro-blip. The slider spans ×1 to
×10. Inertia lengthens acceleration only; release retains its quick response.
This setting does not simulate a gearbox or add automatic gear changes.

Volume does not change engine response.

## What preserves the reference's character

The program reads twelve short loops from the actual PCM of **2023 YZ250 +
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

H2 retains eight H1 segments unchanged, including the three low/mid loaded
excerpts responsible for the accepted micro-blip. H3’s ×1 mode preserves that
throttle response.
Preparation separately selects a steadier floor and rising upper textures,
preferring the same reference acceleration as the accepted material.

The bank spans six estimated RPMs and two textures: falling and rising RPM.
Neighboring loops blend gradually on a shared engine phase. Their position
stays continuous even at zero gain. This removes repeated excerpt selection
and internal pitch sweeps that made the earlier mode C unstable.

Between upper nodes, blending compensates energy lost when weakly correlated
loops overlap. `BlendEnergy.sx` contains their offline-measured stereo covariance.
Gain depends on blend weights, never instantaneous audio level: this is not a
compressor. The low/mid group keeps its H1 blend to preserve the accepted attack.

H3 retains H2's complete bank and blend behavior. A dedicated worker now
feeds audio independently of GUI rendering. The small 2,048-frame queue,
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

`Assets/Compact.pcm` contains twelve 64 KiB segments, **786,432 bytes total**.
This bank is the only audio data embedded by `Bank.sx`. Loading decodes it once
to float32: about 1.5 MiB in memory. Earlier `Reference.pcm` and `Grains.bin`
assets remain historical preparation data; H3 neither embeds nor reads them.

RPM remains an acoustic estimate of **3,660–10,500**, without a tachometer.
Idle was not recorded. Both load textures are rising/falling proxies, not
measured torque. A thirteen-second recording does not cover every situation;
repetition and timbre differences between loops remain listening questions.
The microphone and FMF exhaust are part of the reference. This hybrid prototype
awaits human listening approval before generalization.

`Assets/Compact.json` records original/PCM hashes, selected windows, the usable
phase interval, levels and bank size. Preparation only reads the archives.

## Verify and export

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --debug -o Build/YZ250-H3
Build/YZ250-H3 --check
Build/YZ250-H3 --render Build/YZ250-H3
python3 Silex-Examples/Sources/YZ250/VerifyCompact.py Build/YZ250-H3
```

The ten stereo PCM16 WAVs use a common 0.7 gain:

| Suffix | Content |
| --- | --- |
| `Fixed-4500`, `Fixed-7000`, `Fixed-9500` | 8 s at steady RPM, load texture 0.7 |
| `Load-Low`, `Load-High` | 8 s at 7,000 RPM, load 0 then 1 |
| `Throttle` | 12 s: two blips, full-throttle rise and hold, release, then partial throttle |
| `Idle` | 8 s at the recorded floor, zero load |
| `Micro` | 4 s with an 80 ms throttle opening |
| `Progressive` | 12 s: progressively open throttle over 4 s, hold, then release |
| `Long` | 20 s: full throttle at inertia ×4, hold, then release |

The first nine scenarios keep inertia ×1 for comparison with H2; `Long` uses
the ×4 setting proposed by default in the interface.

Every export includes an RPM, phase, acoustic-load and throttle CSV. UI holds
continue indefinitely.

Checks cover 21 RPM/load points, cadence, finite unclipped output, load slowing
the rise without an artificial cap, hold/release, block independence, stopping
and invalid input. Checks also measure rendered energy at upper nodes and their
midpoints: H1's roughly 3 dB dip fails this regression. The low/mid group must
retain its existing blend. They also follow keyboard event → throttle: Space press,
repeat, release, loss of focus, M stop and switching from the bench. The UI
runtime checks buttons and three layout widths without opening an audio device.

`VerifyCompact.py` measures pitch and level variation in the WAVs, full RPM and
release. It protects the three accepted H1 excerpts by hash and checks the
floor's evenness, progressive throttle, micro-blip, bank size and hashes. Results are written to
`*-Verification.json`. These measurements do not replace listening validation
of the sound's character. `--check` also reproduces the old GUI-fed queue's
starvation with an offline mixer: a 120 ms stall exceeds its 46 ms reserve.

To verify actual audio output with the GUI, without screenshots:

```sh
Build/YZ250-H3 --live-check Build/YZ250-H3-Live
python3 Silex-Examples/Sources/YZ250/VerifyLive.py Build/YZ250-H3-Live
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
`Build/YZ250-H3-Rebuild/Assets`.

Python uses only its standard library and is not needed to play the compiled
demo. Earlier `Prepare.py` prepares historical grain-bench assets only; it does
not rebuild the compact bank.
