# Uphill driving, braking and sliding

This demo places a 100 kg car on an 11.5° slope. Wait for it to land, then
press **Z**: the engine drives all four wheels uphill. **F** releases throttle
and applies all brakes; the car slows down and holds its position. **X**
releases both throttle and brakes. These commands remain selected after the
key is released.

**G** recreates the car without tire grip. Suspension still supports the
chassis, but the car slides downhill even with the brakes applied. Z spins the
wheels without stopping that slide. Press G again to compare with grip enabled.
The button always shows the current choice.

From the workspace root or the Spec group root containing this example:

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleHill/Main.sx --release
```

## Controls

| Key | Action |
| --- | --- |
| Z | Select 80% uphill throttle and release brakes. |
| X | Coast: release throttle and brakes. |
| F | Release throttle and apply all four brakes. |
| G | Toggle tire grip and recreate. |
| I | Reverse the slope and gearbox direction to climb the opposite grade. |
| M | Compare soft and firm suspension. |
| T | Cycle 40 cm cylinder, ray, sphere, then cylinder contacts. |
| R | Recreate at the starting point with brakes applied. |
| Space | Pause or resume simulation. |
| Escape | Close the window. |

The buttons perform the same actions. G, I, M, T and R recreate the vehicle and
floor, preserve other choices, apply brakes and resume simulation. Wait for
landing before pressing Z. Driving commands also resume a paused simulation.
Repeated key events are ignored.

The yellow strip marks the front. I selects reverse gear to climb the opposite
slope; positive telemetry still means uphill. The following camera and metric
grid reveal displacement. Cyan bars show physical wheel rotation, white bars
follow suspension lengths and green pads indicate support. Telemetry reports
speed, progress from the origin, supports, forces, normal ride height, engine
RPM and gear.

## Setup and scope

Soft suspension and 40 cm cylindrical wheel contacts are initially selected.
Each wheel has a 30 cm radius. Rays search along their center axes; sphere
searches use a 30 cm radius. Soft springs use 1,200 N/m and 160 N·s/m per wheel,
firm springs 10,000 N/m and 1,000 N·s/m. Their respective maximum lengths of
77.985 and 60 cm compensate for their different static compression.

A 40 N·m engine drives all four wheels through a manual +1/−1 gearbox and two
differentials with ratio 3, each receiving half the torque. Tires use a constant
friction coefficient of 1 or 0, with no rolling resistance. This bounds the
Coulomb comparison against Jolt; it does not qualify variable curves, other
terrain or a complete driving model. The physical plane and visible road have
the same normal. All poses and reactions come from simulation.

Simulation runs at 120 Hz. Rendering interpolates poses, suspension travel and
wheel angles. Shared meshes are created at startup; the grid moves in five-meter
increments. Telemetry refreshes on commands or at most at 10 Hz. Contact pads
come from the start of a physical step and may slightly differ from the
interpolated pose during landing.

[VehicleSuspension](../VehicleSuspension/README.md) remains available for turns,
anti-roll bars, obstacles and overturning.

## Checks

From the same root:

```sh
silex test Silex-Examples/Sources/Physics3D/VehicleHill/Model.sx
silex compile Silex-Examples/Sources/Physics3D/VehicleHill/Main.sx --release -o .silex/vehicle-hill
.silex/vehicle-hill --physics-check
.silex/vehicle-hill --controls-check
.silex/vehicle-hill --smoke
```

The physical check covers 48 configurations at 60/120 Hz: two slopes, three
contact detectors, two suspension setups and grip enabled/disabled. It checks
climbing, braking, supports, normal ride height and mean load, as well as sliding
under gravity. Recreation and stale handles are also checked. The headless
controls check exercises logical/uppercase/physical keys, repetition, actual
button clicks, pause and preserved choices.

The **TEST AUTOMATIQUE** run executes four eight-second physical passes: soft
with grip, soft without grip, the opposite slope with grip, then firm suspension.
It checks rendered chassis/wheel transforms, road alignment, framing, pause and
recreation. Wait for its normal exit. Interactive testing assesses how clearly
the slope, climb, braking and sliding can be felt and understood.
