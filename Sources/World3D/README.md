# World3D FPS

Walk through the forest with an upright collision capsule. The central blue
staircase exercises step climbing; the green one-metre ledge is walkable, the
red two-metre block prevents automatic step climbing, and the yellow roof blocks upward motion.
Scattered cube rocks, pebbles and procedural trees use their rendered transforms
as box colliders. Imported GLTF foliage and grass remain decorative, as in the
archived WorldDemo; they have no mesh colliders.

From the Silex workspace root:

```sh
silex run Silex-Examples/Sources/World3D/Main.sx --release
```

For the Jolt-3D-Physics candidate, run from its `Worktree/` group instead:

```sh
Silex/Toolchain/zig-out/bin/silex run Silex-Examples/Sources/World3D/Main.sx --release
```

The launcher runs the application beside `Main.sx`, where its relative `Assets/`
paths resolve. A directly compiled executable must be launched from that directory.

## Controls

| Input | Action |
| --- | --- |
| WASD | Walk |
| Mouse | Look |
| Left Shift | Sprint |
| Space | Jump; release early for a shorter jump |
| Left Alt / Option | Lower viewpoint and walk slowly; press while sprinting to slide |
| R | Reset the character |
| Escape | Quit |

The settings follow the archived NKEngine WorldDemo: 6 m/s walk, 7.8 m/s sprint,
3 m/s crouch, 1.85 m nominal jump height, 0.4 s ascent and 0.35 s descent,
125 ms coyote time, 45° slope limit and 1.2 m maximum step. Camera effects include
stair smoothing, head bob, landing dip, strafe tilt and sprint FOV (75–90°).
The 120 Hz movement loop is independent of rendering and interpolates position.

Like the archive, crouching changes eye height and speed while preserving the
full-height capsule. It does not allow passing under a lower ceiling. A slide
lasts at most 1.35 s, ends when Alt is released or support is lost, and prevents
jumping while active. Footstep sounds are not included.

`FPSController.sx` owns gameplay and camera effects, `Player.sx` binds input and
Application, and `GFX.Physics.CharacterMover3D` resolves capsule motion. The
current mover treats body poses as stationary during each call: moving-platform
transport, pushing dynamic bodies and physical character-to-character interaction
are future physics work.

## Verification

The consumer test `GFX.Physics/Tests/Consumer/Tests/CharacterMover3D.sx` covers
capsule collision behavior; `Tests/Controller.sx` covers the FPS movement rules.
Pass `--smoke` to the executable for an automatic four-second staircase, jump
and landing run. It checks the final support and peak height and then exits.
