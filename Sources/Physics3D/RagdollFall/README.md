# Two falling ragdolls: impulse and floor contact

The gold mannequin starts with raised arms; blue keeps a relaxed pose.
Each has ten bodies and nine free joints, without motors. Collision boxes
match rendered mesh dimensions. The world uses eight position correction passes
to retain anchors during impacts; Physics keeps its default of four passes.
Internal collisions are disabled; the floor
and contacts between instances remain part of the simulation.

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
show impulses, current contacts and simulated time.

## Qualification

```sh
silex test Silex-Examples/Sources/Physics3D/RagdollFall/Model.sx
silex test Silex-Examples/Sources/Physics3D/RagdollFall/Main.sx
```

The binaries support `--physics-check` (four four-second recipes, with/without
an impulse at 60/120 Hz, repeated after recreation), `--controls-check` (UI/key events through physical
effects) and `--smoke` (SDL/Metal, impulse, exact pause, resume, reset, second
fall and automatic exit). No check produces captures. Anchors and box corners
are checked in native Debug/Release; the renderer reuses pose buffers and geometry.

The headless Jolt witness separately qualifies a three-sphere chain and a
symmetric fall. This ten-part example is a tested consumer, without a claim of
identical Jolt impact trajectories. Active limits and motorized pose tracking
remain unqualified here. [RagdollPose](../RagdollPose/README.md) retains the pose
and short free-fall demonstration.
