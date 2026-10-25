# Observe a moving support's reaction

Three experiments advance together: a 1000 kg platform, a 200 kg platform,
and a kinematic platform with prescribed velocity. Selecting a view preserves
all three simulations. The panel compares their speeds; the grid stays in
world space.

From the workspace root or Spec Worktree group root:

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release
```

- **1 / 2 / 3**: view 1000 kg, 200 kg or the kinematic support.
- **Z / S**: apply an impulse along +Z / −Z. Dynamic supports receive
  ±2M N·s; the kinematic support receives a prescribed velocity change of
  ±2 m/s. Clicking acts immediately, without a reset.
- **G**: lock/release all three vehicles' track brakes.
- **P**: pause/resume. **R alone**: explicitly return to the start. **Escape**: quit.

Wait for the vehicles to settle, then push along +Z. With locked tracks, the
kinematic support stays at 2 m/s. The 1000 kg support and its vehicle converge
to 1.82 m/s; the 200 kg pair to 1.33 m/s. The difference comes from the vehicle's
reaction: a finite-mass platform slows as it carries the vehicle.
An opposite impulse returns total horizontal momentum to zero.

To compare free tracks, reset with R, release G, then push. Wheels rotate and
the vehicle moves slower than its support. The engine stays in neutral without
throttle. Suspension, rotation and position come from the solver, without
prescribed chassis animation.

The platform measures 8 × 0.4 × 12 m and rests on a frictionless plane. The
vehicle uses the other tracked examples' 100 kg, six-ray profile. Dynamic
worlds use 48 velocity iterations; the kinematic world keeps the default 12.
This test illustrates reciprocal reaction and relative rolling; repeated
impulses, leaving the platform, rotating supports and general driving are not
qualified by its fixed witness.

## Verify

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --controls-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --witness
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --smoke
```

The witness reproduces the six standalone `TrackedDynamicPlatformRun.py`
cases in Silex-Benchmarks at 60/120 Hz. The controls test uses actual clicks,
preserves identities and clocks, and distinguishes impulse, view selection,
braking, pause and return to start. The native smoke closes when finished.

## Observe carrying by a rotating support

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation
```

Three kinematic supports with fixed pivots compare opposite rotations and a
stationary control. The vehicle starts one metre from the red pivot; wheel
contacts determine its position and orientation. The world grid stays fixed.
The panel shows vehicle/support angular velocities around Y.

- **1 / 2 / 3**: +Y rotation, −Y rotation or stationary support.
- **Z / Lancer**: set the moving supports to +0.25 / −0.25 rad/s.
- **S / Arrêter**: stop the supports without moving the vehicles.
- **G**: lock/free the tracks; **P**: pause; **R only**: return to the start.

Wait for settling, launch with locked tracks, then compare opposite rotations.
The support carries the vehicle through its contacts. Stop with S, restart
with R, release G and launch again: tracks roll and relative motion becomes
visible. All three worlds advance together; selecting a view preserves their
state. Repeated launch actions set the same velocity without accumulating it.

The fixed witness covers four six-second cases at 60/120 Hz: stationary,
opposite braked rotations and +Y rotation with free tracks. Rotation runs from
2 to 4 seconds, followed by stopping. The scene's 4328 states match the
`TrackedRotatingPlatformRun.py` benchmark qualified against Jolt. This mode
retains 12 velocity iterations. Finite-mass dynamic rotation and general driving
on moving terrain remain outside this qualification.

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation-controls-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation-physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation-witness
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation-smoke
```
