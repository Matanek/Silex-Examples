# The puppet workshop: first physical steps

A thirteen-body mechanical character walks and turns on a grid floor.
Torso and leg motors track walking targets; foot contacts actually move the body.
Rendering follows the physical bodies.

From the workspace or Spec Worktree group root:

```sh
silex run Silex-Examples/Sources/Physics3D/ActiveRagdoll/Main.sx --release
```

- **Hold ZQSD**: choose a camera-relative direction; the character turns and
  walks towards it.
- **P**, or **Pousser**: apply an impulse to the torso without placing its pose.
- **F**: release/re-enable the joints and balance assistance.
- **R**: destroy and recreate the character. Only this command resets it.
- **Escape**: close the window.

The camera follows smoothly. A left HUD shows loaded foot supports, speed and
assistance torque. Nonadjacent parts can collide; hips, knees, ankles, shoulders
and elbows have limits. Arms hang freely: shoulders and elbows have no pose
motors. Nuts and eyes decorate the physical volumes. The reference silhouette
has a faceted purple head, grey cap and jaw, pale nut eyes and hands, an orange
vest, a spindle waist and pale feet.

## Balance and walking

Each foot trajectory separates the lifted return from ground propulsion.
The target foot path travels 60 cm front-to-back, with a 19 cm lifted return.
Two-link inverse kinematics computes hip and knee targets. Joint motor torques
are bounded; no body pose is imposed while moving.

An external angular motor assists pelvis balance, capped at 350 N·m per axis
and enabled while contacting the ground. All translations remain free: no motor
lifts or transports the pelvis. Passive mode disables both assistance and joint motors.
In active mode, a fall starts alternating leg support searches, followed by
leg extension as the pelvis becomes upright. Walking resumes after stabilization.
Corrective steps also start when the predicted center of mass leaves the foot
support footprint. Use F to let it fall, then re-enable it: getting up needs no
reset. R remains an explicit recreation. The external torque helps the get-up;
this controller does not model autonomous human balance.

Physics runs at a fixed 120 Hz with 24 velocity iterations and 32 position
passes. Render geometry and the textured floor are created once; transforms
are interpolated between physical steps.

## Check without a window

```sh
silex test Silex-Examples/Sources/Physics3D/ActiveRagdoll/Main.sx
silex test Silex-Examples/Sources/Physics3D/ActiveRagdoll/Qualification.sx
silex compile Silex-Examples/Sources/Physics3D/ActiveRagdoll/Main.sx --release -o .silex/active-ragdoll
.silex/active-ragdoll --controls-check
.silex/active-ragdoll --physics-check
```

The scene check covers logical keys and HUD buttons, impulse, passive mode,
reset, framing and mesh transforms without initializing a window. Physics
checks cover rest, walking, turning, stopping, bounded efforts, passive fall,
getting up after four fall directions, walking again, active shoves and
destruction at 60/120 Hz. Arm motor torques remain zero. A frictionless
countercheck verifies that internal motors and angular assistance do not translate the total center of mass
horizontally.

This is the first course in an evolving scene. Grabbing, loads, hitting with
objects, climbing, ropes and entering vehicles are not present yet. It does
not replace independent capsule-controller qualification or establish universal
trajectory parity with Jolt.

Visual and active-ragdoll inspiration:
[MetallCore999](https://www.youtube.com/@metallcore9993) and the
[Unity example](https://github.com/metallcore999/Projects). The character and
Silex controller are specific to this demo.

[Guide français](README.fr.md).
