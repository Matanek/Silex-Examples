# Drive two tracks

Six maneuvers show how two tracks of suspended wheels move and turn a chassis.
The wheels keep their steering axes; relative track speeds create curves and
opposing rotation produces a pivot. Colored spokes read each physical wheel's
rotation: blue on the left, orange on the right. Green markers indicate current
supports. The panel reports actual track velocities and driving phases.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release
```

- **Z**: forward; **S**: reverse.
- **← / →**: left / right curve.
- **P**: pivot with opposing track rotation.
- **G**: forward with zero grip; wheels spin while the chassis stays in place.
- **R**: recreate and replay the current choice.
- **Space**: pause/resume; **Escape**: quit.

Buttons perform the same actions. Each choice recreates the vehicle at the
start and runs eight seconds: two seconds of braked landing, two seconds at
80% throttle, then four seconds of braking and recovery. It stops afterwards
for comparison; R replays it. The camera follows the chassis; grid spacing is
one meter and the white marker stays fixed.

This is an interactive validation scene using qualified Jolt/Silex recipes:
100 kg, six 30 cm wheels, 10000 N/m springs and 1000 N·s/m dampers, two tracks
of 2 kg·m² inertia, a 15 N·m engine, ±1 gears and differential ratio 6. The scene
steps at 120 Hz; the same recipes are checked at 60 Hz. Tracks are an ideal
mechanical coupling, without links or continuous track collision geometry.
Six wheel rays contact a plane; this is not yet an all-terrain test.

## Headless checks

```sh
silex test Silex-Examples/Sources/Physics3D/TrackedDriving/Model.sx --nocache
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --controls-check
```

`--oracle-check` emits all 8,652 states from six recipes at 60/120 Hz in the
qualification witness format, checking that rendering consumes the same
simulation. `--smoke` opens a “TEST AUTOMATIQUE” window, runs all six recipes,
checks framing and transforms, then exits with its final marker. Closing it
early does not pass that check.
