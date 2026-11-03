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
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release -o Build/MonsterTruck-Chevrolet
Build/MonsterTruck-Chevrolet --engine-library /absolute/path/to/EngineLibrary
```

Chevrolet 454 sound is enabled by default. Without an option, the bank path is
`Build/EngineLibrary-Monster-Package`, relative to the current directory. An
explicit absolute path works from any directory. `--silent` retains driving
without opening an audio engine or device. The HUD displays acoustic RPM.
The interface and renderer retain their usual controls.

| Control | Action |
| --- | --- |
| Hold Z | Progressive normal acceleration |
| Shift + Z | Turbo: 25% more torque and a sharper response |
| Hold S | Front brake and immediate reverse request |
| Shift + S | Stronger front brake to lift the rear |
| Q / D | Front steering, left / right from the rear camera |
| A / E or ← / → | Rear steering in the desired direction of the nose |
| T | Couple / separate the steering axles |
| Hold Space | Rear handbrake |
| P | Monster / Low / Firm inflation without restarting |
| R | Restart with the selected inflation |
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

Motors supply up to 1250 N·m per wheel normally and 1562.5 N·m with Shift,
with opposite chassis reactions. Front brakes reach 1000 N·m per wheel, or 1250 N·m with Shift, and
the rear handbrake 2200 N·m. Reversal immediately requests opposite torque;
velocity physically passes through zero before moving backward.

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
Build/MonsterTruck-Chevrolet --check
Build/MonsterTruck-Chevrolet --scene-check
Build/MonsterTruck-Chevrolet --arena-check
Build/MonsterTruck-Chevrolet --slope-check
Build/MonsterTruck-Chevrolet --ramp-check
```

They cover physics, inflation, centering, short stunt inputs, controls, HUD,
terrain seams and slow driving on actual approach facets. States are compared
with one and four workers.

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

The driving model acts directly on rims; it has no crankshaft or gearbox.
The acoustic adapter therefore uses rim rotation relative to the chassis,
the 454 profile’s first gearing, and a simplified idle/launch slip model.
Effort comes from the difference between commanded and actual wheel speed.
This retains RPM in the air and in reverse, with less effort when wheels spin
freely. Brakes and the handbrake release acoustic effort. RPM is smoothed and
bounded by the profile scale. This sound connection changes no driving forces
and does not claim to add a physical transmission.

Offline integration check without a window or audio device:

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/EngineSoundChecks.sx --debug -o Build/MonsterTruck-Audio-Checks
Build/MonsterTruck-Audio-Checks /absolute/path/to/EngineLibrary
```

It covers RPM derivation, reverse, effort, brakes, airborne wheels, PCM and
reset, plus identical physics trajectories with and without reading audio
inputs. Interactive listening and graphical performance still require checks
on the machine used.
