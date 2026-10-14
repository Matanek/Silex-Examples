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
- **3**: request elbow and knee angles beyond their stops;
- **P**: impulse on gold's forearm;
- **B**: launch a red block towards gold and observe its physical impact;
- **C**: choose the next shot, frontal or oblique from the left/right;
- **M**: stop its motors, then resume towards the selected target;
- **T**: choose suspension or floor and recreate both mannequins;
- **Space**: pause or resume;
- **R**: recreate the assemblies; **Escape**: quit.

Request **3** retains the open target’s shoulders and hips, but requests
−2.8 rad at the elbows and 2.8 rad at the knees. Their limits remain −2.35
and 2.4 rad: joints bound the gesture, and contacts may block it before a stop.
The panel reports four excessive requests while their motors are active.
An excessive target does not place any member.

The block flies and transfers its impact through contact: B changes no
mannequin pose or velocity when firing. The impact counter increases only
after a measured contact with gold. Only one block is active; a new shot
replaces it, and it disappears after about three seconds. R and T remove it.
B resumes after a pause; Space freezes the projectile too.
C preserves pause and the trajectory of an already launched block. Its choice
persists across R and T to compare the same direction in both support modes.
Directions use the scene's initial frame; rotating the torso does not rotate
the launcher. The block weighs 8 kg and its horizontal speed relative to the
targeted part is 16 m/s.
It starts 3.2 m upstream to retain a 0.2 s aiming time. The initial velocity
compensates for gravitational drop; on the floor, the aiming height stays at
least 30 cm above ground so the cube does not strike the floor before the torso.
Shots then aim at the mobile torso to move the whole mannequin.
In suspension, obliques aim at the selected side’s forearm and frontal shots
at the left forearm; P retains its direct impulse on that arm.

To start on the floor with an oblique shot selected, compile and launch the
binary from the same root:

```sh
silex compile Silex-Examples/Sources/Physics3D/RagdollDrive/Main.sx --release -o .silex/ragdoll-drive
.silex/ragdoll-drive --floor --oblique
```

Choose a direction with C, fire with B, then compare motors and free limbs
with M. T retains the direction and changes support.

Changing the target preserves poses and velocities: motors progressively turn
the limbs. A new target resumes the motors. R and mode changes are the only
immediate mannequin placements in this demo. Fixed torsos make the joints observable without the
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

On the compiled binary, `--projectile-check` qualifies firing, contact and
response without a window at 60/120 Hz in both support modes, with active or
released motors. It also compares an identical mannequin without a block. `--oblique-check`
exercises both obliques in their sixteen corresponding configurations, retaining
the same limit, penetration and velocity bounds.
In free mode, at least one limb must deviate by more than 15 cm from the control
during the first second; on the floor, the torso must also deviate by more
than 50 cm from the control. Suspended motorized mannequins must regain their
target after impact.
Holding intentionally reduces movement amplitude.

`--physics-check` and `--controls-check` validate the model and controls without
a window; `--smoke` exercises target changes, impulse, release, resume, pause,
reset, then frontal and both oblique block shots in both modes, with interpolated rendering
and visibility checked in a window that closes automatically. On the compiled
binary, `--floor` starts the interactive scene directly on the floor and
`--limits` selects the excessive request without placing members.
`--limits-check` isolates its headless recipe; `--physics-check` includes it
alongside the previous cases and oblique shots. Smoke checks the request and then frontal/oblique firing in both support modes.
A completed
smoke requires its final marker, not only exit code zero. Its frame rate is a local sample,
without a comparative FPS claim.
