# Free wheels: rolling, grip and suspension

A 100 kg chassis drops onto four suspended wheels. Springs support its weight;
white rods show their length and green pads identify ground supports. White
hub bars rotate with the physical wheel angles. Tires are passive: ground
contact spins them. There is no engine or steering input.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

After landing, try **P**, then **R** and **V**. Repeat with **G** to compare
without grip: the same push now produces a slide. The camera follows the
chassis while the metric ground grid makes travel visible. Buttons perform
the same actions as keyboard keys. The yellow strip marks the chassis front (+Z).

- **P / Push forward** applies a 200 N·s impulse along the chassis forward
  direction. Ground contact spins the tires, sharing the initial motion.
- **V / Push sideways** applies 200 N·s laterally. Tire grip resists drift;
  without tires, lateral velocity persists.
- **G / Grip** switches mode and **recreates** the vehicle above the ground.
  The no-grip mode retains suspension but removes virtual tires: wheels
  remain unspun and transmit no tangential force.
- **B / Jump** applies a vertical 500 N·s impulse, losing then regaining support.
- **C / Overload** applies downward force for two seconds, compressing the
  suspensions to their stops before they recover.
- **Space / Pause** freezes chassis motion, wheel angles and overload time.
- **R / Recreate** preserves the selected mode and recreates the vehicle above ground.
- **Escape** closes the window.

Physical actions and recreation resume a paused simulation. A new overload
replaces its remaining duration with two seconds. Successive pushes accumulate;
keyboard auto-repeat is ignored. The panel shows mode, speed, height, support
count and total normal force. At rest: about 88 cm, four supports and 981 N.

## Verification

```sh
silex compile Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release -o .silex/vehicle-suspension
.silex/vehicle-suspension --physics-check
.silex/vehicle-suspension --controls-check
.silex/vehicle-suspension --smoke
```

The **TEST AUTOMATIQUE** run closes after dropping, jumping, losing/regaining
support, overloading, pausing, rolling, pushing and comparing grip modes. It
checks physical values, rendered transforms and framing through the actual
ECS camera. Ordinary controls are hidden in this mode. Headless paths check
physics at 60/120 Hz and keyboard/button events. They do not replace observing
visual readability.

Simulation advances at 120 Hz. Rendering interpolates poses, lengths and angles
with unwrapping across ±2π. Meshes are created once and shared; the grid moves
only at five-meter boundaries. The panel refreshes at most ten times per second
and after commands. Supports are observed at the start of a step, while the
final pose is interpolated; this may slightly offset a pad during an impact.

SDK guides: [suspension](../../../../Packages/GFX.Physics/Docs/EN/VehicleSuspension3D.md)
and [passive tires](../../../../Packages/GFX.Physics/Docs/EN/PassiveTires3D.md).
