# Soft-tire monster truck

[Français](README.fr.md)

This demonstration combines a raised pickup, four deformable flat-tread tires and
physical suspension in one world. The course includes bumps, blocks of different
heights, steps and two ramps.

Use Release for interactive trials.

## Run the demo

From the workspace root containing `Silex-Examples/`, with the local packages linked
to that workspace:

```sh
silex run Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release
```

This compiles and opens an interactive window. To prepare a binary without opening a
window:

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release -o /private/tmp/silex-monster-truck-demo
```

After compilation, run `/private/tmp/silex-monster-truck-demo` without options to
play. This absolute path works from any directory.

| Control | Action |
| --- | --- |
| Hold Z | Accelerate; reverse torque when moving backward |
| Hold S | Apply the front brake and immediately request reverse |
| Hold Q / D | Front wheels, left / right from the rear camera |
| Hold A / E or ← / → | Rear wheels, overriding coupled steering |
| T | Couple / separate the two steering axles |
| Hold Space | Rear-wheel handbrake |
| Shift + Z | Boost |
| P | Inflation: monster / low / firm, without restarting |
| R | Restart with the selected inflation |
| Mouse wheel | Adjust chase-camera distance |
| Escape | Quit |

Both axles are coupled initially. Press T to control them independently: Q/D for the
front, A/E or arrow keys for the rear. Rear inputs also override the coupling while
coupled mode is active. Steering both axles the same way enables crab motion;
opposite steering tightens a turn. Rear inputs orient the wheels: steering only the
rear pair left while driving forward turns the nose to the right.

The left HUD identifies the current section. Yellow arrows indicate course
direction; checkered markings identify the start and landing area. Bumps are cyan,
blocks orange, ramps red and tall steps purple.

For a first trial, drive straight ahead over the first bump and two staggered
obstacles, followed by the 30, 50 and 70 cm blocks. Continue toward the ramp and
landing area. Then try the taller steps and alternating bumps in the two side areas.
Finally, compare the same obstacle with all three inflation settings without
restarting the vehicle.

## Physical assembly and limits

Each tire is 2.20 m in diameter and 1.32 m wide, with a 1.32 m rim diameter and 1.56
m flanges. It has 192 vertices and 384 triangles. Its sidewalls and 96 internal
shear diagonals resist lateral shear while allowing ground-contact compression. Its
cross-section has a flat tread and nearly upright sidewalls. The 48 bead links from
the `SoftTire` prototype exchange impulses with the rim; no vertex is artificially
fixed to it. Four SixDOF suspensions connect dynamic rims to the dynamic chassis
without a fixed support or vertical guide. Motors apply up to 1250 N·m per wheel
with an opposite chassis reaction. In coupled mode, rear steering is −65% of front
steering; the angle decreases progressively with speed to a 20° minimum. S brakes
the front pair at 1000 N·m per wheel and engages reverse torque at the rear during
deceleration; Space locks the rear pair at 2200 N·m per wheel. Velocity physically
passes through zero before the truck moves backward. Bead attachments are sized for
the increased torque. The chassis center of mass represents a low, slightly forward
engine/transmission assembly, with a progressive torque response proportional to
input magnitude. Suspensions provide ±80 cm of travel with 1800 N/m springs and 300
N·s/m damping. Rims have a barrel and two collision flanges that protect the beads.
Controls run at 120 Hz, with eight coupling steps at 960 Hz and one soft substep per
coupling. The rigid solver profile uses eight velocity iterations.

Pressures 700, 250 and 1000 are solver coefficients, not calibrated bar values. The
wheelbase is 4.10 m. The chassis weighs 150 kg, each rim 20 kg and each carcass 9.6
kg. Visible tread lugs follow deformed vertices; collision uses the vertex collision
spheres. Self-collision and soft/soft contacts are unavailable.

## Windowless checks

After compiling the binary:

```sh
/private/tmp/silex-monster-truck-demo --check
/private/tmp/silex-monster-truck-demo --scene-check
```

Both modes exit before creating the graphical application. The first exercises rest,
inflation, driving, steering, braking, obstacle traversal and one/four-worker
comparison, plus tire centering under alternating rear steering, motor reversal and
suspension travel after a reference impact. The second checks controls, reset,
meshes, HUD bounds and camera projection without capturing images.

`--single` selects one worker for interactive trials. `--profile` opens an automated
twelve-second window and measures frames; it is separate from playing. Windowless
timings do not establish the truck's graphical FPS.