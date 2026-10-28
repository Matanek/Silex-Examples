# Drive an RC car or a monster truck

The car starts with strong acceleration, four-wheel drive, soft suspension,
sphere sweeps and solid tire sides. A 280 × 360 pixel panel uses natural text
heights and stays on the left, leaving the vehicle and terrain visible. Grid
spacing is one meter; the camera follows movement and can still be orbited
with the mouse.

From the `SilexProject` workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

## Driving

- Hold **Z** to accelerate; release to coast.
- Hold **S** to brake, then reverse after slowing down. While reversing, Z
  brakes before accelerating forward again.
- Hold **Q / D** to steer left/right relative to the vehicle. Steering recenters
  on release and decreases with speed. Letters follow logical keyboard input
  (ZQSD on AZERTY).
- Hold **Space** to lock the rear wheels. During a turn, tire forces let the rear
  slide; release to regain drive. Front wheels remain driven while Z is held.
- **R** restarts with the chosen profile and releases controls.
- **Escape** exits. Losing focus releases held controls; Space no longer pauses
  the simulation.

## Profiles and terrain

**N** switches between the RC car and monster truck. Physical wheel radius
changes from 32 to 65 cm; track width, rotational inertia and suspension travel
also change. Rendered wheels use these actual dimensions. Mass stays at 100 kg,
with continuous chassis collision enabled and a low center of mass so ordinary
braking does not consistently overturn the vehicle. A 180 Nm engine drives two
differentials and three automatic forward gears with short shifts. The RC
profile reaches about 33–34 km/h after one second of acceleration in the
60/120 Hz checks; the monster reaches about 39–40. These playful settings do
not represent a calibrated real vehicle.

Eight fixed obstacles form the course: a small ramp ahead, a taller ramp farther
along, a lateral incline, three steps on the opposite side, a low crossbar and a
steeper ramp. Rendering uses the physical obstacle shapes and poses. Checks
cover monster step traversal, airborne motion and regaining support on the ramp
course. Excessive maneuvers can overturn the vehicle; R restarts it.

Panel buttons and keyboard shortcuts also compare:

- **M**: soft/firm suspension.
- **T**: sphere, wide cylinder, narrow cylinder, ray, then sphere contacts.
- **A**: anti-roll bars.
- **L**: a 60° total tilt limit or unrestricted mode.

These changes recreate the vehicle at the start and release controls; terrain
stays in place. **O** applies a toppling impulse, **B** jumps and **C** applies
a two-second overload. **G** remains a diagnostic shortcut to disable/restore
grip by recreating the vehicle. The engine imposes no chassis pose, velocity or
slide angle. A 4000 Nm rear handbrake per wheel and combined tire friction
actually share the longitudinal/lateral force budget.

The wheel sides hit the floor during rollover using their actual width, even
when suspension support is unavailable. This side envelope stays active with
each of the four sweep modes. When overturned, wheels extend without catching fictitious floor support.
The chassis rests on its own collision shape; a package regression covers the
cylinder-contact compression/extension alternation.

## Checks without a window

```sh
silex test Silex-Examples/Sources/Physics3D/VehicleSuspension/DrivingChecks.sx
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/DrivingChecks.sx --release
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release -- --controls-check
```

Checks cover acceleration, braking before reversing, rear locking and mirrored
slides, large physical wheels on obstacles, jumps/landings, inverted wheels,
held/released inputs, focus, repetition, buttons, rendered dimensions and HUD
bounds and the actual text height after visible actions. Historical physical
witnesses remain available through `--physics-check`
with their original configurations. `--smoke` is an automatic graphical test
that opens a window and closes when complete; it remains separate from the
interactive playground.
