# Silex Examples

`Silex-Examples` gathers visual and interactive demonstrations so they can be
found and launched without browsing each package repository. This repository
is a catalog of standalone applications: focused technical illustrations
belong in documentation, while API proofs remain under `Tests/` in their
owning package.

The [World3D FPS scene](Sources/World3D/README.md) demonstrates capsule movement,
variable jumping and automatic stair climbing in a forest.

## Organization

All demonstrations live under [`Sources/`](Sources/). Focused technical
demonstrations are named directly after what they show. Complete programs are
grouped under `Sources/Apps/` and, as the catalog grows, `Sources/Games/` so
each product can keep its own sources and assets together.

A compact, self-contained demonstration remains a direct file:

```text
Sources/AnalogClock.sx
Sources/BoidsSimulation.sx
```

A large or multi-file demonstration receives a directory with a `Main.sx`
entry point:

```text
Sources/Physics2D/FallingBodies/Main.sx
Sources/EmbeddedWebView/Main.sx
Sources/EmbeddedWebView/Web/...
```

Applications follow the same multi-file convention under their stable group:

```text
Sources/Apps/Calculator/Main.sx
Sources/Apps/Calculator/Calculator.sx
Sources/Apps/Calculator/Interface.sx
Sources/Apps/Calculator/Session.sx
Sources/Games/Minesweeper/Main.sx
```

Closely related Bundle demonstrations share the stable `Sources/Bundle/`
prefix so content transitions, window replacement, and simultaneous windows
can be explored together without flattening their names into `Bundle...` files.
The `Sources/Physics2D/` prefix similarly groups the focused body-control and
shape-response demonstrations with the larger falling-bodies and rotating-
container applications.

A single [`Package.json`](Package.json) describes the dependency graph needed
by the complete catalog.

## Installing published packages

```sh
silex install AI
silex install GFX --suite
silex install GFX.Audio
silex install GFX.Physics
silex install GFX.UI --suite
silex install GFX.WebView
silex install HTML
silex install Plot
```

## Running a demonstration

Run direct files from the repository root:

```sh
silex run Sources/AnalogClock.sx
silex run Sources/Bundle/Transitions.sx
silex run Sources/Bundle/WindowReplacement.sx
silex run Sources/Bundle/MultipleWindows.sx
silex run Sources/ApplicationWindow.sx
silex run Sources/DirectWindowInputLoop.sx
silex run Sources/DedicatedSystemTerminal.sx
silex run Sources/ComposedSystemTerminal.sx
silex run Sources/ApplicationCommandConsole.sx
silex run Sources/BehaviourTreeCreatures.sx
silex run Sources/GeneratedHTMLWebView.sx
silex run Sources/BoidsSimulation.sx
silex run Sources/CanvasProjection3D.sx
silex run Sources/CanvasEffectsGallery/Main.sx
silex run Sources/CanvasFilterPostProcess/Main.sx
silex run Sources/CharacterMover2D.sx
silex run Sources/FPSStatsPanel.sx
silex run Sources/PerformanceStatsPanel.sx
silex run Sources/PlotGallery.sx
silex run Sources/SilexLogo.sx
silex run Sources/SpatialAudio.sx
silex run Sources/WebViewBridge.sx
```

Run multi-file demonstrations from the repository root as well:

```sh
silex run Sources/Physics2D/FallingBodies/Main.sx
silex run Sources/Physics2D/RotatingPhysicsContainer/Main.sx
silex run Sources/Physics3D/RigidScene.sx
silex run Sources/Physics3D/DistanceSpringScene.sx
silex run Sources/PhysicsDebugDraw2D/Main.sx --release
silex run Sources/PhysicsJointDebugDraw2D/Main.sx --release
silex run Sources/ShapeGallery2D/Main.sx
silex run Sources/Apps/Calculator
silex run Sources/Games/Minesweeper
```

`BehaviourTreeCreatures.sx` is a top-down RTS vignette driven by one immutable
`Resources.Behaviour<Battlefield>` and one independent
`Components.Behaviour<Battlefield>` instance per unit. Two round yellow workers
travel between a crystal mine and storage. Three square blue guards patrol in
separate lanes, then form around each red diamond raider: one tanks on the
frontline while the other two support it. The raider is stronger than one
guard; when the tank becomes wounded, its tree is interrupted, a healthy guard
takes over, and the wounded guard retreats to its own healing slot before
returning. Alternating waves use one hard-hitting raider or two lighter
raiders, then respawn two seconds after the previous wave is defeated. Health
bars, short unit markers and the live decision panel expose the active branches
and tank rotations.

