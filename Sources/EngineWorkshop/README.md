# Assemble and listen to an engine

This new demo uses only GFX.Audio's part-based engine generator. The separate
`EngineAudio` bench remains available for sound comparisons.

From the workspace or Spec group root:

```sh
silex compile Silex-Examples/Sources/EngineWorkshop/Main.sx --release -o Build/EngineWorkshop
Build/EngineWorkshop
```

**M** or the button toggles ignition. Requested RPM, load and throttle drive the
sound; holding **Space** requests full throttle at 7,000 RPM. Releasing returns
to the selected RPM. Focus loss releases that command. Listening volume is
separate from the engine's four sound branches.

Choose a V8, 450 four-stroke single or 250 two-stroke single, then edit parts.
Changes are prepared after 120 ms without further editing and crossfaded over
50 ms. The newest pending request replaces the previous one. Displayed lengths
refer to the first exhaust; other paths keep their length offsets. Other exhaust
settings apply to all paths together.

- **Block and head**: cylinders, cycle, bore, stroke, chamber and combustion duration.
- **Intake**: runner, airbox and filter absorption.
- **Exhaust**: headers, pipes and silencers.
- **Mechanics and turbo**: mass, damping, wheel, maximum pressure and inertia.
- **Listen to parts**: select a solo branch directly; the four full-mix levels are
  preserved. Solo uses level 1 for that branch. For intake comparisons, accelerate;
  the turbo needs to be fitted and supplied with boost. Small geometry changes
  can be masked in the full mix.

Displacement and geometric compression are derived from the parts. Invalid
assemblies preserve the previous sound. Adjust the chamber when compression
falls outside 2..25. The restore button resets the selected model's parts and
mix without requiring an engine restart.

The page scrolls and cards rearrange with window width. Synthesis, phases,
filters and transitions belong to the package. The demo owns only the RPM
bench, controls and bounded stream feeding: 480-frame blocks and 4,800 queued
frames at 48 kHz, at most 110 ms of prepared/queued PCM excluding device output.
The queue is replenished around UI update/drawing; commands reach queued audio
after this reserve. `--trace-audio` reports empty-queue observations and the
largest update interval when the window closes. This is not a historical device
underrun counter. The V8 preserves its 1:0.1 outlet balance while editing parts.

```sh
Build/EngineWorkshop --trace-audio
Build/EngineWorkshop --check
Build/EngineWorkshop --render Build/EngineWorkshop.wav
silex compile Silex-Examples/Sources/EngineWorkshop/Measure.sx --release -o Build/EngineWorkshop-Measure
Build/EngineWorkshop-Measure
```

`--check` opens neither window nor audio device; it checks models, changes to
dimensions/topology/turbo, drawing at three widths and shutdown. The 12-second
WAV contains idle, acceleration under load with turbo, a silencer change,
overrun and shutdown. The separate measurement program times five repetitions of 480,000 frames per
source for one and eight V8s with turbo at 6,000 RPM, excluding device, PCM
transfer and UI.

The acoustic model is simplified. Timbre and workshop usability still require
listening and interaction; two-strokes do not yet model conical expansion
chambers or detailed scavenging. No sound is certified as an exact commercial
vehicle reproduction. The original bench is preserved.
