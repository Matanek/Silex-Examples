# Drive a compound orientation under load

The gold 2 kg load pivots around the fixed white point. Three gray bars form
an offset rigid attachment; red X, green Y and blue Z show the motor frame
attached to the load. The servos drive X twist and Y/Z swing simultaneously.
This scene makes the recipe qualified by
`GFX.Physics/Tests/Consumer/Tests/LoadedSwingTwist3D.sx` observable and helps
read motorized poses, without constituting a ragdoll.

From the workspace root or owning Spec Worktree group:

```sh
silex run Silex-Examples/Sources/Physics3D/LoadedSwingTwist/Main.sx --release
```

The scene starts paused. Selecting a target resumes simulation; targets do
not change automatically in manual mode.

- **Cible +** commands approximately X +14°, Y +11°, Z −9°.
- **Cible −** reverses all three targets; the load and its axes orient the other
  way while retaining the pivot.
- **Recentrer** commands all three angles to zero.
- **Space** or **Pause/Reprendre** pauses/resumes motion.
- **R** or **Remettre à zéro** restores the initial pose while paused; **Escape** exits.

Actual angles, targets and torques update ten times per second. The attachment
must remain at the white pivot, motion must converge and reversal must be
readable. Colored axes follow the motor frame rotated by 0.35 rad inside the
load; they are not fixed world axes.

Weight deflects equilibrium away from the target. Stiffness 80 N·m/rad and
damping 15 N·m·s/rad are finite: **Recentrer** should not align all three angles
exactly to zero. Each axis has a 30 N·m budget. Simulation runs at 120 Hz and
rendering interpolates poses; the camera is fixed, isotropic inertia is
0.4 kg·m² and gravity is −9.81 Y. Local offset is (0.5, 0.2, 0.4) m;
floor, support and bars are visual. This recipe has no contact or second
dynamic articulation.

Equilibria and balances are compared against Jolt. Equal transient responses
between engines are not established. Human testing checks readability and
smoothness of the compound motion, as well as the controls.

Window-free control check followed by a nine-second SDL/Metal smoke:

```sh
silex compile Silex-Examples/Sources/Physics3D/LoadedSwingTwist/Main.sx --release -o .silex/loaded-swing
.silex/loaded-swing --controls-check
.silex/loaded-swing --smoke
```

The check synthesizes clicks and keyboard events through their physical effects,
covering reversal, recentering, repeated Space, reset and rendered poses.
The smoke visits all three targets, pauses and resumes simulation, checks
steady states and displayed transforms, and closes itself.
