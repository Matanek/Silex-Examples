# Drive two tracks over a finite ramp

Drive continuously, change terrain in place and observe all six suspensions.
Blue spokes on the left and orange spokes on the right follow physical wheel
rotation; green markers show current supports.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release
```

- Hold **Z / S**: forward / reverse. Changing direction brakes before shifting;
  it does not move the vehicle back to the start.
- Hold **Q / D**, or **← / →**: turn. At very low speed without throttle, tracks
  counter-rotate to pivot.
- Hold **Space**: brake. Releasing throttle allows coasting; light braking holds
  the vehicle when nearly stationary.
- **B / F**: add the ramp / return to the flat plane, retaining the vehicle,
  pose, velocity and simulation clock. Removing a support can naturally let
  the vehicle fall.
- **M**: enable or disable one automatic cycle from the current state.
  A driving input immediately takes over.
- **P**: pause/resume; **R**: the only reset, retaining the selected terrain;
  **Escape**: quit.

Five buttons control terrain, automatic driving, pause and reset. Driving uses
held keys. Releases and focus loss clear controls without recreating the vehicle.
B/F and M retain pause; R resumes. Free driving continues beyond fourteen
seconds. Inputs never impose chassis poses or wheel rotation.

The scene starts at the foot of the ramp. To compare the qualified course,
enable M then explicitly press R to start over: settling for 2 s, 80% throttle
for 5 s, and moderate 4% braking for 7 s. The cycle never resets itself.
Hold a ZQSD key to drive manually. Manual driving modulates throttle and track
speed differences with vehicle speed, retaining the engine and suspensions.

The camera follows the chassis; grid spacing is one meter. The panel reports
track velocities, driving mode and supports. Watch ascent, supports disappearing
at the top, flight and recovery after landing.

The model uses 100 kg, six 30 cm wheels, 10000 N/m springs, 1000 N·s/m dampers,
two tracks of 2 kg·m² inertia and a 15 N·m engine. Tracks are an ideal coupling
without articulated links. Six rays contact the plane or an 8 × 0.4 × 6.03 m
box tilted by 0.1 rad. Moderate braking isolates the obstacle: full braking
from about 58 km/h overturns Jolt at 120 Hz. That extreme braking, general
terrain and automatic shifting on the ground are not qualified here.

## Headless checks

```sh
silex test Silex-Examples/Sources/Physics3D/TrackedDriving/Model.sx --nocache
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --controls-check
```

`--controls-check` retains identity, pose, velocity, rotors and clock across
commands, then checks held-key driving, braking, reverse, buttons and pause.
R is checked as a separate recreation. `--oracle-check` emits all 8,652 historical
states; `--ramp-check` emits the 5,044 flat/ramp states. Both retain the qualified
witness simulation. `--smoke` runs those eight recipes in a “TEST AUTOMATIQUE”
window and checks framing, wheels/supports, ramp, pause and recreation before
closing. Closing it early does not validate that check.

`--live-smoke` checks held-key driving, turns, braking, B/F in place, M and
manual takeover, pause and the uninterrupted clock beyond fourteen seconds
in a separate automatic window.
