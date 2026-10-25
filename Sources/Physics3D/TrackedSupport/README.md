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
