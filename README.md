# Silex Examples

`Silex-Examples` gathers visual and interactive demonstrations so they can be
found and launched without browsing each package repository. This repository
is a catalog of standalone applications: focused technical illustrations
belong in documentation, while API proofs remain under `Tests/` in their
owning package.

This development revision requires the compiler and packages using the single
`Result` API: ordinary calls return the success value or panic, and `try call()`
keeps the `Result` for explicit error handling. Update the toolchain and
packages together before running these sources.

Start with the [retro victory sound](Sources/RetroVictory.sx): four C–E–G–C
notes written in beats at 187.5 BPM with `GFX.Audio.Music`. Choose a customizable
retro timbre, then call `melody.prepare(audio, using:timbre)` once at game loading time and
`audio.play(victory)` when the player wins. No application PCM buffer is needed.
The melody lasts 0.88 seconds, followed by a 30 ms tail. Change the `Music.Note`
values and tempo to adjust the melody, or modify the timbre before preparation.
The demo's `audio.wait` only keeps the standalone program alive; omit it in a
game. From the `SilexProject/` workspace root:

```sh
silex run Silex-Examples/Sources/RetroVictory.sx --release
```

The [procedural audio demonstration](Sources/ProceduralAudio/README.md) plays
beeps, impacts, a laser, an explosion, a changing engine, an 8-bit sound and
melodies composed directly or through MIDI. Select a recipe with `--case` or
verify its PCM and stream without a device using `--check`.

The [World3D FPS scene](Sources/World3D/README.md) demonstrates capsule movement,
variable jumping and automatic stair climbing in a forest.

The [rigid shapes scene](Sources/Physics3D/RigidShapesScene/README.md) shows
cylinders, tapered shapes, capsule/box/convex sweeps, a terrain opening and an
infinite supporting plane in one window.

The [reactive UI form](Sources/UIReactiveForm.sx) demonstrates shared state,
keyed editable rows, keyboard focus and hidden/disabled controls. Enable automatic
reordering, select text in a row, and keep typing: the edit stays with that row.
Tab/Shift+Tab navigate, Space/Enter activate buttons and checkboxes, and arrows
adjust the slider. The custom counter accepts keyboard input without text input.
Columns share offered space independently of text length; the fixed-column toggle
keeps the form at 400 logical pixels. Long field text scrolls internally, following
the caret, and supports wheel scrolling. The form permits up to four rows. `--smoke` on the compiled executable runs a
hidden one-second SDL/Metal rendering check with repeated reordering.

`UIAdaptiveFlow.sx` demonstrates wrapping fractional panels and weighted shrinking
of actions. Resize the window from 900 to 540 and 340 logical pixels to see
three, two and one panels per row. Editing, selection and keyboard focus remain
attached to their field. Keep enough height (820 pixels) for the three rows;
use `UIOverflow.sx` to explore container clipping and `UIScrollView.sx` for scrolling containers.
Its compiled executable accepts `--smoke` to check all three geometries and
render the changing layouts through SDL/Metal for one second.

`UIGrid.sx` compares a 230 px fixed column, an intrinsic content column and a
column sharing the remaining space. Resize the window, edit the fields and use
**Tab** to navigate. **Une seule colonne** switches all three cards to one track
while preserving editing identities. The fields below use 25% and 50% of their
parent's inner width. Fixed tracks may overflow in a very narrow window; grid
tracks do not wrap automatically. From the workspace or Spec group root, run
`silex run Silex-Examples/Sources/UIGrid.sx`.
The compiled executable accepts `--cpu-check` to construct the actual session,
draw both column configurations and exit without opening a window. Run this
check on both Debug and Release builds before testing the graphical demo.

`UIScrollView.sx` combines a vertical document, a nested horizontal card strip,
a nested vertical action panel and editable rows. Scroll with the wheel or drag
the bars, use **Tab**, and try **Voir la dernière ligne** (reveal only) versus
**Éditer la dernière** (reveal and focus). Resize while editing. The inner wheel
scroll bubbles to the document at its limit. Run from the workspace or Spec root:
`silex run Silex-Examples/Sources/UIScrollView.sx`.
Its compiled executable accepts `--cpu-check` to construct, scroll, resize,
reveal and edit the actual session without creating a window or GPU device.
Verify that startup on both Debug and Release builds before the visual test.

