# engine-sim audio witness

[Français](README.fr.md)

This development tool runs multiple engine-sim profiles without the Windows UI.
It provides a witness for the Silex listening bench. The full thermal simulation
runs outside GFX.Audio. A reduced game implementation must be compared against
this witness before claiming the same sound character.

## Build on macOS ARM64

Requirements: Xcode with Clang/Flex, CMake, Python 3.12+ and Bison 3.2+.
Bison can be built in a local directory. The Piranha reader requires a newer
version than `/usr/bin/bison` on the tested host.

From the workspace or Spec group root, prepare a dedicated public checkout
without downloading the Windows graphics dependencies:

```sh
git clone --filter=blob:none https://github.com/ange-yaghi/engine-sim.git Build/EngineReference-Upstream
git -C Build/EngineReference-Upstream switch --detach 85f7c3b959a908ed5232ede4f1a4ac7eafe6b630
git -C Build/EngineReference-Upstream submodule update --init dependencies/submodules/simple-2d-constraint-solver dependencies/submodules/piranha dependencies/submodules/csv-io
python3 Silex-Examples/Tools/EngineReference/Build.py \
  --source Build/EngineReference-Upstream --output Build/EngineReference \
  --bison /path/to/bison
```

The checkout must contain revision `85f7c3b959a908ed5232ede4f1a4ac7eafe6b630`
and the dependency commits pinned in `Build.py`. The script archives these
commits independently of local checkout modifications. It changes only its
generated copy under `Build/EngineReference/Source`, builds the helper and
stages its runtime. `Provenance.json` records source revisions and binary/IR
hashes. Keep handwritten files outside this generated directory.

Portability adaptations preserve the original values and equations: portable
includes, inline constants, explicit default gas mixture, a renamed template
parameter, a complete type include, a name correction in `RingBuffer::overwrite`,
Piranha paths through `std::filesystem`, and removal of an unused graphics
include. Original profiles retain engine-sim’s gas and constraint calculations. Delta Studio,
Discord and the Windows application are excluded from this build.

The FIR sum supports vectorization through reassociated additions in
`convolution_filter.cpp` only. `--scalar-fir` builds the strict scalar control.
The comparison requires a maximum difference of 32 PCM16 units and an error
RMS below 0.0001 full scale, with identical RPM. This checks numerical
adaptation rather than perceptual realism.

## Exhaust blend

At 100%, convolution PCM remains identical to the accepted witness. Below it,
the raw branch uses DC-removed pressure without the derivative pre-emphasis
intended for convolution. Mean powers are tracked over 120 ms to balance the
branches (maximum gain 16); the control is smoothed over 10 ms. Processing is
local to each channel without per-sample allocation. This removes the previous
blend’s electrical texture jump; the final colour still needs listening.

```sh
ctest --test-dir Build/EngineReference/CMake --output-on-failure
python3 Silex-Examples/Tools/EngineReference/ExhaustChecks.py \
  --binary Build/EngineReference/RenderReference \
  --baseline Build/EngineReference/RenderReference-Before-Controls \
  --runtime Build/EngineReference/Runtime \
  --report Build/EngineReference/Exhaust-Checks.json
```

The check compares all eight profiles at 100% against the preserved previous
helper, then tests 99.9, 99, 90, 50 and 0% on the Chevrolet. It checks transitions,
no clipping in the scenario and identical telemetry. The synthetic C++ check
also exercises branches with very different signal levels.

## Run and verify

The [demo](../../Sources/EngineAudio/README.md) provides `--reference`.
The helper also offers two deterministic offline renders:

```sh
cd Build/EngineReference/Runtime
../RenderReference Profile454.mr Impulse.pcm Witness full
../RenderReference Profile454.mr Impulse.pcm Base base
```

Each writes 14 seconds of mono 44.1 kHz audio, a CSV of RPM/controls and a
10 kHz float32 trace containing RPM, cycle angle and both exhaust pressures.
`full` retains the profile's initial audio settings. `base` disables convolution,
derivative, jitter and air noise. This is a defined diagnostic stage, not an
identification of the video's settings at 4:48–5:00.

From the work root after rendering the demo:

```sh
python3 Silex-Examples/Tools/EngineReference/Verify.py \
  --binary Build/EngineReference/RenderReference \
  --runtime Build/EngineReference/Runtime \
  --bridge-wave Build/EngineReference/Bridge.wav \
  --report Build/EngineReference/Verification.json
```

This checks packets, bit-exact repeated runs, mechanical stages, bounds and
final silence, rejection of invalid requests and PCM transfer into Silex with
its gain. `--scalar-binary /path/to/RenderReference` also compares the vectorized
FIR against the scalar control. The private `serve` protocol receives one line
per block: mono frames (1–960), ignition (0/1), pedal, texture, convolution,
bench RPM and load. Replies contain four little-endian uint32 values (magic
`0x34563845`, frames, RPM × 1,000, starting state), followed by mono PCM16. The
Silex client copies this into a stereo GFX.Audio stream.

The runtime uses each profile’s 10–40 kHz simulation, eight gas substeps and 44.1 kHz synthesis.
The full calculation remains intentional for this single witness. The live client
uses a bounded FIFO with nonblocking polling; offline rendering stays synchronous.
Allocation behavior, latency and multiple game vehicles remain unqualified.
This development tool is tested on macOS ARM64 only.

