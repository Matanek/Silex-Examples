# Validated engines through GFX.Audio

[Français](README.fr.md)

This demo consumes `GFX.Audio.Engines`. The package owns simulation, profiles,
exhaust responses, intake and output processing. The demo owns input, the
instrument display and stream feeding. The autonomous `EngineAudio` bench
remains available as an independent comparison witness.

Prepare a library with GFX.Audio's tools, then from the workspace or Spec group:

```sh
silex compile Silex-Examples/Sources/EngineLibrary/Main.sx --debug -o Build/EngineLibrary-Demo
Build/EngineLibrary-Demo /absolute/path/to/EngineLibrary
```

**M** toggles ignition; hold **Space** to accelerate. Release or focus loss closes
the throttle. Ignition can be cut while rotating. Engine selection requires
ignition off and rotation stopped. Controls retain the first bench's meaning:
holding speed, load, exhaust, texture, ambience and volume. Intake is shown only
for the 450 four-stroke, which supplies measured aspiration flow.

Sound retains the full reference simulator at 44.1 kHz stereo. Playback keeps
five queued blocks and at most four requested calculations ahead, about 98 ms
excluding device output. The interface consumes ready blocks without waiting
for simulation. Closing releases stream and engine. No private demo sound source
or parts generator is used.

Checks without a window or audio output:

```sh
silex compile Silex-Examples/Sources/EngineLibrary/Check.sx --debug -o Build/EngineLibrary-Demo-Check
Build/EngineLibrary-Demo-Check /absolute/path/to/EngineLibrary
silex compile Silex-Examples/Sources/EngineAudio/PackageParity.sx --release -o Build/EngineLibrary-Parity
Build/EngineLibrary-Parity /absolute/path/to/EngineLibrary
```

The comparator uses the original bench as an independent oracle with its usual
runtime under `Build/EngineReference`. PCM and RPM must match for all eight
profiles across control changes. This historical runtime is needed only by the
comparator, not by the new demo. The
[package guide](../../../Packages/GFX.Audio/Docs/EN/Engines.md) explains
deployment, API and qualification limits.

The UI command above uses Debug for local checks under the 4 GiB guard. The
simulator remains a Release build. The full window’s Release compilation exceeds
that guard with the current compiler and remains to be qualified.