[UIOverflow](Sources/UIOverflow.sx) compares wrapping and clipping independently
in a fixed container. Wrapping starts enabled and keeps buttons whole. Disable
wrapping to force overflow, then toggle hidden overflow: it clips the drawing
and pointer targets without moving or shrinking the buttons. Resize while editing
the field; the action counter makes clipped clicks observable. Panel padding
places the normal content and does not add a second clipping rectangle.

### Virtualized project list

`silex run Silex-Examples/Sources/UIListView.sx --release` browses 50,000 projects
with uniform-height composable rows, filtering, reordering, single/multiple
selection and programmatic reveal. Use Tab then arrows, Home/End or Page Up/Down;
Shift extends multiple selection. The builder counter demonstrates bounded row
descriptions while scrolling. `--cpu-check` validates the actual session without
creating a window.

[Play and control a MIDI score](Sources/MIDIPlayer/README.md) with a customized timbre or an integrated instrument. The player owns its audio feeding in standalone and application modes; Space pauses/resumes, S stops and R replays.

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

`Physics3D/ConvexMeshScene.sx` shows convex bodies on three fixed meshes:
a shifted cube slides across planar seams, a cube rests on both valley
slopes, and a rotating tetrahedron lands on the right. Alternating shades
show the actual triangles. Space pauses, R restarts and Escape closes.
From the workspace root, run
`silex run Silex-Examples/Sources/Physics3D/ConvexMeshScene.sx`.

`Physics3D/ConvexCompoundScene.sx` drops two rigid assemblies onto a fixed
mesh: three convex leaves with compensated local offsets on the left, and
a tetrahedron mixed with boxes on the right. The leaves rotate together and
retain individual contact identities. Space pauses, R restarts and Escape
closes the window; the scene restarts automatically every five seconds.
`--smoke` verifies two cycles, contacts, rotation and rendered poses, then exits.
Run from the workspace root:
`silex run Silex-Examples/Sources/Physics3D/ConvexCompoundScene.sx`.

`Physics3D/SphereCastScene.sx` animates six spherical probes against a box edge,
convex corner, sphere, capsule cap, triangle vertex and compound child. The
blue spheres stop at the swept volume's first contact; green dots mark points
on the obstacles. Press **C** to compare a center ray, **Space** to pause,
**R** to restart and **Escape** to quit. From SilexProject, run
`silex run Silex-Examples/Sources/Physics3D/SphereCastScene.sx`.

`Physics3D/HingeScene.sx` shows a gold free pendulum, a blue pendulum limited
to ±0.35 radians with red stop markers, and a green two-link chain with masses
2 and 8 kg. Space pauses, R restarts, L toggles the blue stops, I applies an
impulse with an off-axis component, and Escape closes. From the workspace or
Spec group root, run `silex run Silex-Examples/Sources/Physics3D/HingeScene.sx`.
The compiled binary accepts `--smoke` for two four-second cycles checking
anchors, axes, hard stops, movement and interpolated render transforms.


`Physics3D/HingeMotorScene.sx` shows a gold pendulum driven at 1 rad/s with
40 N·m, a blue one with the same motor and ±0.65 rad stops, and a green one
whose 2 N·m motor cannot overcome gravity to maintain the target speed.
**V** reverses, **M** switches motors on/off, **T** changes the green torque
between 2 and 40 N·m, **L** toggles blue stops, **R** restarts, **Space** pauses,
and **Escape** closes. From the workspace or Spec group root, run
`silex run Silex-Examples/Sources/Physics3D/HingeMotorScene.sx --release`.
The compiled binary accepts `--smoke`: two four-second cycles check target
speed, reversal, insufficient effort, both stops, motor off and rendered poses.

