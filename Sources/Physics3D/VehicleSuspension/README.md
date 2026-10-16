# Compare wheel contacts at an edge

A 100 kg chassis rests on four suspended wheels. A 30 N·m engine drives the
rear wheels through an automatic gearbox. Tire contacts accelerate, turn and
brake the vehicle. White hub bars show physical rotation; the yellow strip
marks the front. The camera follows the chassis over a metric ground grid.
A raised purple band lies ahead; **sphere** mode is selected initially.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

To compare, wait for landing, press **Z** and let the vehicle cross the purple
band. Sphere contacts reach its edges and lift the chassis. **T** recreates it
with ray contacts: press Z again; the rays miss the band and the chassis keeps
its ground supports. T switches back. The **Contacts** button shows the current
choice. The engine and band are identical in both runs.

After landing, **Z** accelerates forward, **S** requests reverse and **X**
releases throttle. These inputs remain selected after releasing the key.
**←/→** select maintained steering; **↑** centers it. **F/H** activate or
release their brakes. **R** starts fresh with released throttle and straight
wheels. Buttons perform the same actions.

- **Z / Accelerate** selects 60 % throttle and forward direction.
- **S / Reverse** selects 50 % and reverse direction. The gearbox opens then
  engages its clutch; a vehicle traveling forward must first slow down.
- **X / Release** sets throttle to zero. Tires continue rolling.
- **←/→ / Steer** selects 18° front-wheel steering; **↑** centers it. Left/right
  follow the vehicle frame marked by its yellow strip, rather than screen edges.
- **F / Brake** activates/releases all four 1500 N·m wheel brakes.
- **H / Handbrake** activates/releases only the 20 N·m rear brakes.
- **T / Contacts** switches ray/sphere and recreates the vehicle with throttle,
  steering and brakes released. The cast sphere radius is 12 cm; physical wheel
  radius remains 30 cm. The band measures 1.68 × 0.18 × 4 m, with edges 6 cm
  from wheel axes. This contact volume is an approximation; it does not
  reproduce the complete cylindrical tire shape.
- **G / Grip** changes mode and recreates the vehicle. Without grip, suspension
  still supports the chassis and rotors remain engine-connected, but friction
  curves are zero. Z spins wheels without propelling the chassis; P produces
  a slide the wheel brakes cannot stop.
- **P / Push forward** applies a 200 N·s impulse along chassis forward,
  separate from the engine. **V** applies the same impulse sideways.
- **B / Jump** applies 500 N·s vertically, losing then regaining support.
- **C / Overload** adds downward force for two seconds, compressing suspensions
  to their stops before they recover.
- **Space / Pause** freezes chassis, wheels, engine RPM and overload time.
- **R / Recreate** preserves grip mode, releases throttle and brakes, centers
  steering and recreates the vehicle above ground.
- **Escape** closes the window.

Throttle, steering and brakes combine. Use X before testing a stop, then F for
service braking; press F again to release it. Actions resume a paused simulation;
keyboard repeat is ignored. G, R and T reset all inputs; G and R preserve the selected contact mode.

The panel shows speed, steering, height, supports and suspension forces, then
engine RPM, gear, clutch and throttle. Gear 0 means neutral; negative gears
mean reverse. Gear changes are automatic. At rest: about 88 cm, four supports
and 981 N.

## Verification

```sh
silex compile Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release -o .silex/vehicle-suspension
.silex/vehicle-suspension --physics-check
.silex/vehicle-suspension --controls-check
.silex/vehicle-suspension --smoke
```

The **TEST AUTOMATIQUE** run closes after suspension, rolling, grip, steering
and brake checks, then acceleration, reverse, stopping, powered wheels without
grip and engine pause on a plain floor. It then compares the same obstacle
with rays and spheres: band supports, chassis lift, mode switching and another
pause. Let it close normally. It checks physics, rendered
transforms and framing through the actual ECS camera. Band mesh dimensions
and pose are compared with its physical body; band support points stay in the
useful frame. Headless paths verify
physics at 60/120 Hz and keyboard/button input; they do not replace observing
the rendering.

Simulation runs at 120 Hz, with rendered interpolation of poses, lengths and
angles. Meshes are created once and shared, the grid moves at five-meter
boundaries, and the panel updates at most ten times per second or after input.
Supports sampled at step start may appear slightly offset from the final
interpolated pose during an impact.

SDK guides: [suspension](../../../../Packages/GFX.Physics/Docs/EN/VehicleSuspension3D.md),
[tires](../../../../Packages/GFX.Physics/Docs/EN/PassiveTires3D.md),
[steering and brakes](../../../../Packages/GFX.Physics/Docs/EN/VehicleControls3D.md)
and [powertrain](../../../../Packages/GFX.Physics/Docs/EN/VehiclePowertrain3D.md).
