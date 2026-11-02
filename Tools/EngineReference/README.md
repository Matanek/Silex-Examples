# engine-sim audio witness

[Français](README.fr.md)

This development tool runs the original Chevrolet 454 without its Windows UI.
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
include. Gas and constraint calculations remain engine-sim's. Delta Studio,
Discord and the Windows application are excluded from this build.

The FIR sum supports vectorization through reassociated additions in
`convolution_filter.cpp` only. `--scalar-fir` builds the strict scalar control.
The comparison requires a maximum difference of 32 PCM16 units and an error
RMS below 0.0001 full scale, with identical RPM. This checks numerical
adaptation rather than perceptual realism.

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

The runtime uses a 10 kHz simulation, eight gas substeps and 44.1 kHz synthesis.
The synchronous path and full cost are intentional for this single witness.
Allocation behavior, latency and multiple game vehicles remain unqualified.
This development tool is tested on macOS ARM64 only.

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
