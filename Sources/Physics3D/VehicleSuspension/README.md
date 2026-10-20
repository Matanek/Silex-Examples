# Feel suspension and compare toppling

A 100 kg chassis rests on four suspended wheels. A 30 N·m engine drives the
rear wheels through an automatic gearbox. Tire contacts accelerate, turn and
brake the vehicle. White hub bars show physical rotation; the yellow strip
marks the front. The camera follows the chassis over a metric ground grid.
A raised purple band lies ahead; **40 cm cylinder** mode is selected initially.

**Soft suspension** is selected initially. **Z** raises the nose;
**X then F** makes it dive under braking. Left and right arrows lean the body
towards the outside of a turn. **M** recreates the vehicle with the previous
firm setup; repeat the same manoeuvres to compare. The button shows the setup,
and telemetry reports physical pitch and roll. Wait for landing before driving.

**A** compares anti-roll bars: first drive a turn with **Z and ←/→**, press A,
wait for landing and repeat the same manoeuvre. The body leans less towards
the outside; the button shows the current choice. The initial setup remains
soft with no bars, preserving the previous feel. M still compares soft/firm.
Throttle, tires and dampers are identical between A comparisons. Straight-line
acceleration pitch and braking dive remain present.


**O** launches the chassis with a jump and a roll impulse. To compare from rest,
press R, wait for landing and press O: without protection the car can overturn.
**L** recreates the same vehicle with a 45° total inclination limit; wait for
landing and repeat O. The body leans strongly and then regains wheel support.
Correction is gradual, with a small transient overshoot of the target.

The initial setup stays soft, with no bars or tilt limit. L preserves suspension,
tires, grip and obstacle; R, M, T, G and A preserve the limit choice. The two
buttons perform the same actions as the keys. The 500 N·s jump and 400 N·m·s
angular impulse are identical in both cases; displayed angles and rendering
come from simulation.

The soft preset uses 1,200 N/m and 160 N·s/m per wheel, versus 10,000 and
1,000 for firm. Its 77.985 cm maximum extension compensates for the greater
static spring compression, preserving the roughly 87.55 cm resting height.
Engine, mass, inertia and tires are identical between presets. Contact forces
and the four suspensions produce body rotation. Wide cylinders limit roll
more than rays; T retains the contact comparison without promising equal lean.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

To compare, wait for landing, press **Z** and let the vehicle cross the purple
band. The 40 cm tires find support on its edges and lift the chassis. **T**
recreates the same vehicle with 8 cm tires: press **Z** again; they miss the
band and the chassis keeps its ground supports. Their visible width follows
their physical width. Engine, wheel radius and band remain identical.

T cycles **ray → sphere → 40 cm cylinder → 8 cm cylinder → ray**. The button
shows the current mode. Center rays also miss the band; a 12 cm cast sphere
reaches its edges.

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
- **O / Topple** adds a jump and an angular impulse around the chassis forward
  direction. Wait for a fresh vehicle to land before comparing.
- **L / Limit** switches free/45°, recreates the vehicle and resumes simulation
  while preserving other settings. The bound covers combined pitch and roll.
- **A / Anti-roll** enables or disables two 1000 N/m bars and recreates only
  the vehicle, releasing controls and resuming simulation. R, M, T and G preserve
  this choice. A pair stops coupling when either wheel loses support.
- **M / Suspension** switches soft/firm and recreates the vehicle with controls
  released and simulation resumed. R, G and T preserve the preset.
- **T / Contacts** cycles all four modes and recreates the vehicle with
  throttle, steering and brakes released. Cylinders have a total width of
  40 or 8 cm, a radius of 30 cm and a steered axle; sphere mode retains its
  separate 12 cm cast radius. The band measures 1.68 × 0.18 × 4 m, with edges
  6 cm from wheel axes: a 4 cm half-width cannot reach it; 20 cm can.
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
with rays, spheres, wide cylinders and narrow cylinders: band supports,
chassis lift, mode switching and pause. It then tests soft suspension on a plain
floor: pitch, braking dive, opposite turns, recovery, pause and soft/firm
recreation. Let it close normally. It checks physics,
rendered transforms and framing through the actual ECS camera. Rendered tire/hub
widths and band mesh dimensions/pose are compared with their physical settings;
band support points stay in the useful frame. Headless paths verify
physics at 60/120 Hz (both presets, suspension travel, recovery and no engine
lean without grip) and keyboard/button input; they do not replace observing
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

## Check the anti-roll comparison

The headless `-- --anti-roll-check` path compares opposite turns and straight
driving with ray/wide-cylinder contacts at 60/120 Hz, braking recovery, no-grip
absence of motion and obstacle crossings with 40/8 cm tires. The SDK produces
these reactions at physical support points. No presentation angle is added,
and bars do not define a maximum body-tilt angle. Their Jolt spring coupling
also depends on the fixed time step and damping.

The smoke preserves earlier scenarios, then compares both turns with bars,
rendered transforms, pause and recreation. TEST AUTOMATIQUE windows close on
completion. The interactive trial is for judging softness and how clearly
this difference can be felt.

## Check toppling and protection

`-- --tilt-check` selects the 16 headless toppling recipes: 60/120 Hz, opposite
impulses, ray/cylinder contacts, soft/firm suspension and anti-roll bars.
Checks cover the real impulse, free overturning, bounded tilt, support and mean
weight during the last recovery second. `--physics-check` retains all eight
previous physical recipes.

The smoke continues the previous checks with both topples, rendered physical
poses, pause and limit recreation. Interactive testing assesses how clearly
this optional protection reads and feels.
