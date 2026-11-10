# Qualify the YZ250 by listening

For the new generator without sample playback, use the
[fully procedural YZ250 prototype](../YZ250Procedural/README.md).
This page describes the earlier sample-grain comparison bench.

This isolated prototype uses the supplied **2023 YZ250 + FMF Full Exhaust
PURE SOUND** recording. It keeps all 13.19 seconds of stereo PCM and lets you
hold an estimated RPM while changing acoustic load. It adds no catalogue
engine and changes neither the Chevrolet 454 nor the 500 four-stroke motocross.

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

## Compare three listening modes

- **A · Référence**: play the decoded recording at its original speed.
- **B · Reconstruction**: play the same trajectory through overlapping grains,
  still at original speed. This checks preservation of the material before
  evaluating control.
- **C · Moteur piloté**: open the throttle; RPM rises automatically and falls
  when throttle is released.

In C, **Accélérateur** is the default. Hold **Space** for full throttle; releasing
it returns to the slider position. Load slows the rise and lowers the resulting
RPM. Throttle and load also select recorded material; release favors falling-RPM
portions. Losing focus releases Space.

**Banc à régime imposé** retains the earlier behavior: choose RPM directly,
then change acoustic load alone to compare timbre.

Each button starts its listening mode. **M** or “Lecture / arrêt” toggles
playback; resuming restarts the trajectory. Throttle, bench and load control C; volume
is common to all three modes. A and B stop at the recording's end, while C can
be held indefinitely. The interface is French.

Start with A then B: mechanical texture, throttle bursts, irregularities and
stereo should remain recognizable. Then open and release the throttle in C.
Compare a rise at low load with one at high load. Use the bench to hold RPM
and change only load. Listen for attacks,
mechanical body, joins, looping artifacts and control response. Automated
checks do not decide whether the result is realistic.

## What the controls represent

Analysis estimates a **3,660..10,500 RPM** range assuming a single-cylinder
two-stroke. No tachometer accompanies the recording: absolute calibration and
possible harmonic ambiguities remain to be verified. The prototype does not
invent idle below the analyzed range.

Throttle mode adds a simplified listening-driver response without measured
torque or inertia. Released throttle returns to the recorded floor; stopping
cuts playback. This response runs on the audio clock and is independent of UI
frame frequency.

On the bench, load 0..1 mainly selects falling-RPM versus rising-RPM portions.
In throttle mode, that choice also follows throttle and RPM evolution. It is neither
a torque measurement nor a thermodynamic simulation. One recording cannot
provide a complete grid of all RPM/load combinations. Microphone placement and
the FMF exhaust are baked into its timbre; there is no cabin or independent
camera rendering yet.

Mode C overlaps four 120 ms stereo windows, renewed every 30 ms. It selects
material near the requested RPM/load, searches for correlation alignment and
limits transposition to 0.75..1.33. Complete samples are retained without
per-grain normalization or reduction to a periodic waveform. This prototype
stays local to the example pending listening approval; no additional public
package API is created.

## Export and verify

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --debug -o Build/YZ250-Prototype
Build/YZ250-Prototype --check
Build/YZ250-Prototype --render Build/YZ250
```

Export creates `YZ250-Reference.wav`, `YZ250-Reconstruction.wav` and
`YZ250-Controlled.wav` at 44,100 Hz stereo PCM16 with a common 0.7 gain. The third
file lasts 12 seconds: two throttle bursts, first at low load, then at high load,
each followed by release. A short fade closes each export.

`--check` compares A/B over the complete recording, checks load-dependent
material at constant RPM, finite output, stopping, invalid controls, independence
from block sizes, and buttons/layouts without an audio device.
It also checks automatic throttle rise, the load effect, return to the recorded
floor after release, and switching to the bench.

`Assets/Analysis.json` records the original MP3 hash, PCM hash, estimates and
their limits. The prototype reads only embedded assets. The archived MP3 stays
unchanged. To repeat preparation with the decoded 44.1 kHz stereo PCM16 WAV
and original MP3:

```sh
python3 Silex-Examples/Sources/YZ250/Prepare.py Build/YZ250-Source.wav \
  '.archives/EngineSounds/2023 YZ250 + FMF Full Exhaust PURE SOUND.mp3' \
  Silex-Examples/Sources/YZ250/Assets
```
