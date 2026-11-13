# Soft-tire monster truck

[Français](README.fr.md)

Drive a pickup with four deformable tires on a 144 × 184 m dirt course.
Jump tables, plateaus, a bowl and small rollers are sculpted into the ground.
Open lanes between the mounds leave room to choose an approach and build
speed. The pickup has cutaway fenders, an exposed tube frame and a steel
skid plate under the transmission. Packed dirt and gravel cover the course.
On dirt, the tires leave a dust trail and a gravel sound. Wheel slip raises a
denser cloud. Landing on dirt throws up a burst around the wheels and plays
a low impact sound.

## Launch and drive

From the workspace root containing `Silex-Examples/`:

```sh
silex run Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx
```

The render loop is paced at 120 Hz, matching the physics simulation. The
16 m wide quarter-pipe is beyond the bowl, near the edge of the arena. An
arrow marks its approach.
Its lip turns slightly back toward the ramp. Adjust your approach speed and
use the brake in the air to set up the landing.

The two steel rails are at the far left. Center the truck on the arrow and
keep the wheels on the approach berms. The skid plate takes over in the middle.
The rail nearer the small rollers climbs. The one nearer the arena edge descends.

The Chevrolet 454 from [AudioEngineSimulator](../../AudioEngineSimulator/README.md)
is enabled by default. The demo embeds the simulator and its resources on
macOS ARM64. A row of shortcuts appears at the bottom of the view. Press **H**
to show or hide the settings and telemetry panel.

To use a custom library, compile and supply its absolute path. Pass application
options to the compiled binary:

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release -o Build/MonsterTruck-Drive-Response
Build/MonsterTruck-Drive-Response --engine-library /absolute/path/to/EngineLibrary
```

This customization requires a complete v3 native library compatible with
`AudioEngineSimulator.Engines`. An invalid path remains an explicit error. `--silent`
intentionally disables sound; omitting a custom library never disables it.
The embedded standard engine also works from another current directory,
without access to the example sources.

| Control | Action |
| --- | --- |
| Hold Z | Progressive normal acceleration |
| Shift + Z | Turbo: 25% more torque and a sharper response |
| Hold S | Reverse torque, both on the ground and in flight |
| Hold ↑ | Independent front brake |
| Hold ↓ | Independent rear brake |
| Q / D | Coupled four-wheel steering by default, left / right from the rear camera |
| A / E or ← / → | Rear steering in the desired direction of the nose |
| T | Couple / separate the steering axles |
| Hold Space | Four-wheel service brake |
| P | Monster / Low / Firm inflation without restarting |
| H | Show or hide settings and telemetry |
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
A lane along the western mounds leads to the slide rails.

For a wheelie, briefly press Shift + Z, then release. To lift the rear,
build speed and briefly press Space. Torque and braking physically pitch the
vehicle: time the inputs to recover its balance. Then compare the same
obstacle with all three inflation settings.

## Physical assembly

Each tire is 2.20 m in diameter and 1.32 m wide, with a 1.32 m rim and
1.56 m flanges. It has 192 vertices, 384 triangles and 96 internal shear
diagonals. Reinforced bead seats (480,000 N/m, damping 250 N·s/m) retain the
tires on their rims during powered landings. The 48 bead links exchange impulses
with the rim; vertices remain dynamic.

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
within its physical 7000 RPM limit. The telemetry panel shows “Turbo : actif” while
Shift + Z is requested. A short boost can produce a wheelie; holding it can
flip the truck.

Every wheel torque produces an
opposite chassis reaction. Up brakes only the front wheels, up to
1000 N·m per wheel. Space applies the four-wheel service brake: 1250 N·m
at the front and 937.5 N·m at the rear. Down brakes only the rear wheels,
up to 2200 N·m per wheel.

Z and S send the new torque direction on the next simulation step, both on the
ground and in flight. The gearbox engages through a 25 ms clutch take-up without
a gear-change dead time. Opposing torque slows and reverses wheel rotation;
the command does not wait for the truck to stop or add an automatic brake.

Chassis travel direction reduces neither clutch pressure nor the permitted
engine RPM. Wheels can therefore spin in the requested direction while the
truck still slides the other way. Clutch capacity is 450 N·m on the engine
side, before gearbox and final-drive multiplication; it bounds physical torque
in both directions independently of truck speed. Launch engagement depends on
engine RPM and wheel rotation, but never drops below pedal demand: crossing
zero does not disengage a motor that is still being commanded. The opposite
chassis reaction enables pitch changes and stunts; the player controls them
by metering the inputs.

When Z and S are held together, the last distinct press wins; keyboard repeat
does not change that priority. Releasing that key restores the other pedal if
it remains held. In flight this directly controls wheel angular momentum and
its reaction on truck pitch, including during a flip.

The three brake commands are independent of Z/S and take priority over drive.
Releasing them restores the held motor command; focus loss releases them all.
Shift remains boost and never turns S into a brake. Up and Down brake their
respective axles in flight; Space brakes all four wheels.

The four SixDOF suspensions provide ±80 cm of travel, 1800 N/m springs and
300 N·s/m damping. The assembly retains its low centre of mass. Steering
remains available at speed with a 0.35 rad minimum; coupled rear steering
is −65% of the front angle.

Simulation runs at 120 Hz, with eight coupling steps at 960 Hz and one soft
substep per coupling; the rigid solver uses eight velocity iterations.
Terrain rendering and collisions share a heightmap sampled at one-meter
intervals. The terrain is static. A compaction map reserves the ground under
and around the quarter-pipe, protects the rail footings, and distinguishes
packed mounds from loose soil for future deformation. The quarter-pipe also
shares its curved profile between rendering and collisions. The skid plate
aligns with the bottom face of the central chassis collider.

The visible tire deforms under load. The tread stays flat across its width,
and its beveled chevrons extend over shoulders that are 12 cm wider
per side than the physical profile. Matte black rubber with darker grooves
surrounds rims with a bare-metal lip, a recessed red center with ventilation
openings, and a dark hub. Collision uses physical vertex spheres.
Self-collision and soft/soft contacts are unavailable.

## Verify

The general `--check` includes the same sustained reversal checks as
`ReversalChecks.sx`; it does not constrain pitch during prolonged full torque.

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
terrain seams and slow driving on dirt slopes. `DriveChecks` also
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

`--profile-drive`, `--profile-boost` and `--profile-turn` retain the twelve-second
run with, respectively, full throttle, boost, and full throttle followed by a
turn on the table. The HUD describes the scenario actually running. Sound
remains enabled unless `--silent` is supplied. Add `--profile-long` to extend
the scenario to 36 seconds; the slope test remains fixed at six seconds.

`--trace-performance` retains free driving and the interactive HUD. Every half
second the terminal reports FPS, sector, position, the number of wheels above
a slope, mean physics time per 1/120 s step, and maximum update cost. Cumulative
physics and simulated time help distinguish simulation overload from the rest
of the frame. `focused` reports focus at the latest update; `focus_changed`
marks a transition during the measured interval. Exclude transition intervals
when comparing foreground and background performance. `--ledge` places the
truck on the table's side slope, rear wheels on the mound and front
wheels towards the ground; controls remain available.
`--bumps` starts on the small rollers. `--profile-bumps` holds the brakes
there for twelve seconds, with a measurement HUD and automatic shutdown.
`ModuleCostChecks.sx` compares flat ground, small rollers, central ramps, a
side mound, and the table edge without a window: computation per simulated
second, maximum step cost, and physical state. It does not measure rendering FPS.
These measurements are optional; ordinary launches emit no trace.
Compare binaries separately, without concurrent builds or tests, in the same
mode and on the same course.

`--trace-stutter path.csv` records recent frames during free driving. Press
**M** when the scenery starts stuttering, keep driving for about two seconds,
then quit with **Escape**. The window title confirms the mark. The path must
name a new file. On exit, the demo writes application-side frame times,
physics steps, the chassis pose, and the camera position around the mark.
Add `--quit-after-mark` to exit two seconds after pressing M, aligning the
end of an external recording with the trace.

## Reusable Chevrolet sound

The `AudioEngineSimulator.Engines` module supplies the Chevrolet 454 through
`Library.driven_engine("454")`. MonsterTruck passes `engine_rpm` and normalized
combustion torque through `OperatingState`. Sound follows the RPM produced by
shifts, the clutch and the wheels. The physics loop consumes ready blocks.
Playback holds up to ten queued blocks and four native requests. The gravel
loop is synthesized at startup, and its volume follows tire speed and slip
on loose dirt. R resets the sound and particles.

Offline integration check without a window or audio device:

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/TransmissionChecks.sx --release -o Build/MonsterTruck-Transmission-Checks
Build/MonsterTruck-Transmission-Checks
```