`Physics3D/FixedScene.sx` shows a rigid beam and two loads carried by a
translating and rotating support. D detaches the blue load, C captures its
current pose to reattach it, R resets and Space pauses. From the workspace or
Spec group root, run
`silex run Silex-Examples/Sources/Physics3D/FixedScene.sx --release`.
Its `--smoke` mode checks two complete detach/contact/reattach cycles and
rendered transforms.

`Physics3D/HingePositionScene.sx` compares two torque-limited position motors
without gravity: gold is strongly damped, blue overshoots and oscillates.
Red cubes mark the target of each tip. T reverses targets, R resets, Space
pauses and Escape exits. From the workspace or Spec group root, run
`silex run Silex-Examples/Sources/Physics3D/HingePositionScene.sx --release`.
Its `--smoke` mode checks two eight-second cycles, target reversal, overshoot,
anchor/axis errors, torque bounds, a twelve-frame pause/resume and interpolated
rendered transforms. Space and Escape remain available in both modes.


`Physics3D/HingeFrictionScene.sx` starts two rotors at 2 rad/s without gravity.
Gold brakes to rest while blue rotates freely. F toggles gold friction; R
spins both again with the chosen friction setting. Removing friction from
a stopped rotor leaves it stopped until R provides a new initial velocity.
Space pauses/resumes and Escape exits. From the workspace or Spec group root:
`silex run Silex-Examples/Sources/Physics3D/HingeFrictionScene.sx --release`.
The `--smoke` mode checks two six-second cycles, mutable braking, free
rotation, torque bounds, twelve-frame pause/resume and rendered poses.

## Hinge motors with different directional effort

```sh
silex run Silex-Examples/Sources/Physics3D/HingeTorqueBoundsScene.sx --release
```

Gold and blue rotors start toward +1 rad/s. Press **T** to reverse the target:
gold brakes and reverses more slowly because its negative torque is four
times weaker; blue has equal capacity in both directions. **R** restarts from
rest toward the current target, **Space** pauses/resumes, and **Escape** quits.
The executable's `--smoke` verifies signed acceleration, reversal, reset,
rendered poses and twelve frozen frames followed by resumption in two cycles.

### Soft hinge stops

From the workspace or Spec group root:

```sh
silex run Silex-Examples/Sources/Physics3D/HingeSoftLimitsScene.sx --release
```

Gold yields beyond +/-0.4 rad under motor load; blue has rigid stops at those
angles. Both motors have the same speed and effort. T reverses the target,
R restarts from rest with the current target, Space pauses/resumes, Escape exits.
`--smoke` checks soft deflection, rigid bounds, effort, anchors, reversal, reset,
pause/resume and rendered poses through two cycles.

### Combined hinge angle and velocity

`Sources/Physics3D/HingeCombinedScene.sx` compares two identical servos
(k=8 N·m/rad, c=4 N·m·s/rad, torque ±10 N·m) following thin gray target arms.
Gold receives the sinusoidal trajectory’s angle and velocity, blue only its
angle; gold reduces damping lag. T reverses motion without jumping the target,
R restarts from rest, Space pauses/resumes and Escape exits.

Run from the workspace or Spec group root:

```sh
silex run Silex-Examples/Sources/Physics3D/HingeCombinedScene.sx --release
```

The binary accepts `--smoke`: two eight-second cycles, reversal and reset,
a twelve-frame pause, bounded torque, anchors/axes and rendered poses checked.
Mean tracking error is compared over settled intervals 2–4 and 6–8 seconds,
excluding startup and reversal.

`Physics3D/SliderScene.sx` shows a gold carriage sliding under gravity along an
inclined blue rail. Red stops bound its signed travel to ±2.5 m and the slider
holds its orientation. **T** applies alternating uphill/downhill impulses,
**R** resets, **Space** pauses/resumes and **Escape** closes. From the workspace
or Spec group root, run `silex run Silex-Examples/Sources/Physics3D/SliderScene.sx --release`.
Its compiled executable accepts `--smoke` to check both stops, impulses, reset,
pause/resume, alignment and interpolated ECS poses over two eight-second cycles.

