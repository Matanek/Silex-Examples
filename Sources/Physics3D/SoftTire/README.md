# Try a soft tire

A powered wheel rolls across a flat floor and climbs a small step. Its
deformable carcass is retained on a dynamic rim by two rows of elastic bead
links. Low initial inflation and flexible sidewalls emphasize compression;
increase the load or change inflation to alter its actual physical response.

From the `SilexProject/` root, using the workspace compiler and packages:

```sh
silex run Silex-Examples/Sources/Physics3D/SoftTire/Main.sx --backend native --release
```

Use Release for the interactive trial. Debug is intended for verification and
has a much higher simulation cost.

| Control | Action |
| --- | --- |
| Hold Z / S | Forward / reverse motor |
| Hold Space | Brake the rim |
| C | Switch rim load: 20 / 50 kg |
| P | Cycle inflation: cross / very low / firm |
| O | Enable or remove the step |
| R | Restart with the selected settings |
| Mouse | Orbit the camera and adjust its distance |
| Escape | Quit |

The compact HUD stays on the left and displays measured FPS; the camera follows
the wheel. Yellow
markers on the rim and carcass help distinguish their rotation. Changing the
load, inflation or obstacle does not reset the wheel.

## What the rig demonstrates

The carcass is a closed torus with 192 vertices, stretch, shear and bending
constraints, inflated by pressure. Its 48 bead links exchange equal and
opposite impulses with the rim at the same point. Every vertex remains dynamic;
no kinematic attachment or teleport holds it in place. Contacts and links
transfer forces in both directions. The motor applies torque only to the rim;
no tire translation is imposed.

The rim cannot collide directly with the floor or step. A mechanical guide
blocks sideways motion and tipping while leaving height, forward motion and
wheel rotation free. It supplies no vertical support. Without the carcass,
the rim falls through the floor: this negative control is part of verification.
A second control without bead links unseats under lateral force, while the
linked tire stays retained. The controller runs at 120 Hz, with four coupling
steps containing two soft substeps each: the total remains eight soft substeps
per controller step.

The cross profile starts at 150; P switches to 50 (very low), then 1500 (firm).
These are solver coefficients rather than calibrated pressures in bars. Rim
mass is additional to carcass mass; this setting is not the total mass of a
vehicle.

## Verify without a window

Compile from the same root, then pass options to the executable:

```sh
silex compile Silex-Examples/Sources/Physics3D/SoftTire/Main.sx --backend native --release -o /private/tmp/silex-soft-tire-demo
/private/tmp/silex-soft-tire-demo --check
```

`--check` verifies support, load, inflation, guidance without vertical support,
torque transfer and climbing, followed by controls, explicit wheel replacement
and HUD bounds. Sustained driving combines twenty seconds of motor input,
braking, reverse, inflation and load changes, checking bead retention and
obstacle clearance. It creates no window. `--controls-check` verifies only
controls, reset, mesh updates and HUD bounds; `--bench` measures one simulated
second without rendering. `--smoke`
opens a test window, drives the wheel and closes after five simulated seconds.
`--profile` opens a twelve-second automated window and reports average FPS,
longest frame interval and time spent stepping physics. `--fleet-bench` measures
four complete tires in independent worlds without a window. It excludes
rendering and a shared chassis, so it does not measure monster-truck FPS.
`--profile-four` runs four independent physical tires in the graphical process,
with one tire displayed, to measure simulation scaling in that context. It does
not measure rendering four tires or a complete shared vehicle.


This experimental prototype qualifies one guided wheel against rigid bodies.
A full monster truck still needs wheel integration and qualification for its
intended loads, turns and speeds. Soft/soft contacts and self-collision remain unimplemented.
