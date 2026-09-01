# Silex Examples

`Silex-Examples` gathers visual and interactive demonstrations so they can be
found and launched without browsing each package repository. This repository
is a catalog of standalone applications: focused technical illustrations
belong in documentation, while API proofs remain under `Tests/` in their
owning package.

## Organization

All demonstrations live under [`Sources/`](Sources/). They are neither grouped
by package nor placed in subjective categories such as “showcase”,
“application”, or “interactive”. Each name directly expresses what the
demonstration shows.

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
silex run Sources/GeneratedHTMLWebView.sx
silex run Sources/BoidsSimulation.sx
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
silex run Sources/PhysicsDebugDraw2D/Main.sx --release
silex run Sources/PhysicsJointDebugDraw2D/Main.sx --release
silex run Sources/ShapeGallery2D/Main.sx
```

`PhysicsDebugDraw2D` is a live metric diagnostic scene. It applies the
`(0, -9.81) m/s²` world gravity at a fixed 60 Hz and continuously recycles
falling bodies through ramps, a chain, a sensor, and a floor. Its fixed labels
live in a separate retained vector Canvas; the geometric Canvas
is rebuilt only after a physics step. `PhysicsJointDebugDraw2D` places all
eight joint families under the same SI gravity as suspended mechanisms: spring
mass, pass-through pendulums, servo, soft target, slider, pendulum, rigid welded
pair, and wheel suspension. Continuous targets preserve motion without hiding
the body's inertia. Both examples display an FPS panel and accept `--verify`
for a bounded motion check followed by a three-frame hidden renderer smoke.

The focused Physics 2D demonstrations are direct files:

```sh
silex run Sources/Physics2D/BodyControl.sx
silex run Sources/Physics2D/ShapeResponse.sx
```

Their `Module.*` imports are explicitly relative to each source directory. The
manifest declares `"sources": "Sources"`, so this physical directory does not
appear in module names: `Sources/Physics2D/FallingBodies/Model.sx` becomes
`Physics2D.FallingBodies.Model` and remains accessible as
`Package.Physics2D.FallingBodies.Model`. You can also enter a demonstration
directory and run `silex run Main.sx`; the parent manifest and its dependencies
remain active.

`BodyControl.sx` visualizes compound mass derivation, an offset center of mass,
an off-center impulse, and a kinematic tray carrying dynamic cargo through
contacts and collider-aware CCD. `ShapeResponse.sx` repeatedly drops a bullet
circle, capsule, rounded polygon, and segment onto polygonal platforms and a
one-sided chain conveyor, exercising the shared contact response and its
material rules. The rounded polygon outline includes its physical radius, so
its visible support matches its collider.

Both focused demonstrations accept `--verify` on their compiled executable.
This opens a hidden window, advances a fixed number of deterministic physics
steps, checks the expected outcome, and stops automatically:

```sh
silex compile Sources/Physics2D/BodyControl.sx -o /tmp/silex-body-control
/tmp/silex-body-control --verify
silex compile Sources/Physics2D/ShapeResponse.sx -o /tmp/silex-shape-response
/tmp/silex-shape-response --verify
```

These checks also reject duplicate cargo pairs, a cargo escape, and transient
circle penetration through the conveyor. The package consumer tests remain the
correctness oracle for the underlying APIs:

```sh
silex test Tests/Consumer/Tests/BodyControl.sx
silex test Tests/Consumer/Tests/DynamicShapes.sx
```

Run those two commands from the `GFX.Physics` package checkout, and link that
checkout into this workspace before compiling the demonstrations when testing
unpublished package changes.

The Plot gallery presents several pages in sequence. Closing the current
window opens the next page.

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
