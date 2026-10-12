# Follow a pose and release the limbs

Both mannequins hang from their fixed torsos. Blue holds a neutral pose. Gold's
motors follow a target and can resist an impulse; when they stop, its limbs
hang under gravity. Anatomical limits and nonadjacent internal collisions stay
active. [Guide français](README.fr.md).

From the workspace or Spec group root:

```sh
silex run Silex-Examples/Sources/Physics3D/RagdollDrive/Main.sx --release
```

Use the buttons or keys:

- **1 / 2 / 0**: open, folded or neutral target for gold;
- **P**: impulse on gold's forearm;
- **M**: stop its motors, then resume towards the selected target;
- **Space**: pause or resume;
- **R**: recreate the assemblies; **Escape**: quit.

Changing the target preserves poses and velocities: motors progressively turn
the limbs. A new target resumes the motors. Reset is the only immediate
placement in this demo. Fixed torsos make the joints observable without the
whole assembly falling; this demonstrates neither standing balance nor world
translation control. [RagdollFall](../RagdollFall/README.md) retains free fall
and impacts.

Simulation runs at 120 Hz with 32 position correction passes and interpolated
rendering. Motors have 120 N·m per-axis budgets, stiffness 400 N·m/rad and
damping 40 N·m·s/rad. Targets change on commands; metrics and UI refresh at
10 Hz or after an actual action. Detailed geometric observations run only in
tests and smokes.

`--physics-check` and `--controls-check` validate the model and controls without
a window; `--smoke` exercises target changes, impulse, release, resume, pause
and reset in a window that closes automatically. A completed smoke requires
its final marker, not only exit code zero. Its frame rate is a local sample,
without a comparative FPS claim.
