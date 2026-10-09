# Drive a loaded shoulder and elbow

The bronze upper body and gold load each weigh 2 kg. The white shoulder stays
fixed to the support; the cyan elbow follows the upper body. Gray rods connect
the joints and mass centers. Red X, green Y and blue Z show the shoulder frame;
the blue line at the elbow follows its flexion axis. These frames move with
the members rather than the world axes.

From the workspace or owning Spec Worktree group root:

```sh
silex run Silex-Examples/Sources/Physics3D/ArticulatedPose/Main.sx --release
```

The scene starts paused. Poses never change automatically in manual use.

- **Pose +** targets shoulder X +14°, Y +11°, Z −9° and elbow +20°.
- **Pose −** reverses all four targets: the elbow bends relative to the upper
  body while the shoulder reorients the assembly.
- **Recentrer** targets zero on all four axes.
- **Space** or **Pause/Reprendre** pauses/resumes both members.
- **R** or **Remettre à zéro** restores the initial paused pose; **Escape** closes.

The white pivot must stay fixed and the cyan elbow must follow the upper body
without breaking the attachment. The load follows the elbow. Measurements
separate shoulder angles from the elbow’s angle relative to the upper body:
the load’s world rotation may change while its local elbow angle stays steady.
Check whether both motions are legible and smooth and whether controls behave
as expected.

Gravity deforms the elastic servos; recentering must not align every angle
exactly to zero. Shoulder capacity is 60 N·m per axis, stiffness 120 and damping
20; elbow capacity is 40 N·m, stiffness 80 and damping 15. Simulation runs at
120 Hz, interpolates both poses and updates measurements at 10 Hz. Meshes and
local rod orientations are prepared once. Inertias are isotropic, 0.4/0.2 kg·m²;
the floor and support are visual.

The contact-free recipe matches the qualified
`GFX.Physics/Tests/Consumer/Tests/ArticulatedPose3D.sx` consumer. Equilibria
are compared with pinned Jolt. Transient differences are measured without
general parity. This prepares articulated poses; the ragdoll facade, hierarchy
and self-filtering remain to be built.

Headless control check and SDL/Metal smoke covering twelve physical seconds:

```sh
silex compile Silex-Examples/Sources/Physics3D/ArticulatedPose/Main.sx --release -o .silex/articulated-pose
.silex/articulated-pose --controls-check
.silex/articulated-pose --smoke
```

The control check synthesizes clicks and keys through their physical effects.
The smoke visits opposite poses then recenters, pauses both members, checks
anchors, equilibria and rendered transforms, and closes automatically.
