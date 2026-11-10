# Listen to the fully procedural YZ250 prototype

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250Procedural/Main.sx
```

The window title is **YZ250 · procédural intégral · P1**. It is separate from
the earlier sample-grain A/B/C bench and the vehicle workshop. It starts silent.
The Chevrolet 454, 500 four-stroke and GFX.Audio package are unchanged.

## Validate steady RPM before sweeps

1. Click **4 500 tr/min**, **7 000 tr/min**, then **9 500 tr/min**. Each hold
   continues until another command. Listen to cadence, body, level and possible
   oscillations for at least ten seconds.
2. At constant RPM, compare both ends of **Charge acoustique**. Energy and
   texture change while the firing cadence stays identical.
3. Try **Montée lente · 5 s**, then **Montée rapide · 1 s**. Each button starts
   again at 3,660 RPM and automatically reaches 10,500 RPM. That final RPM is
   then held indefinitely.
4. **Arrêt** stops with a short fade. Moving the RPM slider returns to imposed
   RPM mode; **Écouter ce régime** starts the displayed hold.

These are bench sweeps comparing one generator at different speeds. The RPM
slider imposes speed; it is not a throttle. The prototype has no torque,
inertia or transmission model yet. The load control therefore does not slow
the timed sweeps.

## What is synthesized

The acoustic engine produces one firing per revolution for a single-cylinder
two-stroke. A continuous phase on the 44,100 Hz audio clock drives 64 harmonics.
Six filtered noise bands represent the recording's nonperiodic body: combined
flow, exhaust and mechanical texture. Noise is modulated at the firing cadence;
firing strength varies slightly between revolutions without changing their
timing. RPM and gains evolve continuously without bank switching, grain joins
or loops.

The signal is mono, duplicated to both channels. It adds neither spatialization
nor reverberation. Fixed headroom gain is 0.55; no compressor, clipping or
automatic normalization artificially stabilizes the level. Listening volume
is independent.

`Calibration.sx` contains only numeric spectral, filter and envelope parameters.
The program loads no PCM, WAV or MP3 and embeds no recorded cycle. Harmonic
phases come from a minimum-phase construction of the average spectrum, not
from the recording's phases. This is parametric acoustic synthesis without
thermodynamic simulation.

## What the reference recording actually supplies

Calibration uses the supplied archived **2023 YZ250 + FMF Full Exhaust PURE
SOUND.mp3**. It measures 109 windows, each following six estimated cycles.
This order-domain analysis follows acceleration within each window instead of
treating every excerpt as a constant-pitch sound. It measures harmonic and
residual energies, then aggregates them over six RPM nodes and two load textures.
Noise filters are normalized offline using their impulse-response energy.

`Calibration.json` retains hashes of the original, decoded PCM, analyzed pitch
path and generated parameters. The original decode is exclusively an input to
the offline calibration tool.

The source has no tachometer or torque measurement. The **3,660–10,500 RPM**
range is an acoustic estimate inherited from pitch tracking; possible octave
errors remain unresolved. Load mainly interpolates falling- and rising-RPM
textures. The bottom range has limited coverage and idle is not calibrated.
The microphone and FMF exhaust influence the parameters. Measuring them does
not establish faithful reproduction: human listening must validate timbre
before any generalization.

## Export and verify

```sh
silex compile Silex-Examples/Sources/YZ250Procedural/Main.sx --debug -o Build/YZ250-Procedural
Build/YZ250-Procedural --check
Build/YZ250-Procedural --render Build/YZ250-P1
python3 Silex-Examples/Sources/YZ250Procedural/Verify.py Build/YZ250-P1
```

The seven stereo PCM16 WAVs use the same 0.7 listening-volume gain:

| Suffix | Listening case |
| --- | --- |
| `Fixed-4500`, `Fixed-7000`, `Fixed-9500` | 8 s at steady RPM, load 0.7 |
| `Load-Low`, `Load-High` | 8 s at 7,000 RPM, load 0 then 1 |
| `Ramp-Slow`, `Ramp-Fast` | 1 s at the start, a 5 or 1 s rise, then full RPM until 12 s |

A fade closes the files; UI holds have no programmed end. Each WAV has an
accompanying RPM/phase CSV.

`--check` verifies 21 RPM/load points, the firing clock, absence of clipping and
nonfinite output, load independent of cadence, ramp and hold, independence
from rendering block boundaries, reset, stopping and invalid commands. It
also tests buttons through the UI runtime without an audio device, plus three
layout widths.

`Verify.py` analyzes the WAVs themselves: peaks across several harmonics during
holds, 200 ms level variation, order-tracked sweeps and final hold pitch. It
also checks that generator sources have no sample dependency. Measurements
are recorded in `*-Verification.json`. These checks do not decide realism.

To reproduce calibration with the original stereo 44.1 kHz PCM16 decode,
without gain:

```sh
python3 Silex-Examples/Sources/YZ250Procedural/Calibrate.py \
  Build/YZ250-Source.wav \
  Silex-Examples/Sources/YZ250/Assets/Analysis.json \
  '.archives/EngineSounds/2023 YZ250 + FMF Full Exhaust PURE SOUND.mp3' \
  Silex-Examples/Sources/YZ250Procedural
```

The tool checks hashes before analysis and writes exclusively to its output
directory. Archives stay unchanged. Python uses only its standard library and
is not needed to play the compiled prototype.
