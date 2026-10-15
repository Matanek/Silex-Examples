# Steering, brakes and suspension

A 100 kg chassis drops onto four suspended wheels. Springs support its weight;
white rods show their length and green pads identify ground supports. White
hub bars rotate with the physical wheel angles. Tires are passive: ground
contact spins them. Steering turns the front wheels; brakes slow their rotors and contact transfers
force. P launches the chassis by impulse; the powertrain remains future work.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

After landing, **P** launches the vehicle, **←/→** turn and **F** stops it.
**↑** centers the wheels. Steering remains selected after releasing a key until
another choice. Left/right follow the vehicle frame, marked by its yellow strip.
**F/H** activate or release their brakes. Repeat with **G** to compare without
grip: wheels steer but the vehicle slides even with brakes active. The camera follows the
chassis while the metric ground grid makes travel visible. Buttons perform
the same actions as keyboard keys. The yellow strip marks the chassis front (+Z).

- **P / Push forward** applies a 200 N·s impulse along the chassis forward
  direction. Ground contact spins the tires, sharing the initial motion.
- **←/→ / Steer** selects a maintained 18° front-wheel angle; **↑** centers it.
- **F / Brake** activates/releases all four brakes, limited to 1500 N·m per wheel.
- **H / Handbrake** activates/releases only the rear brakes, limited to 20 N·m.
- **V / Push sideways** applies 200 N·s laterally. Tire grip resists drift;
  without tires, lateral velocity persists.
- **G / Grip** switches mode and **recreates** the vehicle above the ground.
  The no-grip mode retains suspension but removes virtual tires: wheels
  remain unspun and transmit no tangential force.
- **B / Jump** applies a vertical 500 N·s impulse, losing then regaining support.
- **C / Overload** applies downward force for two seconds, compressing the
  suspensions to their stops before they recover.
- **Space / Pause** freezes chassis motion, wheel angles and overload time.
- **R / Recreate** preserves the selected mode and recreates the vehicle above ground. R and G release brakes and center steering.
- **Escape** closes the window.

Physical actions and recreation resume a paused simulation. A new overload
replaces its remaining duration with two seconds. Successive pushes accumulate;
keyboard auto-repeat is ignored. The panel shows mode, speed, height, support
count, steering angle and total normal force. At rest: about 88 cm, four supports and 981 N.

## Verification

```sh
silex compile Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release -o .silex/vehicle-suspension
.silex/vehicle-suspension --physics-check
.silex/vehicle-suspension --controls-check
.silex/vehicle-suspension --smoke
```

The **TEST AUTOMATIQUE** run closes after dropping, jumping, losing/regaining
support, overloading, pausing, rolling, pushing, comparing grip modes, turning, stopping and rear braking. It
checks physical values, rendered transforms and framing through the actual
ECS camera. Ordinary controls are hidden in this mode. Headless paths check
physics at 60/120 Hz and keyboard/button events. They do not replace observing
visual readability.

Simulation advances at 120 Hz. Rendering interpolates poses, lengths, steering and angles
with unwrapping across ±2π. Meshes are created once and shared; the grid moves
only at five-meter boundaries. The panel refreshes at most ten times per second
and after commands. Supports are observed at the start of a step, while the
final pose is interpolated; this may slightly offset a pad during an impact.

SDK guides: [suspension](../../../../Packages/GFX.Physics/Docs/EN/VehicleSuspension3D.md)
[passive tires](../../../../Packages/GFX.Physics/Docs/EN/PassiveTires3D.md)
and [wheel controls](../../../../Packages/GFX.Physics/Docs/EN/VehicleControls3D.md).
