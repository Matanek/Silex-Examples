# Drive a rack to its rail stops

From the workspace root or the Spec Worktree group root:

```sh
silex run Silex-Examples/Sources/Physics3D/RackServo/Main.sx --release
```

The scene starts paused. The yellow pinion drives the blue bar held by a slider.
Green markers show the two rail stops.

- **Vers la droite**, then **Vers la gauche**: the bar reaches each stop.
  The motor remains active and pushes the stop; status and torque show this.
  Each button explicitly selects its side and resumes the simulation.
- **Revenir au centre**: the motor brings the bar back to the rail midpoint.
- **Space** or **Pause/Reprendre**: pause or resume the simulation.
- **R** or **Remettre à zéro**: restore the initial pose, paused.
  **Escape** closes the window.

The ratio is 2 rad/m and stroke ±0.6 m. Pinion targets are ±1.5 rad, with a
12 N·m cap, stiffness 15 and damping 8. Physics uses a fixed 120 Hz step.
The stop holds the bar at a pinion angle of ±1.2 rad before its target;
settled torque is ±4.5 N·m. Teeth and markers are decorative: transmission
comes from the constraint, without tooth collisions.

The hinge takes the short angular path. Targets ±2 rad would drive the other
way after reversal and could remain blocked by the rail; this example chooses
commands whose path reaches the requested side. Pose correction at the first
stop remains progressive. The comparative witness preserves Silex and Jolt
transients at 60/120 Hz; it does not guarantee phase below 0.002 rad on every
step at every frequency.

Headless verification:

```sh
silex compile Silex-Examples/Sources/Physics3D/RackServo/Main.sx --release -o .silex/rack-servo
.silex/rack-servo --controls-check
```

This check synthesizes clicks and keys and verifies both stops, midpoint,
reset and poses sent to rendering. The native smoke opens a window and closes
it after nine simulated seconds; run it only when a window is appropriate:

```sh
.silex/rack-servo --smoke
```

Normal execution stays manual. This scene does not qualify arbitrary spatial
chains, free axes or shape collisions.
