# Qualify the YZ250 by listening

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
- **C · Moteur piloté**: hold RPM with the first slider and select acceleration
  or release material through the load control.

Each button starts its listening mode. **M** or “Lecture / arrêt” toggles
playback; resuming restarts the trajectory. RPM/load sliders control C; volume
is common to all three modes. A and B stop at the recording's end, while C can
be held indefinitely. The interface is French.

Start with A then B: mechanical texture, throttle bursts, irregularities and
stereo should remain recognizable. Then choose an intermediate RPM in C and
change only load, followed by RPM changes at constant load. Listen for attacks,
mechanical body, joins, looping artifacts and control response. Automated
checks do not decide whether the result is realistic.

## What the controls represent

Analysis estimates a **3,660..10,500 RPM** range assuming a single-cylinder
two-stroke. No tachometer accompanies the recording: absolute calibration and
possible harmonic ambiguities remain to be verified. The prototype does not
invent idle below the analyzed range.

Load 0..1 mainly selects falling-RPM versus rising-RPM portions. It is neither
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
file lasts 12 seconds: held RPM, acceleration, load/release at identical RPM,
then deceleration. A short fade closes each export.

`--check` compares A/B over the complete recording, checks load-dependent
material at constant RPM, finite output, stopping, invalid controls, independence
from block sizes, and buttons/layouts without an audio device.

`Assets/Analysis.json` records the original MP3 hash, PCM hash, estimates and
their limits. The prototype reads only embedded assets. The archived MP3 stays
unchanged. To repeat preparation with the decoded 44.1 kHz stereo PCM16 WAV
and original MP3:

```sh
python3 Silex-Examples/Sources/YZ250/Prepare.py Build/YZ250-Source.wav \
  '.archives/EngineSounds/2023 YZ250 + FMF Full Exhaust PURE SOUND.mp3' \
  Silex-Examples/Sources/YZ250/Assets
```
