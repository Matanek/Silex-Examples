# Drive two tracks over a finite ramp

Eight maneuvers show how two tracks of suspended wheels move and turn a chassis.
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
- **B**: finite ramp; **F**: flat control with the same inputs.
- **R**: recreate and replay the current choice.
- **Space**: pause/resume; **Escape**: quit.

The scene starts on the ramp. B and F recreate the vehicle and run fourteen
seconds: two seconds of settling, five seconds at 80% throttle, then seven
seconds of moderate 4% braking. On the ramp, watch the green supports disappear
at the top, the chassis continue in flight, then all six wheels recover their
loads after landing. The phase and support counter follow those physical states.

Buttons perform the same actions. The original six maneuvers (Z/S/arrows/P/G)
remain eight-second sequences: two seconds of braked landing, two seconds at
80% throttle, then four seconds of braking and recovery. It stops afterwards
for comparison; R replays it. The camera follows the chassis; grid spacing is
one meter and the white marker stays fixed.

This is an interactive validation scene using qualified Jolt/Silex recipes:
100 kg, six 30 cm wheels, 10000 N/m springs and 1000 N·s/m dampers, two tracks
of 2 kg·m² inertia, a 15 N·m engine, ±1 gears and differential ratio 6. The scene
steps at 120 Hz; the same recipes are checked at 60 Hz. Tracks are an ideal
mechanical coupling, without links or continuous track collision geometry.
Six wheel rays contact the plane and the top of an 8 × 0.4 × 6.03 m ramp tilted
by 0.1 rad. The mechanical profile is unchanged. Moderate braking isolates the
obstacle: full braking from about 58 km/h overturns the Jolt reference at 120 Hz.
This recipe qualifies neither that extreme braking nor general terrain or
automatic shifting on the ground.

## Headless checks

```sh
silex test Silex-Examples/Sources/Physics3D/TrackedDriving/Model.sx --nocache
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --controls-check
```

`--oracle-check` emits all 8,652 states from six recipes at 60/120 Hz in the
qualification witness format, checking that rendering consumes the same
simulation. `--ramp-check` emits all 5,044 flat/ramp states, identical to the
`TrackedRamp.sx` benchmark. `--smoke` opens a “TEST AUTOMATIQUE” window, runs all eight recipes,
checks framing and transforms, then exits with its final marker. Closing it
early does not pass that check.