Compile its deterministic hidden smoke and pass `--verify` to the executable:

```sh
silex compile Sources/BehaviourTreeCreatures.sx -o /tmp/silex-bt-creatures
/tmp/silex-bt-creatures --verify
```

The bounded run asserts one shared definition, five persistent villagers,
dynamic raider instances, multiple waves, completed gather/deposit cycles,
combat on both sides, a tank rotation, a priority interruption, a completed
heal and defeated raiders.

`FallingBodies` is the visual counterpart of the `FallingBodies2D` benchmark.
It uses the same fixed body sizes, fixed-step world and background physics
worker, then publishes completed transform snapshots to Scene2D without
blocking rendered frames. Benchmark options, diagnostics and metric panels are
deliberately omitted. `RotatingPhysicsContainer` remains the focused example
of the application-level `Plugins.Physics2D` integration.

`Physics3D/RigidScene.sx` shows the application-level `Plugins.Physics3D`
integration with Scene3D: three dynamic cubes fall onto a fixed floor, and a
red marker records the latest contact begin point. The mesh and collider of
each body use the same dimensions; Scene3D reads the pose published by the
physics plugin before rendering. A separate lane contains a purple sensor and
a thin red wall. Press **Space** to fire a fast yellow box, **C** to switch
continuous collision for the next shot, and **R** to query the wall with a
filtered ray. The console reports the selected mode, ray fraction, and sensor
crossing. With continuous collision enabled, the projectile reaches the wall;
with it disabled, the projectile can pass through in one fixed step.

`Physics3D/DistanceSpringScene.sx` shows a separate 3D distance spring: a
blue weight oscillates beneath a fixed gold anchor without gravity. Press
**R** to release it again from length 3 toward target length 2, and **D**
to switch between damping ratios 0.1 and 1.0. The first mode overshoots and
oscillates; the second returns without a visible overshoot.

`Physics3D/TriangleMeshScene.sx` shows a gold sphere falling onto a sloped
surface made of two differently colored fixed triangles. Gravity makes it roll
across their shared diagonal; a dark patch makes the rotation visible. The
sphere restarts after each crossing; press **R** to restart early or **Escape**
to quit. A compiled binary accepts `--smoke` to check the fall, continuing
contact, both face identities, support height, and acquired spin. From the
workspace root or the Spec Worktree group root, run
`silex run Silex-Examples/Sources/Physics3D/TriangleMeshScene.sx`.

`Physics3D/HeightGridScene.sx` builds a fixed 4 by 4 height grid. A gold sphere
falls onto its three colored slopes, then rolls across the marked cell rows.
The visible triangles use the same grid as the collider. Press **R** to
restart or **Escape** to quit. A compiled binary accepts `--smoke` to check
the fall, contact identity on all three rows, travel, and acquired spin.
From the workspace root or Spec Worktree group root, run
`silex run Silex-Examples/Sources/Physics3D/HeightGridScene.sx`.

`Physics3D/CapsuleTerrainScene.sx` moves a gold capsule back and forth over a
4 by 4 height grid. The marked seams show uphill and downhill support changes.
Press **Tab** for manual movement with **WASD** or the arrow keys, **Space** to
jump, **R** to restart, and **Escape** to quit. The capsule turns coral while
airborne. A compiled binary accepts `--smoke` to verify continuous support
through all three rows in both directions. From the workspace root or Spec
Worktree group root, run
`silex run Silex-Examples/Sources/Physics3D/CapsuleTerrainScene.sx`.

`Physics3D/MovingConvexScene.sx` shows two dynamic convex solids falling and
rotating about their actual mass centers, and a kinematic convex platform
carrying a sphere. The meshes use the physical hull boundaries. Simulation
runs in real time and restarts every 4.5 seconds. **Space** pauses, **R**
restarts and **Escape** exits. Launch from the workspace root:
`silex run Silex-Examples/Sources/Physics3D/MovingConvexScene.sx`.

`Physics3D/ConvexPairsScene.sx` uses hulls for every physical shape: a rotating
tetrahedron hits a dynamic convex base, while a kinematic platform lifts a
convex cube. The scene repeats every 4.5 seconds; Space pauses, R restarts and
Escape exits. From the workspace root, run
`silex run Silex-Examples/Sources/Physics3D/ConvexPairsScene.sx`.

`Physics3D/CharacterConvexScene.sx` walks an upright capsule up and down a
fixed convex wedge. Tab switches to manual movement, WASD or arrows move
relative to the camera's horizontal orientation,
Space jumps, R restarts and Escape exits. A `--smoke` run checks continuous
support in both directions and the interpolated render component over 1,020
fixed steps. From the workspace or Spec group root, run
`silex run Silex-Examples/Sources/Physics3D/CharacterConvexScene.sx`.

