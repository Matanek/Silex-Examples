# Follow a pose and release the limbs

Initially both mannequins hang from their fixed torsos. Blue holds a neutral pose.
Gold starts without motors: its limbs fall and swing under gravity. P applies a 6 N·s
forearm impulse. M or a target enables motorized holding; M then releases it.
T recreates both mannequins with mobile torsos and a physical floor; press T
again to return to suspension. Anatomical limits and nonadjacent internal
collisions stay active. [Guide français](README.fr.md).

From the workspace or Spec group root:

```sh
silex run Silex-Examples/Sources/Physics3D/RagdollDrive/Main.sx --release
```

Use the buttons or keys:

- **1 / 2 / 0**: open, folded or neutral target for gold;
- **P**: impulse on gold's forearm;
- **M**: stop its motors, then resume towards the selected target;
- **T**: choose suspension or floor and recreate both mannequins;
- **Space**: pause or resume;
- **R**: recreate the assemblies; **Escape**: quit.

Changing the target preserves poses and velocities: motors progressively turn
the limbs. A new target resumes the motors. R and mode changes are the only
immediate placements in this demo. Fixed torsos make the joints observable without the
whole assembly falling; this demonstrates neither standing balance nor world
translation control. In floor mode, motors act on contacting limbs while the
torsos remain fully mobile: a target does not impose a pose, and contacts may
prevent exact tracking. R recreates the current mode.
[RagdollFall](../RagdollFall/README.md) retains free fall and impacts.

Simulation runs at 120 Hz with 32 position correction passes and interpolated
rendering. Motors have 120 N·m per-axis budgets, stiffness 400 N·m/rad and
damping 8 N·m·s/rad for gold, 40 for blue. Gold can visibly oscillate after an
impulse instead of damping the reaction almost immediately.
Targets change on commands; metrics and UI refresh at
10 Hz or after an actual action. Detailed geometric observations run only in
tests and smokes.

`--physics-check` and `--controls-check` validate the model and controls without
a window; `--smoke` exercises target changes, impulse, release, resume, pause,
reset and both modes in a window that closes automatically. On the compiled
binary, `--floor` starts the interactive scene directly on the floor. A completed
smoke requires its final marker, not only exit code zero. Its frame rate is a local sample,
without a comparative FPS claim.