It checks all three gears, direction reversal, adjustment restrictions, tire
stability, RPM/load correlation, PCM production and reset, plus identical
physics trajectories with and without reading audio inputs. `--scene-check`
also checks mouse buttons, Space after focus, and retaining gearing after R.
Interactive listening and graphical performance still require checks on the
machine used.

`ReversalChecks.sx` also checks both directions at 2 and 18 m/s, the extreme
final ratios at 12 m/s, cancellation of a reversal and torque on the first step.
It requires all four wheels to rotate in the new direction for at least 150 ms,
before the chassis loses half its initial speed (at 12 and 18 m/s). Tire beads
remain seated and tires stay above the ground; pitch remains free to react to
torque:

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/ReversalChecks.sx --release -o Build/MonsterTruck-Reversal-Checks
Build/MonsterTruck-Reversal-Checks
```

`BrakeChecks.sx` verifies Space/Up/Down routing, release and focus loss, physical
braking of each axle, a four-wheel stop with held throttle and resumed drive
after brake release.

`DirectionChecks.sx` also checks opposing torque on the first step, free-wheel
reversal and pitch reaction in both directions, under four attitudes and with
final drive ratios 6, 8 and 12. It also verifies 100 ms pedal alternation for
airborne angular momentum control:

```sh
silex run Silex-Examples/Sources/Physics3D/MonsterTruck/DirectionChecks.sx --release
```

`BrakeChecks.sx` also covers last-pedal priority, overlapping presses, release
and keyboard repeat.