### Slider velocity motor

`silex run Silex-Examples/Sources/Physics3D/SliderMotorScene.sx --release`
starts the carriage uphill at −1 m/s. T cycles uphill/braking/downhill,
F toggles 30/6 N (6 N cannot climb), D enables/disables the drive, R resets,
Space pauses/resumes and Escape quits. Native `--smoke` runs two 12-second
cycles checking both stops, reversal, braking, insufficient capacity,
disable/re-enable, reset, pause/resume and interpolated ECS poses.

### Slider position servo

`silex run Silex-Examples/Sources/Physics3D/SliderPositionScene.sx --release`
compares a critically damped gold carriage and an underdamped blue carriage
on parallel rails. Green markers show the target. T reverses the target,
R resets, Space pauses/resumes and Escape quits. Native `--smoke` verifies
two eight-second cycles, overshoot versus monotonic travel, target reversal,
force bounds, alignment, reset, pause/resume and interpolated ECS poses.

The `UIScrollView.sx` demo includes a “Défilement lissé” checkbox to compare
time-based wheel smoothing with immediate scrolling in the same viewport.
Scrollbar dragging, programmatic moves and focus remain immediate in both modes.
`--scroll-trace` reports host update intervals, wheel packet/drawing counts and
scroll offsets. `SCROLL_ROUTE` compares wheel-event coordinates with the last
mouse position and reports the delta and whether input processing requested a
redraw (`changed`, up to three packets per reporting interval). This flag does
not identify which viewport consumed the event. These are input/cadence
diagnostics, not GPU FPS. The compiled executable accepts `--cpu-check` without
opening a window.

### Slider axial friction

`silex run Silex-Examples/Sources/Physics3D/SliderFrictionScene.sx --release`
shows a gold carriage on an inclined rail. F toggles a 15 N brake, sufficient
to hold the gravity load; T launches alternately uphill/downhill, R restarts,
Space pauses/resumes and Escape quits. Native `--smoke` checks two eight-second
cycles of launch/braking, resting under load, free travel, re-enabling the brake,
reset, force bounds, alignment, pause/resume and interpolated ECS poses.

### Signed slider force bounds

`silex run Silex-Examples/Sources/Physics3D/SliderForceBoundsScene.sx --release`
compares a gold carriage with [-0.5, 2] N and a blue one with symmetric ±2 N.
T reverses target speed, R resets, Space pauses/resumes and Escape quits.
Gold accelerates quickly toward positive speed and reverses more slowly when
negative effort is needed. Native `--smoke` verifies two eight-second cycles,
independent clamped trajectories, signed budgets, alignment, target reversal,
reset, pause/resume and interpolated ECS poses.

### Soft slider stops

`Sources/Physics3D/SliderSoftLimitsScene.sx` compares a gold damped carriage
with a blue undamped one around equal soft bounds. Use the visible **Relancer**,
**Repartir** and **Pause/Reprendre** buttons, or T, R and Space. Each relaunch
sets a ±4 m/s speed in an alternating direction and resumes a paused simulation;
R also resumes after resetting. The panel shows the relaunch count, direction
and pause state. Letter shortcuts follow the logical T/R keys. Escape quits.
`--controls-check` validates events and clicks without opening a window.
`--input-trace` logs received keyboard events for diagnosis. Native `--smoke`
shows a clearly labelled automatic scenario without interactive buttons and
checks two complete spring trajectories through the same relaunch dispatcher;
consumer tests cover keyboard events, clicks and relaunching while paused.

```sh
silex run Silex-Examples/Sources/Physics3D/SliderSoftLimitsScene.sx --release
```

### Slider target tracking with combined position and velocity

```sh
silex run Silex-Examples/Sources/Physics3D/SliderCombinedScene.sx
```

