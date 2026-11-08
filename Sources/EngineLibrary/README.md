# Validated engines through GFX.Audio

[Français](README.fr.md)

This demo consumes `GFX.Audio.Engines`. The package owns simulation, profiles,
exhaust responses, intake and output processing. The demo owns input, the
instrument display and stream feeding. The autonomous `EngineAudio` bench
remains available as an independent comparison witness.

The package supplies the standard engines on macOS ARM64. From the workspace
root, launch the demo directly without additional preparation:

```sh
silex run Silex-Examples/Sources/EngineLibrary/Main.sx
```

A custom library remains optional: after compilation, pass its absolute path
as the binary’s first argument.

**M** toggles ignition; hold **Space** to accelerate. Release or focus loss closes
the throttle. Space retains priority after clicking a button; Enter activates
the focused control. Ignition can be cut while rotating. Switching free/road mode
requires only ignition off, without waiting for deceleration; it resets the bench.
Engine-profile selection still requires ignition off and rotation and vehicle
stopped. Controls retain the first bench's meaning:
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
Build/EngineLibrary-Demo-Check
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

## Optional transmission

Enable **Mode Route · boîte de vitesses** after switching ignition off.
The gearbox starts in automatic mode. **A** switches automatic/manual;
**↑ / ↓** or +/− request gears, **N** selects neutral and holding **S** brakes.
The instrument shows mode, gear, speed and overspeed rejection. Ignition can
be cut while moving. Rejected requests do not engage later without a new command;
after N while moving, successive + commands can reach a safe gear.

Disable road mode once ignition is off to return to the free bench, even while
the engine or vehicle is still slowing down; the new context starts at rest.
Holding RPM and load controls appear only in free mode, where they apply. Transmission and
telemetry are supplied by `GFX.Audio.Engines`, not private demo calculations.

Buttons describe their next action: **Démarrer** or **Arrêter**, **Passer en
manuel** or **Passer en automatique**. The road checkbox uses the panel’s light
foreground color.

In road mode, open **Régler la démultiplication** to stage final-drive and
individual gear ratios. A larger numeric value shortens the gearing; at the
same speed, the engine turns faster. Ratios must decrease from first to last.
**Appliquer la démultiplication** requires the engine and vehicle to be stopped.
Dragging these sliders does not change the simulation before applying.
**Rapports d’origine** restores the profile’s stock gearbox. Selecting another
profile also restores its stock values. The demo retains each profile’s gear
count; the API accepts custom gearboxes with 1..12 ratios. Prepare a v2 bank
for this workflow.

Stock gearing remains the default. A taller gear does not guarantee more
acceleration: engine torque and vehicle drag also affect the result.
