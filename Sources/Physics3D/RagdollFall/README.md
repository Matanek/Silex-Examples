# Two falling ragdolls: impulse and floor contact

The gold mannequin starts with raised arms; blue keeps a relaxed pose.
Each has ten bodies and nine limited joints, without motors. Elbows and knees
bend in one direction; shoulders and hips have mirrored lateral limits.
The neck stays within a limited cone. These settings give the boxes a stylized
anatomy, without claiming the full range of human motion.
Collision boxes match rendered mesh dimensions. The world uses 32 position correction passes
to retain anchors during impacts; Physics keeps its default of four passes.
Nonadjacent parts can collide: a forearm meets the torso. Parent/child pairs
remain filtered at their joint; shoulder limits keep upper arms outside the
chest. The floor and contacts between instances remain part of the simulation.

From the workspace or Spec group root:

```sh
silex run Silex-Examples/Sources/Physics3D/RagdollFall/Main.sx --release
```

- **Libérer / rejouer** restores the initial poses and starts the fall.
- **Pousser le torse**, or **P**, applies an off-center `(6, 2, 3)` N·s impulse
  to the gold torso and resumes a paused simulation. Multiple impulses can
  accumulate during the four-second run.
- **Space** or the pause button freezes/resumes both assemblies.
- **R** or **Remettre à zéro** destroys and recreates the assemblies, paused.
- **Escape** closes the window.

After four simulated seconds, automatic pause lets you inspect the poses.
Release, P or resume after completion starts another run from the initial poses.
Logical keys work independently of their physical positions; auto-repeat does
not apply repeated impulses. White markers show joint frames. The counters
show impulses, current contacts and simulated time, refreshed at 10 Hz.
Commands and pause changes provide immediate feedback.

## Qualification

```sh
silex test Silex-Examples/Sources/Physics3D/RagdollFall/Model.sx
silex test Silex-Examples/Sources/Physics3D/RagdollFall/Main.sx
```

The binaries support `--physics-check` (four four-second recipes, with/without
an impulse at 60/120 Hz, repeated after recreation), `--controls-check` (UI/key events through physical
effects) and `--smoke` (SDL/Metal, impulse, exact pause, resume, reset, second
fall and automatic exit). No check produces captures. Counterchecks cover
forearm/torso contact, adjacent-part filtering and forbidden flexion correction.
Falls check angular errors (< 0.08 rad), penetration between nonadjacent parts
and upper arm/torso (< 5 cm), anchors (< 4 cm) and floor penetration (< 5 cm)
at every step in native Debug/Release; the renderer reuses pose buffers and geometry.

For cost diagnosis, `--profile-cost` separates paused UI work from 480 physical
steps after warm-up. `--profile-scene` measures the actual window cadence during
two pauses and two falls, then closes the window. `--smoke` adds detailed checks
at every physical step; its cadence includes that validation work. Use the
interactive **Release** launch, without these options, to assess demo fluidity.

The headless Jolt witness separately qualifies a three-sphere chain and a
symmetric fall. This ten-part example is a tested consumer, without a claim of
identical Jolt impact trajectories. Motorized pose tracking and Jolt parity for
limits during these impacts remain unqualified here. [RagdollPose](../RagdollPose/README.md) retains the pose
and short free-fall demonstration.
