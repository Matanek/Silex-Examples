# Raise and lower a load on the vertical rail

A hinge connected to the world holds the blue arm. It carries a green vertical
slider offset by 0.8 m and a gold 2 kg sphere. This manual scene lets you read
the combination of two joint families and its controls; the gravity recipe's
balances are already qualified in Physics `SpatialRail3D`.

From the workspace root or owning Spec Worktree group:

```sh
silex run Silex-Examples/Sources/Physics3D/SpatialRail/Main.sx --release
```

The scene starts paused, with no automatic target changes.

- **Abaisser jusqu’au plan** resumes simulation and lowers the sphere on the
  rail. First contact brakes the motor and holds the reached travel.
  **CONTACT ATTEINT** confirms the stop with a small green measured contact marker.
- **Lever la charge** resumes simulation and raises it towards +15 cm travel.
  **CHARGE LIBRE** indicates release; the contact marker disappears.
- **Freiner** stops travel and holds the current position.
- **Space** or **Pause/Reprendre** pauses/resumes simulation.
- **R** or **Remettre à zéro** resets travel to zero while paused; **Escape** exits.

Travel and target appear in centimeters alongside the command number. Measurements
update ten times per second. The rail and crossbar stay attached to the arm;
only the sphere moves vertically. The camera is fixed. Radius 0.15 m, physical
floor Y=1.58 m, initial centers Y=1.8 m, masses 2/2 kg and isotropic inertias
0.4/0.2 kg·m². Capacities: hinge 60 N·m, slider 40 N; only the sphere touches
the frictionless floor, with zero restitution.

The command brakes at first contact and does not push towards an unreachable
target. This scene adds visual reading, raising to +15 cm and interactions
to the comparative recipe; it does not qualify arbitrary chains.

Window-free control check followed by an automatic graphical smoke:

```sh
silex compile Silex-Examples/Sources/Physics3D/SpatialRail/Main.sx --release -o .silex/spatial-rail
.silex/spatial-rail --controls-check
.silex/spatial-rail --smoke
```

The check synthesizes clicks and keyboard events through their physical effects,
verifies a ten-second hold, raising, braking, pause, reset and displayed poses.
The SDL/Metal smoke follows two contacts and closes itself.