`Physics3D/ConvexHullScene.sx` builds a solid wedge from six points using
`ConvexHull3D`. Two spheres, a box and a green capsule fall, bounce on the actual slope, slide
off and land on a lower tray. Physics advances at 60 Hz in real time with interpolated
render poses, matching restitution and shadows reaching the tray. The scene
restarts automatically every three seconds; Space pauses, R restarts and
Escape quits. `--smoke` verifies two complete cycles and rendered motion.
Run from the workspace root:
`silex run Silex-Examples/Sources/Physics3D/ConvexHullScene.sx`.

`Physics3D/TerrainCCDScene.sx` starts three physical trajectories automatically:
gold falls onto the terrain and rebounds, coral rises through the back face
then bounces on the front face, and blue falls through an opening onto a
lower tray. All three spheres have the same constant restitution of 0.65.
Gravity runs in real time at a fixed 1/60 s step;
interpolated poses keep the motion smooth. The sun casts shadows out to
40 m, covering the lower tray as well as the terrain. The scene restarts
every four seconds.
Press **Space** to pause or resume, **R** to restart, and
**Escape** to quit. From the workspace root or Spec Worktree group root, run
`silex run Silex-Examples/Sources/Physics3D/TerrainCCDScene.sx` or append
`-- --smoke` to verify two complete animated cycles in SDL/Metal.

`Physics3D/BoxTerrainScene.sx` shows a gold/coral stack resting across a flat
terrain seam with the standard friction coefficient of 0.6. The blue box and
its inclined terrain have zero friction to show sliding across five coplanar rows.
The visible faces use the collider grids; alternating tints expose the
triangulation. Press **Space** to disturb the top crate, **R** to restart,
and **Escape** to quit. The sliding box restarts after leaving the terrain.
A compiled binary accepts `--smoke` to check horizontal drift, stack height
and settling over 30 seconds, including three automatic Space impulses, and
all five row identities. Sleeping remains disabled on the three boxes.
From the workspace root or Spec Worktree group root,
run `silex run Silex-Examples/Sources/Physics3D/BoxTerrainScene.sx`.

`Physics3D/CompoundMotionScene.sx` demonstrates kinematic and dynamic compound
contacts: a two-rail lift carries a bridge and crates, a rotating cross pushes
independent crates, and a slightly tilted purple body of two joined boxes falls
onto the floor and turns.
Press **Space** to raise/lower the lift, **P** to stop/start the rotor, **R**
to reset, and **Escape** to quit. The two blue rails belong to one collider;
both support the bridge simultaneously. Every visible leaf follows its body's
physical pose. Pass `--smoke` to the compiled executable for a bounded check
of the lift, rotor, and dynamic compound without manual input.

From the workspace root (or the Spec Worktree group root):

```sh
silex compile Silex-Examples/Sources/Physics3D/CompoundMotionScene.sx --release \
  -o .silex/physics3d-compound-motion-release
.silex/physics3d-compound-motion-release
```

`Physics3D/StressScene.sx` provides two selectable visual loads on plain,
untextured surfaces. `bin` emits colored spheres into a fixed container at
up to 80 per second into an open, horizontal aquarium (10 × 4 × 5 m).
Its 4 cm glass walls, thin seams and fixed three-quarter view keep the contents
visible; the inlet sits above the left side and adds a repeatable lateral
spread so the balls mix across the depth instead of stacking in parallel planes. `column` builds a tall stack
of small boxes above a plain floor. Press **Space** to push the top of the
column, **P** to pause or resume physics, or **Escape** to quit. The on-screen
performance panel reports rendered FPS, frame duration and draw statistics.
A matching panel directly below it displays emitted/target dynamic bodies,
awake bodies, and physics milliseconds per step and per rendered frame,
refreshed once per second. The fixed aquarium walls are
excluded from these body counts. The window title and console also report
these counts, fixed steps per second, mean/peak milliseconds per physics step and steps per
rendered frame. The console also reports physics milliseconds per frame.
Frame duration measures the interval between rendered frames, including
simulation and catch-up steps; it is not a GPU timer. Pausing
physics while the scene keeps rendering helps locate the bottleneck. These
live observations are distinct from the repeatable, renderer-free
`WorldScale` benchmark. The aquarium layout replaces the earlier tall bin;
performance baselines recorded with that old geometry are not directly
comparable to this scene. From the workspace root, compile and run for example:

```sh
silex compile Silex-Examples/Sources/Physics3D/StressScene.sx --release \
  -o .silex/physics3d-stress-scene
.silex/physics3d-stress-scene bin 2048
.silex/physics3d-stress-scene bin 4000
.silex/physics3d-stress-scene column 128
```

The stress scene requests immediate presentation. Dynamic visuals use one
`Scene3D.Instances` group per color; group poses are replaced only after a
physics step or emission has changed them. Bodies remain individually simulated.
The displayed frame interval still includes physics, so a rendered FPS value
with physics paused is not an active-simulation result.

The default aquarium target is 2048 spheres; `column` without a count uses 128.
Counts 32, 64, 128, 256, 512, 1024, 2048, 4000 and 4096 are accepted. Larger choices are
stress experiments rather than a promised interactive frame rate. The
physics-only box-column guard covers 256 boxes; use 128 as the first visual
comparison before increasing the load.

`PhysicsDebugDraw2D` is a live metric diagnostic scene. It applies the
`(0, -9.81) m/s²` world gravity at a fixed 60 Hz and continuously recycles
falling bodies through ramps, a chain, a sensor, and a floor. Its fixed labels
live in a separate retained vector Canvas; the geometric Canvas is rebuilt
only after a physics step. `PhysicsJointDebugDraw2D` places all eight joint
families under the same SI gravity as suspended mechanisms. Both examples
display an FPS panel and accept `--verify` for a bounded motion check followed
by a three-frame hidden renderer smoke.

The focused Physics 2D demonstrations are direct files:

```sh
silex run Sources/Physics2D/BodyControl.sx
silex run Sources/Physics2D/ShapeResponse.sx
```

`BodyControl.sx` visualizes compound mass derivation, an offset center of mass,
an off-center impulse, and a kinematic tray carrying dynamic cargo through
contacts and collider-aware CCD. `ShapeResponse.sx` repeatedly drops a bullet
circle, capsule, rounded polygon, and segment onto polygonal platforms and a
one-sided chain conveyor, exercising the shared contact response and its
material rules.

Both focused demonstrations accept `--verify` on their compiled executable:

```sh
silex compile Sources/Physics2D/BodyControl.sx -o /tmp/silex-body-control
/tmp/silex-body-control --verify
silex compile Sources/Physics2D/ShapeResponse.sx -o /tmp/silex-shape-response
/tmp/silex-shape-response --verify
```

The package consumer tests remain the correctness oracle for the underlying
APIs:

```sh
silex test Tests/Consumer/Tests/BodyControl.sx
silex test Tests/Consumer/Tests/DynamicShapes.sx
```

Run those two commands from the `GFX.Physics` package checkout, and link that
checkout into this workspace before compiling demonstrations against
unpublished package changes.

The calculator accepts mouse input and keyboard calculations. The main number
row and the numeric keypad are supported directly. Use `+`, `-`, `*`, `/`,
`%`, `.` or `,`, then `Enter` or `=`. `Backspace` removes the last digit and
`Escape`, `Delete` or `C` clears the calculator.

Minesweeper is a complete game reconstructed from an earlier Godot project.
Choose a grid from 4×4 through 256×256, a difficulty from 1 through 6, a
preset, or one of the Fit actions, then press **JOUER**. Left-click reveals or
chords, right-click and Shift-left-click toggle a flag, middle drag and
two-axis scroll move large boards, `Page Up`/`Page Down` zoom, `Enter` restarts
with the same settings, and `Escape` returns to the menu. A centered terminal
popup keeps the finished board visible after a victory or defeat, enters with
a scale-and-opacity bounce, and offers **RECOMMENCER** or **MENU**. Its yellow
rounded Canvas pictogram draws a simplified `:D` for victory or tearful `TT`
for defeat without depending on an emoji font. From the parent Silex workspace,
the equivalent explicit command is:

```sh
silex run Silex-Examples/Sources/Games/Minesweeper
```

The source tree includes `--verify` for a hidden deterministic menu, loss,
victory, audio-event, renderer-budget, bundle-finalization, and clean-exit
smoke run.

The game consumes `Board.png`, `Mine.png`, and all five WAV files directly.
The menu and HUD share the bundled `GFX.Font` pixel face exposed by
`Font.Face.pixel()` (Departure Mono, including French accents). `Background.jpg`
is the retained source artwork; its checked-in `Background.png` conversion is
the runtime texture because the current public asset decoder is PNG-specific.