Green markers show a sinusoidal moving target. Gold receives position and
velocity; blue receives position alone and visibly lags. T or Inverser reverses
the target direction and resumes from pause. R or Repartir restarts; Space or
the Pause/Reprendre button pauses/resumes; Escape closes. A counter and status
confirm each command. The UI uses logical T/R letters and ignores key repeat.
`--smoke` is explicitly automatic, with disabled interactive controls, two
cycles and independent physics checks. `--controls-check` runs public event/
button and paused-reversal assertions without a window in Debug/Release.


[UIRadioGroup](Sources/UIRadioGroup.sx) shares a typed exclusive value between
vertical and wrapping horizontal radio groups. Tab visits each group once;
arrows skip disabled options and Space/Enter choose the focused option. Hold a
click to see focus before selection commits on release. Try disabling Domicile,
removing Atelier, clearing the options, and setting the value programmatically:
the user-change counter only records user choices. Resize to wrap the horizontal
group; the whole form scrolls when height is limited. From the workspace or Spec
root run `silex run Silex-Examples/Sources/UIRadioGroup.sx`. The compiled executable
accepts `--cpu-check` and exits before creating a Viewer or GPU device. Check both
Debug and Release startup before trying the graphical demo.


### Seven manual 3D articulations

```sh
silex run Silex-Examples/Sources/Physics3D/Articulations/Main.sx --release
```

A single window selects cone, swing/twist, six DOF, gear, rack/pinion, pulley
and curved path. Start each paused mechanism with its action button. The
counter, status and live measurements confirm actions. Previous / Next and
Reset restore the initial paused pose; actions resume from pause. Space and
the Pause / Resume button share pause; R resets; Escape closes.
[Controls and scope](Sources/Physics3D/Articulations/README.md) ·
[Guide français](Sources/Physics3D/Articulations/README.fr.md).

[UITabs](Sources/UITabs.sx) keeps panel edits and text selection while switching
or reordering tabs. Add and close documents, enable the disabled Help tab, and
resize while editing. The bar is one Tab stop; arrows and Home/End select a tab.
Closing an active panel returns its focus to the bar; restoring a removed panel
creates a fresh editor. Programmatic choices do not increment the user-change
counter. From the workspace root run `silex run Silex-Examples/Sources/UITabs.sx`.
Its compiled executable accepts `--cpu-check` to exercise the actual session
without creating a window or GPU device.

### Loaded spatial hinge

A blue pendulum carries a yellow 2 kg payload one metre outside its rotation
plane through a green fixed attachment. Explicit left/right targets, release
under gravity and a mirrored payload give visible manual actions. It starts
paused; Space and R also have labelled buttons.

```sh
silex run Silex-Examples/Sources/Physics3D/LoadedHinge/Main.sx --release
```

[Controls and scope](Sources/Physics3D/LoadedHinge/README.md) ·
[Guide français](Sources/Physics3D/LoadedHinge/README.fr.md).

[UIPanels](Sources/UIPanels.sx) combines collapsible forms, nested bounded splits
and scrollable document/log panels. Edit and collapse the form, drag the blue
separators, or focus them with Tab and use axis arrows, Shift for a 1 px step,
and Home/End for bounds. Window resize preserves preferred sizes and edits.
The visible counter tracks user gestures; programmatic reset does not increment it.
From the workspace root run `silex run Silex-Examples/Sources/UIPanels.sx`.
The compiled executable accepts `--cpu-check` to check the actual session
without opening a window or creating a GPU device.

## Rack servo and rail stops

A yellow pinion drives a blue rack to both finite rail stops. Explicit left,
right and center buttons resume the initially paused simulation; Space pauses
and R resets it. The display distinguishes movement from a motor pushing a stop.

```sh
silex run Silex-Examples/Sources/Physics3D/RackServo/Main.sx --release
```

[Controls and scope](Sources/Physics3D/RackServo/README.md) ·
[Guide français](Sources/Physics3D/RackServo/README.fr.md).


