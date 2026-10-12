# Impose a pose and release two mannequins

Both mannequins share a ten-part hierarchy: torso, head, upper arms, forearms,
thighs and lower legs. White dots show joint frames; colored blocks show
the shapes offset from those frames. The gold mannequin can change pose;
the blue mannequin is a reference.

From the workspace or owning Spec worktree group root:

```sh
silex run Silex-Examples/Sources/Physics3D/RagdollPose/Main.sx --release
```

The scene starts paused.

- **Pose détendue** or **Bras levés** immediately imposes the gold
  mannequin's pose and returns both instances to their initial height.
  The blue mannequin retains its reference pose.
- **Libérer / rejouer** replaces both mannequins, zeros their velocities,
  then starts 600 ms of physical free fall. Automatic pause keeps both
  poses in view and lets you inspect them.
- **Space** or **Pause/Reprendre** interrupts or resumes the fall. After
  it finishes, resuming replays the same short fall from the initial height.
- **R** or **Remettre à zéro** destroys and recreates the assemblies in
  their relaxed pose, paused. **Escape** closes the window.

Parts remain connected during the fall. Imposing a pose is immediate placement,
distinct from physically tracking a motor target. This scene has no floor or
motor; internal collisions are explicitly suppressed. The two instances remain
independent and can normally collide, but this scene's placements and poses
keep them apart.

Gravity is −9.81 m/s² along Y; each part has mass 2 kg and isotropic inertia
0.2 kg·m². Swing/twist joints allow free rotation. Simulation runs at 120 Hz,
interpolates joint frames read through `write_pose`, and refreshes metrics at
10 Hz. Meshes are prepared once. The headless check validates local parentage,
anchors, shape origins, analytical free fall at 60/120 Hz and rendered transforms.

```sh
silex compile Silex-Examples/Sources/Physics3D/RagdollPose/Main.sx --release -o .silex/ragdoll-pose
.silex/ragdoll-pose --controls-check
.silex/ragdoll-pose --smoke
```

The smoke imposes a pose, falls, pauses, resumes and recreates the assemblies
for a second fall. It closes automatically. The manual check concerns the
readability of both poses, joint markers, the fall and controls. Floor contacts,
impulses and general motor targets remain separate qualification steps beyond
the ragdoll foundation.
