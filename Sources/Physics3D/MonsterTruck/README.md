# Soft-tire monster truck

[Français](README.fr.md)

Drive a pickup with four deformable tires in a geometric freestyle arena:
jump tables, a mound with four approaches, large ramps, a landing ramp,
a two-sided bowl and small rollers. The brown floor retains a grid to show
speed. Yellow and red surfaces mark the lines, with white borders.

## Launch and drive

From the workspace root containing `Silex-Examples/`, prepare a v3 native bank
with the tools in `Packages/GFX.Audio/Native/EngineSimulator`, then compile
without opening a window:

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release -o Build/MonsterTruck-Drive-Response
Build/MonsterTruck-Drive-Response --engine-library /absolute/path/to/EngineLibrary
```

Chevrolet 454 sound is enabled by default. Without an option, the bank path is
`Build/EngineLibrary-Monster-Package`, relative to the current directory. An
explicit absolute path works from any directory. `--silent` retains driving
without opening an audio engine or device. The HUD displays physical engine RPM and selected gear.
The interface and renderer retain their usual controls.

| Control | Action |
| --- | --- |
| Hold Z | Progressive normal acceleration |
| Shift + Z | Turbo: 25% more torque and a sharper response |
| Hold S | Front brake and immediate reverse request |
| Shift + S | Stronger four-wheel service braking to lift the rear |
| Q / D | Front steering, left / right from the rear camera |
| A / E or ← / → | Rear steering in the desired direction of the nose |
| T | Couple / separate the steering axles |
| Hold Space | Rear handbrake |
| P | Monster / Low / Firm inflation without restarting |
| Plus court / Plus long | Adjust final drive at rest with the throttle released |
| R | Restart with the selected inflation and final drive |
| Mouse wheel | Chase-camera distance |
| Escape | Quit |

While driving forward, A or ← turns the nose left, so the rear wheels steer
right. Initial coupled steering moves the axles in opposite directions to
tighten turns. Rear inputs override coupling. In independent mode, Q + E or
D + A enables crab motion.

The camera follows horizontal travel with a level horizon. It holds its last
course at low speed or at rest, so wheelies and rollovers do not rotate it with
the chassis. Reversing gradually turns the view toward the new travel direction.

Start straight ahead with the large table, then explore the central mound
and its four approaches. The left side has a takeoff and separate landing;
the right side has a bowl with two slopes. Small rollers are at the far end.
A calibration lane with a bump and three blocks remains on the far left.

For a wheelie, briefly press Shift + Z, then release. To lift the rear,
build speed and briefly press Shift + S. Torque and braking physically pitch the
vehicle: time the inputs to recover its balance. Then compare the same
obstacle with all three inflation settings.

## Physical assembly

Each tire is 2.20 m in diameter and 1.32 m wide, with a 1.32 m rim and
1.56 m flanges. It has 192 vertices, 384 triangles and 96 internal shear
diagonals. The 48 bead links exchange impulses with the rim; vertices
remain dynamic.

Low compresses more under load than Monster; Firm deforms less. Under this
assembly's reference load, loaded radii are approximately 1.00 / 1.11 / 1.17 m.
Coefficients 60 / 1400 / 2600 are not calibrated bar values. The chassis weighs
150 kg, each rim 20 kg and each carcass 9.6 kg.

The engine, clutch and differentials in `GFX.Physics.WheelDrive3D` actually
drive the rims. The engine has a nominal peak torque of 240 N·m between 850 and 7000 RPM,
calibrated for this demonstration’s masses. Its automatic transmission uses
three close ratios, 3.2 / 2.6 / 2.1, and reverse −3.2. Upshifts occur at
4200 RPM and downshifts at 1700 RPM; transitions open then reengage the clutch.
An unsupported wheel receiving drive torque prevents upshifts. Launch modulates clutch pressure.

The center differential redistributes torque to the axle retaining traction
when the other spins. GFX.Physics provides this through
`differential_limited_slip_ratio:2.2`, avoiding wasted torque in unloaded front
wheels during acceleration. Each axle’s left/right distribution remains separate.

Final drive starts at 8 and is adjustable from 6 to 12 using the buttons.
A higher value shortens gearing: slower wheels at equal engine RPM, higher
engine RPM at equal wheel speed. Torque multiplication changes too. Traction,
load and gear shifts still limit actual acceleration. Adjustment is rejected
while the vehicle or wheels are moving, or while the throttle remains applied.
R retains the setting. `Transmission.sx` and `Model.sx` own this demo’s
configuration and driving policy.

During normal driving, a governor progressively reduces combustion near
4800 RPM. Shift multiplies available torque by 1.25 and unlocks an RPM reserve
up to 7000 RPM. This provides acceleration even after reaching the normal RPM
range. Wheels can back-drive the engine above the requested combustion RPM,
within its physical 7000 RPM limit. The HUD shows “Turbo : actif” while
Shift + Z is requested. A short boost can produce a wheelie; holding it can
flip the truck.

Every wheel torque produces an
opposite chassis reaction. Front braking reaches 1000 N·m per wheel. With Shift, service braking
acts on all four wheels: 1250 N·m at the front and 937.5 N·m at the rear. The
rear handbrake reaches 2200 N·m. An opposite-direction
request first brakes with the clutch open, then engages reverse after slowing
down. The physical engine keeps running while braking.

On the ground, braking follows chassis travel. In flight, it follows wheel
rotation direction so the pedals retain their meaning throughout a flip. The
opposite pedal brakes the wheels before driving them the other way; Space
retains rear braking to control rotation in the air.

The four SixDOF suspensions provide ±80 cm of travel, 1800 N/m springs and
300 N·s/m damping. The assembly retains its low centre of mass. Steering
remains available at speed with a 0.35 rad minimum; coupled rear steering
is −65% of the front angle.

Simulation runs at 120 Hz, with eight coupling steps at 960 Hz and one soft
substep per coupling; the rigid solver uses eight velocity iterations.
Terrain facets are solids with adjoining top surfaces. Physics and rendering
use the same list of volumes.

Tread lugs follow deformed vertices; collision uses vertex spheres.
Self-collision and soft/soft contacts are unavailable.

## Verify

These commands exit before creating the graphical application:

```sh
Build/MonsterTruck-Drive-Response --check
Build/MonsterTruck-Drive-Response --scene-check
Build/MonsterTruck-Drive-Response --arena-check
Build/MonsterTruck-Drive-Response --slope-check
Build/MonsterTruck-Drive-Response --ramp-check
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/DriveChecks.sx --release -o Build/MonsterTruck-Drive-Checks
Build/MonsterTruck-Drive-Checks
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/AirborneChecks.sx --release -o Build/MonsterTruck-Airborne-Checks
Build/MonsterTruck-Airborne-Checks
```

They cover physics, inflation, centering, short stunt inputs, controls, HUD,
terrain seams and slow driving on actual approach facets. `DriveChecks` also
compares acceleration with the former drive, rolling boost, a recoverable wheelie
and both final-drive extremes. `AirborneChecks` covers vehicle attitudes, ground
and airborne pedals, and complete aerial rotations. States are compared with
one and four workers.

`--single` selects one worker for playing. `--profile` opens a twelve-second
automated drive; `--profile-slope` opens a six-second test with brakes held
on a ramp. The title and HUD identify these measurements. Windowless timings
do not establish graphical FPS. `--profile-ramp` opens a twelve-second slow,
oblique climb followed by braking on the slope. `--ramp-check` checks eight
approaches without a window, including bead retention and ground clearance.

## Reusable Chevrolet sound

The source is `GFX.Audio.Engines.Library.driven_engine("454")`; the demo copies
no acoustic calculation. It supplies RPM and effort through `OperatingState`
and consumes ready blocks without waiting in the physics loop. Playback holds
at most five queued blocks and four native requests, about 98 ms excluding the
device. R also resets sound.

Sound receives `engine_rpm` and normalized combustion torque from the physical
engine. It follows shifts, clutch engagement and airborne wheels without a
second gearbox simulation. GFX.Audio remains independent of GFX.Physics:
`Library.engine` provides standalone operation with an optional transmission;
`Library.driven_engine` accepts RPM, load and ignition supplied by any game or
simulation. The truck’s configuration is not imposed on these other uses.

Offline integration check without a window or audio device:

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/TransmissionChecks.sx --release -o Build/MonsterTruck-Transmission-Checks
Build/MonsterTruck-Transmission-Checks /absolute/path/to/EngineLibrary
```

It checks all three gears, braking then reverse, adjustment restrictions, tire
stability, RPM/load correlation, PCM production and reset, plus identical
physics trajectories with and without reading audio inputs. `--scene-check`
also checks mouse buttons, Space after focus, and retaining gearing after R.
Interactive listening and graphical performance still require checks on the
machine used.