[UIOverlays](Sources/UIOverlays.sx) demonstrates four anchored popovers, a delayed
tooltip, retained editing and nested modal dialogs. Resize or scroll an anchor;
Escape closes the topmost surface, outside clicks dismiss popovers and modal
focus remains confined. From the workspace root run
`silex run Silex-Examples/Sources/UIOverlays.sx`. The executable accepts
`--cpu-check` to click each popup anchor, submit/close its contents and open
nested modals in its real session without a window or GPU. Persistent popup
actions bind an owned model; they do not borrow locals from the view factory.


[UISelect](Sources/UISelect.sx) demonstrates typed dropdown choices, tentative
keyboard navigation, cancellation and 50,000 virtualized project options.
Reorder or filter the source; programmatic changes update the label without
echoing callbacks. Run `silex run Silex-Examples/Sources/UISelect.sx` from the
workspace root. The executable accepts `--cpu-check` to exercise actual pointer
and keyboard paths, source changes and resizing without a window or GPU.
Use `--cpu-profile` to measure construction, closed/open idle frames and popup
scrolling in the same session, also without a window or GPU. These timings cover
UI update and Canvas command recording, not displayed GPU frames.

[UIComboBox](Sources/UIComboBox.sx) compares a closed Select and editable typed
suggestions, an explicit free-text conversion, and filtering 50,000 projects.
Try Unicode input, cancellation, fixed-width long text and resizing with the
popup open. From the workspace root run
`silex run Silex-Examples/Sources/UIComboBox.sx --release`. The executable accepts
`--cpu-check` and `--cpu-profile` without opening a window.

[UIMenus](Sources/UIMenus.sx) shares commands across menus, nested submenus,
contextual menus, a wrapping toolbar and Cmd/Ctrl shortcuts. Disable Save to
check shared availability; use arrows, Escape and Tab or secondary-click the
editor panel. From the workspace root run
`silex run Silex-Examples/Sources/UIMenus.sx --release`. The executable accepts
`--cpu-check` to exercise its interaction and tiny-resize paths without a
window or GPU.

Run the same compiled UIMenus executable with `--system-menu` for the optional
macOS application menu bar; omit this argument to keep menus in the page. The
`--cpu-check --system-menu` route exercises composition without starting video.

### Hinge stop impacts

A paused manual scene lets you launch and reverse a free rotor or a position
motor between two angular stops. Slow playback and retained before/after
braking speeds make the first stop response observable; Space/R and explicit
buttons control pause and reset.

```sh
silex run Silex-Examples/Sources/Physics3D/HingeImpact/Main.sx --release
```

[Controls and scope](Sources/Physics3D/HingeImpact/README.md) ·
[Guide français](Sources/Physics3D/HingeImpact/README.fr.md).

### Two perpendicular hinges under load

A blue arm turns about a red Z pivot; its gold payload turns about a green X
axis. Visible button pairs raise/lower each part separately, with target angles,
command feedback, braking, pause and reset. The scene starts paused.

```sh
silex run Silex-Examples/Sources/Physics3D/SpatialHinges/Main.sx --release
```

[Controls and scope](Sources/Physics3D/SpatialHinges/README.md) ·
[Guide français](Sources/Physics3D/SpatialHinges/README.fr.md).

### Custom focus feedback

[UIFocusAppearance](Sources/UIFocusAppearance.sx) compares configurable outlines,
underlines, backgrounds and invisible feedback while retaining keyboard focus.
Use Tab/Shift+Tab, F2 to change feedback while editing, and F3 to switch local
light/dark palettes. One field has its own purple outline. These palettes are
explicit description styles, not a theme cascade. From the workspace root run
`silex run Silex-Examples/Sources/UIFocusAppearance.sx --release`.
Short choice popups fit their options; the 30-project ComboBox caps its popup
at 160 px and shrinks while filtering.
The compiled executable accepts `--cpu-check` to exercise the gallery without
opening a window.

## Spatial contact with manual release

Lower the gold sphere onto the plane, observe its contact marker and stopped
motor command, then lift it free. Buttons acknowledge each action; Space/R
and pause/reset buttons remain available. This manual test concerns visual
clarity and interaction; mechanical balances are qualified separately.