## Profiles, transmission and two-stroke model

`Profiles.json` is the shared catalogue. Silex embeds it through JSON; Build.py
generates native vehicle settings, scripts and PCM impulses. Provenance.json
records the catalogue, local-profile hashes and pinned dependencies. Local files
in `Profiles/` adapt the MIT-licensed TRX520 single into generic motocross engines.
Some upstream `new/` IR references are absent at the pin: available smooth_39 and
archive/test_engine_14/15 responses are selected. These choices do not reproduce
the video’s exact settings.

Private `drive` requests extend `serve` with mode (1 auto, 2 manual), requested
gear (0=N, then 1..n) and brake (0..1). Replies contain eight little-endian uint32s:
magic `0x36563845`, frames, RPM × 1,000, starting, gear, km/h × 1,000, flags
(bit 0 shifting, bit 1 unsafe downshift), shift count. Mono PCM16 follows this
32-byte header. The helper’s optional final argument selects a catalogue index,
defaulting to 0 for the accepted 454.

Private `serve-intake` and `drive-intake` retain the `serve`/`drive` commands and
headers, with magic `0x38563845`/`0x39563845`. Each frame interleaves int16
pressure and uint16 positive intake flow (0..65535 represents 0..0.25 m³/s of
ambient air). Flow sums positive intake-valve aspiration, converts moles per
mechanical step at 25 °C and 1 atm, and resamples on the original synthesizer’s
exact clock. Below 60 RPM, a progressive weight removes numerical gas
equilibration jitter at rest; this is independent of ignition. Capture is
read-only: pressure and telemetry remain bit-exact with the historical modes. Only the 4T client requests this protocol.

Drive.cpp controls engine-sim’s vehicle/transmission with a wheel-brake constraint,
progressive clutch pressure and predicted coupled-RPM downshift protection. Ratio
changes preserve vehicle kinetic energy and speed. Profile or Banc/Route changes
require ignition off and a stationary vehicle. Audio stays bounded to four
outstanding requests and five queued blocks.

TwoStroke.py changes only the generated snapshot: configurable ignition period
and a single-cylinder gas branch with exhaust/transfer ports near BDC, followed
by compression and combustion every revolution. A prescribed-pressure transfer
reservoir simplifies crankcase pumping. This is a sound prototype rather than
validated two-stroke thermodynamics. Defaults retain the four-stroke path,
checked against the accepted 454 binary. CycleCheck executes the adapted ignition
module, counting 20 versus 10 sparks over 20 crank revolutions.

```sh
ctest --test-dir Build/EngineReference/CMake --output-on-failure
python3 Silex-Examples/Tools/EngineReference/FleetVerify.py \
  --binary Build/EngineReference/RenderReference \
  --runtime Build/EngineReference/Runtime \
  --report Build/EngineReference/Fleet-Native.json
```

This checks all profiles’ starts, automatic shifts, braking and stops, then safe
manual shifts, unsafe-downshift rejection, neutral, continuous speed and relaunch.
Listening and game qualification remain necessary. Build.py atomically renames
a fresh executable inode to avoid stale signed code pages on macOS rebuilds.

Motocross impulses are prepared offline: a presence shelf at 2 kHz, 4T body
at 250 Hz and a tapered 60/45 ms tail. These two profiles use a 6 kHz input
filter; original profiles retain 1,900 Hz. The 2T leveler captures peaks
immediately without an attenuation floor before PCM16 conversion. These broad
settings are guided by supplied recordings and still require listening feedback.
User recordings are not copied into package sources.

The 4T IR also applies frequency-dependent absorption. `mid_decay_ms=24` and
`high_decay_ms=14` are tau constants in exp(−t/tau), not total tail durations.
A two-pole split at 350/1,800 Hz retains the low body while mid/high ringing
decays faster. Zero values preserve existing recipes exactly. Preparation is
offline and changes neither RPM nor helper code. Broad spectral balance and
RMS alone do not qualify an impact: compare its attack and tail independently
of airflow, then in the complete sound.

```sh
python3 Silex-Examples/Tools/EngineReference/ImpulseChecks.py
```


```sh
python3 Silex-Examples/Tools/EngineReference/IntakeChecks.py \
  --binary Build/EngineReference/RenderReference \
  --runtime Build/EngineReference/Runtime \
  --report Build/EngineReference/Intake-Checks.json
```

## Attribution

[engine-sim](https://github.com/ange-yaghi/engine-sim/tree/85f7c3b959a908ed5232ede4f1a4ac7eafe6b630),
copyright 2022 AngeTheGreat (Ange Yaghi), is accompanied by its
[MIT license](LICENSE.engine-sim), also staged beside the generated runtime.
Profile: `assets/engines/chevrolet/engine_03_for_e1.mr`. IR:
`assets/sound-library/smooth/smooth_39.wav`. The build uses the pinned
[SCS](https://github.com/ange-yaghi/simple-2d-constraint-solver),
[Piranha](https://github.com/ange-yaghi/piranha) and
[csv-io](https://github.com/ange-yaghi/csv-io) submodules. Their sources are
retrieved separately and are not included in this repository. Engine sources
and the video's audio are not copied into GFX.Audio.