`silex run` discovers the only direct `.sx` file that declares `main` in each
of these directories. `Main.sx` remains a repository convention rather than a
special compiler name. Discovery does not descend into subdirectories; if a
directory contains several entry files, pass the intended `.sx` path
explicitly.

Their `Module.*` imports are explicitly relative to each source directory. The
manifest declares `"sources": "Sources"`, so this physical directory does not
appear in module names: `Sources/Physics2D/FallingBodies/Model.sx` becomes
`Physics2D.FallingBodies.Model` and remains accessible as
`Package.Physics2D.FallingBodies.Model`. You can also enter a demonstration
directory and run `silex run Main.sx`; the parent manifest and its dependencies
remain active.

The Plot gallery presents several pages in sequence. Closing the current
window opens the next page.

`CharacterMover2D.sx` demonstrates a capsule controller across a slope, steps,
a concave corner, an unobstructed trampoline, a light pushable dynamic crate,
ten bouncing balls, and a moving elevator. Arena walls retain dynamic objects,
while fixed-step simulation keeps prop contacts and descending elevator carry
stable. The in-window performance panel tracks current and lowest FPS, frames
longer than 33 ms, maximum frame time, measured physics-step cost, and the
progressive pressure applied while pushing. Balls are light, damped dynamic
supports: the character collides with and can jump from them, while the first
shape-cast contact immediately gives each touched ball enough lead velocity to
yield without letting the capsule pass through it. Sustained pressure spreads
clustered balls around the character.
Because this bounded-speed playground contains no bullet, it uses discrete
collision detection, lets idle props sleep, and caps fixed-step catch-up at
four steps per rendered frame.
Ground acceleration and
deceleration preserve momentum instead of replacing velocity from input; jumps
retain that trajectory at their actual takeoff speed. Air control is expressed
as an acceleration whose influence increases as takeoff momentum decreases.
Vertical jumps therefore remain useful for reaching nearby platforms without
gaining full running speed, and a short coyote window makes platform edges more
forgiving.

`AnalogClock.sx` hosts its retained Canvas content in one
`Application.Bundle`. The `Bundle/` examples cover the three ownership layouts:
`Transitions.sx` replaces window content while shared presentation plugins stay
alive when you press `1` or `2`; `WindowReplacement.sx` replaces a complete
splash window with the main window when you press Enter; and
`MultipleWindows.sx` runs two independently closable windows in the same
Application loop, using `1` and `2` as keyboard shortcuts. These examples
accept `--verify` on their compiled executable to use hidden windows, assert a
bounded run, and stop automatically.

The terminal examples form an intentional progression:
`DedicatedSystemTerminal.sx` owns a dedicated window and lifecycle,
`ComposedSystemTerminal.sx` embeds the shell in a broader interface, and
`ApplicationCommandConsole.sx` exposes application-defined commands without
granting access to the system shell.

The WebView examples illustrate three different approaches:
`EmbeddedWebView/Main.sx` embeds web files, while
`GeneratedHTMLWebView.sx` builds and serializes its document with the `HTML`
package before displaying it. `WebViewBridge.sx` demonstrates bidirectional
communication between JavaScript and Silex.

## Synchronization policy

A demonstration promoted here becomes an application owned by this repository.
It may diverge from the former package example it came from. Sources are not
copied automatically, and changes from this repository must not be blindly
propagated back to a package.

The current migration leaves no `Examples/` directory in any package. Future
focused illustrations belong in their package documentation, automatable
proofs belong in `Tests/`, relevant demonstration applications belong in this
repository, and public performance workloads belong in `Silex-Benchmarks`.

The [`CATALOG.md`](CATALOG.md) file records the origin of the selected examples
and the other visual candidates identified during the inventory.

## Platformer2D

[Pixel Trail](Sources/Platformer2D/README.md) is a small playable platformer using
Kenney's CC0 sprites, retained tile layers, nine-tile terrain patches, merged
collisions and a fixed-step character controller. From the SilexProject workspace
root, run `silex run Silex-Examples/Sources/Platformer2D/Main.sx`.

Use arrows or physical A/D keys to move, Space to jump, R to restart and Escape
to quit. This example exercises the locally linked Scene2D, Physics and Nodes
package changes; use those workspace versions until their next publication.

`Physics3D/ConvexTriangleScene.sx` shows three separate fixed triangles: a
rotating tetrahedron lands, a cube with a shifted local origin rests, and a
cube crosses the back face then lands on the front. Space pauses, R restarts,
Escape exits; the sequence restarts every four seconds. From the workspace
root, run `silex run Silex-Examples/Sources/Physics3D/ConvexTriangleScene.sx`.