```sh
silex run Silex-Examples/Sources/Physics3D/SpatialContacts/Main.sx --release
```

[Controls and scope](Sources/Physics3D/SpatialContacts/README.md) ·
[Guide français](Sources/Physics3D/SpatialContacts/README.fr.md).

## Vertical slider carried by a hinge

[SpatialRail](Sources/Physics3D/SpatialRail/README.md) holds a blue arm and
raises/lowers an offset gold sphere on a green vertical rail. Buttons expose
floor contact, release, braking and pause; travel and target appear in centimeters.
From the workspace root or owning Spec group run
`silex run Silex-Examples/Sources/Physics3D/SpatialRail/Main.sx --release`.
[Guide français](Sources/Physics3D/SpatialRail/README.fr.md).

## Shared UI themes

[Sources/UIThemes.sx](Sources/UIThemes.sx) demonstrates inherited light/dark palettes, local overrides,
selection/error/disabled states, menus, choices and custom Canvas content. F2
changes the theme and F3 toggles input errors while preserving editing and focus.
Run with `--cpu-check` to validate without opening a window.

## Three swing/twist servos under load

[LoadedSwingTwist](Sources/Physics3D/LoadedSwingTwist/README.md) drives a gold
2 kg offset load around a fixed white pivot. Colored motor axes expose the
compound rotation; explicit opposite targets, recentering, pause and reset
show finite-spring equilibrium under gravity. From the workspace root or
owning Spec group run
`silex run Silex-Examples/Sources/Physics3D/LoadedSwingTwist/Main.sx --release`.
[Guide français](Sources/Physics3D/LoadedSwingTwist/README.fr.md).

[UIVisuals](Sources/UIVisuals/Main.sx) compares all five image fits, icon actions,
bound and indeterminate progress, and a retained application plot. Use F2 to
change theme, F3 to pause, F4 to hide the animated group, and edit the text while
resizing. Icon actions share a counter across a button, menu and toolbar.
From the workspace or Spec group root:

```sh
silex run Silex-Examples/Sources/UIVisuals/Main.sx --release
```

The compiled executable accepts `--cpu-check` to run 120 sample updates, theme
changes and narrow resizes, proving retained descriptions, measurements and
editing selection without opening a window. Check both Debug and Release
builds before trying the graphical gallery.

## Loaded shoulder and elbow

[ArticulatedPose](Sources/Physics3D/ArticulatedPose/README.md) combines a
three-axis shoulder with a bending elbow, two 2 kg members, a fixed white
pivot and a moving cyan elbow. Opposite poses, recentering, pause and reset
show the elbow’s local frame and gravity-loaded elastic equilibrium. From
the workspace or owning Spec group root run
`silex run Silex-Examples/Sources/Physics3D/ArticulatedPose/Main.sx --release`.
[Guide français](Sources/Physics3D/ArticulatedPose/README.fr.md).


## Text history and word navigation

[UITextEditing](Sources/UITextEditing/README.md) combines short, long and multiline
fields with grouped undo/redo, Unicode word movement and selection, retained
history across theme changes and automatic caret scrolling. From the workspace
or owning Spec group root run
`silex run Silex-Examples/Sources/UITextEditing/Main.sx --release`.
The compiled executable accepts `--cpu-check` for a windowless Debug/Release
check. [Guide français](Sources/UITextEditing/README.fr.md).

## Ragdoll hierarchy and independent poses

[RagdollPose](Sources/Physics3D/RagdollPose/README.md) creates two ten-part
mannequins from one hierarchy. Change the gold mannequin's pose while the blue
one remains a reference, then release both into a short physical free fall.
Pause, replay and reset expose the joint frames and assembly lifetime. From
the workspace or owning Spec group root run
`silex run Silex-Examples/Sources/Physics3D/RagdollPose/Main.sx --release`.
[Guide français](Sources/Physics3D/RagdollPose/README.fr.md).

## Ragdoll fall and impulse

