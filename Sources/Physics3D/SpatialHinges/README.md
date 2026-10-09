# Control two perpendicular hinges

The blue arm rotates about the support’s red Z axis. The gold 2 kg payload
rotates about the green X axis at the arm tip. Its gold connector shows the
depth offset. The manual test checks whether these motions and controls are
clear in the oblique view.

From the workspace root or the Spec Worktree group root:

```sh
silex run Silex-Examples/Sources/Physics3D/SpatialHinges/Main.sx --release
```

The scene starts paused and changes no target automatically.

- **Monter/Baisser le bras**: targets approximately ±20° about the red pivot.
  The payload follows its support, preserving its angle relative to the arm.
- **Lever/Abaisser la charge**: targets approximately ∓26° about the green
  axis, preserving arm position. An already reached target stays held;
  choose the opposite button to see another movement.
- **Freiner les deux**: interrupts movement and holds current angles under
  gravity. Movement and braking commands resume the simulation from pause.
- **Space** or **Pause/Reprendre**: stops or resumes poses.
- **R** or **Remettre à zéro**: restores the horizontal pose, paused.
  **Escape** closes the window.

Targets, whole-degree angles and command number immediately acknowledge the
action; motion takes a few seconds. Motors request ±0.2 rad/s with capacities
60/40 N·m, then brake near the target. Arm mass is 2 kg, isotropic inertia
0.4 kg·m²; payload inertia is 0.2 kg·m² with offset 0.8 m. Collisions are
disabled; the platform and displayed shapes are illustrative. Camera is fixed.

The reaction qualification, documented in the `SpatialHinges3D` guide of
`GFX.Physics`, covers a small-angle path, two masses and two offsets against Jolt. This scene
extends the observed poses with geometry and holding checks for its own path;
it claims no Jolt parity at those angles, spatial contacts or arbitrary chains.

Windowless controls check and automatic graphical smoke:

```sh
silex compile Silex-Examples/Sources/Physics3D/SpatialHinges/Main.sx --release -o .silex/spatial-hinges
.silex/spatial-hinges --controls-check
.silex/spatial-hinges --smoke
```

The check synthesizes real clicks and keyboard events, then verifies independent
movements, reached targets, braking, pause, reset and Scene3D poses. The smoke
exercises both axes, simultaneous reversal and braking with pause/resume,
then closes its explicitly automatic window.
