# Suspension: weight, support and rebound

A 100 kg chassis drops onto four suspended wheels. Springs carry its weight,
white rods show their length and green pads mark ground support. Wheels and
chassis follow the physical simulation.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

- **B / Jump** applies an upward impulse: wheels leave the ground, extend,
  then regain support on landing.
- **C / Overload** adds a downward force for two seconds: suspension compresses
  to its stops and returns under chassis weight alone.
- **Space / Pause** freezes movement and remaining overload duration.
- **R / Recreate** destroys and recreates the vehicle above the ground.
- **Escape** closes the window.

Jump, overload and recreate resume a paused simulation. A new overload replaces
its remaining duration with two seconds rather than adding another force.
Keyboard auto-repeat does not repeat actions.

The panel shows chassis height, support count and total normal force. At rest,
height is close to 88 cm and total force to 981 N. Forces rise on landing and
under overload; they are zero in flight. Wheels are not powered yet: this scene
shows suspension without tire traction, steering or braking.

## Checks

```sh
silex compile Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release -o .silex/vehicle-suspension
.silex/vehicle-suspension --physics-check
.silex/vehicle-suspension --controls-check
.silex/vehicle-suspension --smoke
```

The automatic run is titled **TEST AUTOMATIQUE** and closes after dropping,
jumping, losing/regaining support, overloading, pausing and recreating. It
checks physical data, framing and rendered element transforms. Ordinary
controls are not displayed during this run. Headless paths check physics at
60/120 Hz and keyboard/button events.

Simulation advances at 120 Hz; rendering interpolates poses and lengths.
Meshes are built once and shared. The panel refreshes at most ten times per
second, plus command changes. Supports are sampled at the start of a step,
then the final pose is interpolated. This timing can slightly offset a marker
at impact.

The SDK and its Jolt witness are described in the
[suspension guide](../../../../Packages/GFX.Physics/Docs/EN/VehicleSuspension3D.md).