[RagdollFall](Sources/Physics3D/RagdollFall/README.md) reuses the ten-part anatomy
with anatomical joint limits, nonadjacent internal collisions, a visible floor
and an off-center impulse on the gold torso. Blue provides
a reference fall. Release/replay, impulse, pause and reset work through buttons
and logical keys; simulation pauses automatically after four seconds.
From the workspace or Spec group root:
`silex run Silex-Examples/Sources/Physics3D/RagdollFall/Main.sx --release`.
[Guide français](Sources/Physics3D/RagdollFall/README.fr.md).

## Ragdoll motorized pose tracking

[RagdollDrive](Sources/Physics3D/RagdollDrive/README.md) initially holds two ten-part
mannequins by their fixed torsos. Gold follows selected targets with bounded
motors; blue holds neutral. Push gold's forearm, release its motors and resume
the selected target, while anatomical limits and internal collisions remain
active. T switches between suspension and mobile torsos falling onto a physical
floor, where target efforts interact with contacts. 3 requests elbow/knee
angles beyond their stops to observe the physically bounded gesture. B launches
a red block towards the mobile torso on the floor or exposed limbs in suspension;
C selects frontal, left/right oblique or rear shots. Flight and measured contacts transfer the
impact to the joints. Pause and recreation are
available. This does not demonstrate standing balance.

K lifts gold kinematically and releases it with its current velocity so gravity
and floor contacts take over; Space also pauses the lift.
`silex run Silex-Examples/Sources/Physics3D/RagdollDrive/Main.sx --release`.
[Guide français](Sources/Physics3D/RagdollDrive/README.fr.md).


## Hierarchical data trees

`Sources/UITreeView/Main.sx` explores 50,000 leaves and a deep branch with
stable selection, disclosure controls, hierarchical keyboard navigation,
filtering, mutation and an editable row. Wheel scrolling is smoothed and the
counter reports constructed row descriptions. [Guide](Sources/UITreeView/README.md).

`silex run Silex-Examples/Sources/UITreeView/Main.sx --release`.

## Sortable data tables

`Sources/UITableView/Main.sx` explores 50,000 keyed rows with stable sorting,
resizable columns, single/multiple selection, filtering, themes and an editable
cell. Headers remain fixed vertically and both rails remain visible. Counters
report cell descriptions and comparisons, without FPS claims.
[Guide](Sources/UITableView/README.md). From the workspace or Spec group root:
`silex run Silex-Examples/Sources/UITableView/Main.sx --release`.
Use `-- --cpu-check` for the pure CPU path without opening a window.

## Powered driving, steering and suspension

[VehicleSuspension](Sources/Physics3D/VehicleSuspension/README.md) drops a 100 kg
chassis onto four suspended wheels. B jumps, C overloads for two seconds, Space
pauses and R recreates. Green pads show support lost in flight and regained on
landing. P pushes forward and spins passive tires through ground contact; V
pushes sideways to test lateral grip. G recreates the vehicle with zero tire friction
for a sliding comparison. White hub bars show physical rotation, a yellow strip
marks the front, and the following camera keeps the metric ground grid visible.
Left/right arrows select maintained front-wheel steering; Up centers it. F toggles
the service brake, H the rear handbrake. R/G release brakes and center steering.
The rendered wheels follow their physical steering angles. Z selects maintained forward throttle, S reverse, and X releases throttle.
A 30 N·m engine drives the rear wheels through an automatic gearbox; RPM,
gear and clutch are visible. The no-grip comparison retains rotors with zero
friction curves, so powered wheels spin without propelling the chassis. R/G
also release throttle.

A purple raised band compares per-wheel ray and sphere contacts. Sphere mode
starts selected: Z crosses the band and lifts the chassis. T recreates with
rays, which miss its edges; repeat Z to compare. The band and motor stay the
same. The contact button shows the mode; R/G preserve it. The swept 12 cm
sphere approximates contact volume, while wheel radius remains 30 cm.

`silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release`.
[Guide français](Sources/Physics3D/VehicleSuspension/README.fr.md).
