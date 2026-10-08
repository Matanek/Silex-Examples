# Hinge with an out-of-plane payload

From the workspace root (or the Spec Worktree group root):

```sh
silex run Silex-Examples/Sources/Physics3D/LoadedHinge/Main.sx --release
```

The scene starts paused. The blue arm pivots around the white support; its
green attachment carries a yellow 2 kg payload offset by one metre in depth.
Gravity and the floor are part of the simulation.

- **Vers la droite**, then **Vers la gauche**: arm and payload visibly move
  together. Each button selects its named direction and resumes simulation.
  The message confirms the command.
- **Lâcher le bras**: removes the motor; gravity makes the arm swing.
- **Charge derrière/devant le bras**: rebuilds the payload on the other side
  of the plane and pauses. Select a direction afterward.
- **Space** or **Pause/Reprendre**: stops or resumes the physical poses.
- **R** or **Remettre à zéro**: restores the vertical pose, paused, retaining
  the payload side. **Escape** closes the window.

Displayed angle, motor torque and residuals come from the physical constraints.
This view requests ±0.65 rad with a 40 N·m limit to make the action visible
under gravity; the comparative Jolt witness uses velocity control and a lower
0.2 N·m limit. The camera is fixed.

Window-free controls check and explicitly automatic native smoke:

```sh
silex compile Silex-Examples/Sources/Physics3D/LoadedHinge/Main.sx --release -o .silex/loaded-hinge
.silex/loaded-hinge --controls-check
.silex/loaded-hinge --smoke
```

The controls check synthesizes real UI and keyboard events, then verifies
mutations, displacement and rendered poses. The automatic smoke exercises
both targets, pause/resume, the opposite offset and release, then closes
the window. Normal startup changes no target automatically.

The Jolt comparison covers the converged assembly; initial corrections differ.
This scene does not qualify arbitrary chains, masses or commands.
