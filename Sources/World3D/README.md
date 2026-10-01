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
The 120 Hz movement loop is independent of rendering. Both the capsule position
and its stair correction are interpolated together. The viewpoint catches up at
at most 3 m/s after support height changes; jumping retains its ballistic motion.
Step probing preserves the requested horizontal speed, including small obstacles
and slow movement. Strafe tilt leans toward the direction of movement.

Like the archive, crouching changes eye height and speed while preserving the
full-height capsule. It does not allow passing under a lower ceiling. A slide
lasts at most 1.35 s, ends when Alt is released or support is lost, and prevents
jumping while active.

Footsteps and slide audio reuse the original WorldDemo MP3 samples, decoded once
at startup through GFX.Audio. Steps follow the walking head-bob cycle and alternate
slightly left/right near the center (±0.1 pan), with small gain and pitch variation.
Standing still, pushing against a wall, jumping and sliding do not emit walking steps.
A landing produces one centered impact only after at least 0.30 m of descent from
the airborne peak. Brief losses of support over small obstacles preserve the
left/right walking sequence, and their heights do not accumulate across contacts.
Landing gain rises linearly from 0% at 0.30 m to 100% at 1.50 m and stays capped
above that height. Pitch still varies slightly; the impact remains centered.
The slide sound ends when the slide ends or the character is reset.

`FPSController.sx` owns gameplay and camera effects, `Player.sx` binds input and
Application, `FootstepAudio.sx` consumes movement events, and
`GFX.Physics.CharacterMover3D` resolves capsule motion. The
current mover treats body poses as stationary during each call: moving-platform
transport, pushing dynamic bodies and physical character-to-character interaction
are future physics work.

## Verification

The consumer test `GFX.Physics/Tests/Consumer/Tests/CharacterMover3D.sx` covers
capsule collision behavior; `Tests/Controller.sx` covers the FPS movement rules.
Pass `--smoke` to the executable for an automatic four-second staircase, jump
and landing run. It checks the final support, peak height and footstep/landing
playback requests,
then exits. `Tests/FootstepAudio.sx` also exercises MP3 decoding, overlapping voices,
slide start/stop and reset with a real or dummy audio device.
