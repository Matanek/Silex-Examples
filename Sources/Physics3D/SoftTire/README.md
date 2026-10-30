# Try a soft tire

A powered wheel rolls across a flat floor and climbs a small step. Its
deformable carcass supports a dynamic rim: increase the load to observe its
compression, then change inflation to explore its response.

From the `SilexProject/` root, using the workspace compiler and packages:

```sh
silex run Silex-Examples/Sources/Physics3D/SoftTire/Main.sx --release
```

Use Release for the interactive trial. Debug is intended for verification and
has a much higher simulation cost.

| Control | Action |
| --- | --- |
| Hold Z / S | Forward / reverse motor |
| Hold Space | Brake the rim |
| C | Switch rim load: 20 / 50 kg |
| P | Cycle inflation: normal / soft / firm |
| O | Enable or remove the step |
| R | Restart with the selected settings |
| Mouse | Orbit the camera and adjust its distance |
| Escape | Quit |

The compact HUD stays on the left and the camera follows the wheel. Yellow
markers on the rim and carcass help distinguish their rotation. Changing the
load, inflation or obstacle does not reset the wheel.

## What the rig demonstrates

The carcass is a closed torus with 192 vertices, stretch, shear and bending
constraints, inflated by pressure. Its contacts with the rim and floor
transfer forces in both directions. The motor applies torque only to the rim;
no tire translation is imposed.

The rim cannot collide directly with the floor or step. A mechanical guide
blocks sideways motion and tipping while leaving height, forward motion and
wheel rotation free. It supplies no vertical support. Without the carcass,
the rim falls through the floor: this negative control is part of verification.

Inflation uses solver coefficients 500, 1500 and 3000, rather than calibrated
pressures in bars. Rim mass is additional to carcass mass; this setting is not
the total mass of a vehicle.

## Verify without a window

Compile from the same root, then pass options to the executable:

```sh
silex compile Silex-Examples/Sources/Physics3D/SoftTire/Main.sx --backend native --release -o /private/tmp/silex-soft-tire-demo
/private/tmp/silex-soft-tire-demo --check
```

`--check` verifies support, load, inflation, guidance without vertical support,
torque transfer and climbing, followed by controls, explicit wheel replacement
and HUD bounds. It creates no window. `--controls-check` runs only the latter
part; `--bench` measures one simulated second without rendering. `--smoke`
opens a test window, drives the wheel and closes after five simulated seconds.

This experimental prototype qualifies one guided wheel against rigid bodies.
A full monster truck still needs wheel integration and qualification for its
intended loads, turns and speeds. Soft/soft contacts and self-collision remain unimplemented.
