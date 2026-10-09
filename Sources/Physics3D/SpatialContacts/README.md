# Lower a payload to the plane, then lift it

The gold 2 kg sphere is carried through two perpendicular hinges. The blue
arm stays held. This manual test checks whether the plane, stopped descent
and contact release are visually understandable. Mechanical balances are
already qualified by the Physics package tests.

From the workspace root or the Spec Worktree group root:

```sh
silex run Silex-Examples/Sources/Physics3D/SpatialContacts/Main.sx --release
```

The scene starts paused, without automatic target changes.

- **Abaisser jusqu’au plan** resumes simulation and lowers the payload.
  On first contact, the command brakes the motor and holds the reached angle.
  **CONTACT ATTEINT** confirms the stop. A small green marker appears at the
  measured contact point while contact exists.
- **Lever la charge** resumes simulation and lifts the sphere. The message
  changes to **CHARGE LIBRE** and the green marker disappears.
- **Freiner** interrupts movement and holds the current angle.
- **Space** or **Pause/Reprendre** pauses/resumes simulation.
- **R** or **Remettre à zéro** restores the horizontal pose, paused.
  **Escape** closes the window.

Command number immediately acknowledges the action; angles and state update
ten times per second. Motion takes a few seconds. Camera is fixed. The
infinite physical plane lies at Y=1.58 m; the displayed plate represents its
useful area. Sphere radius 0.15 m, offset 0.8 m, masses 2/2 kg, isotropic
inertias 0.4/0.2 kg·m², motor capacities 60/40 N·m. Only the sphere collides
with the plane, with zero friction and restitution.

Stopping on first contact is part of the command: it does not keep pushing
indefinitely toward an unreachable target. Physics's `SpatialContacts3D`
guide documents the bounded Jolt qualification; this scene adds interaction
and rendering, without qualifying prolonged forced contact or arbitrary chains.

Windowless controls check and automatic graphical smoke:

```sh
silex compile Silex-Examples/Sources/Physics3D/SpatialContacts/Main.sx --release -o .silex/spatial-contacts
.silex/spatial-contacts --controls-check
.silex/spatial-contacts --smoke
```

The check synthesizes real clicks and keyboard events, then verifies contact
stop, holding, lifting, displayed poses, braking, pause and reset. The smoke
follows two contact paths and closes automatically.
