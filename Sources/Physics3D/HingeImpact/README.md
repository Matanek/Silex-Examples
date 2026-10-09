# Observe the first hinge stop braking

From the `SilexProject/` root or the Spec `Worktree/` group:

```sh
silex run Silex-Examples/Sources/Physics3D/HingeImpact/Main.sx --release
```

The scene starts paused. Click **Vers le repère haut**, wait for the stop, then
**Vers le repère bas**. The red tip moves between the two green markers.
**Rotation libre** gives the body ±1 rad/s and leaves the axis unpowered.
**Avec moteur** selects a position drive; click a direction to approach the stop
and reverse. Selecting a mode pauses; a direction command resumes simulation.

Playback runs at ×0.25 with 120 Hz physics. The panel retains each command's
first braking speed before/after and its angle, then displays current state
and motor torque. Stops are ±0.3 rad (±17.2°). The motor requests ±0.8 rad,
effectively clamped to the stops, with 10 N·m, stiffness 1.6 and damping 0.08.
Positive rotation follows the right-hand rule; the buttons name the upper or
lower green marker in the initial view.

**Space** and Pause suspend/resume. **R** and Remettre à zéro recreate the scene
at the center in free mode and paused. **Escape** closes. Key repeats are ignored.
There are no hidden T, M or I commands.

Green markers visualize hinge limits, rather than contacts. The solver can
brake before the limit angle, according to the remaining distance over a step.
The checks cover impulse and motion, without claiming matching transient
speeds against Jolt.

Compile this example and pass `--controls-check` to the executable for windowless
controls checks. `--smoke` opens an automatic window, verifies both modes,
reversal, pause/resume, impulse balance and displayed poses, then closes.
