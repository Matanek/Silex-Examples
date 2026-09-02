# Silex Examples

`Silex-Examples` gathers visual and interactive demonstrations so they can be
found and launched without browsing each package repository. This repository
is a catalog of standalone applications: focused technical illustrations
belong in documentation, while API proofs remain under `Tests/` in their
owning package.

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
Sources/FallingBodies/Main.sx
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
silex run Sources/FallingBodies
silex run Sources/RotatingPhysicsContainer
silex run Sources/ShapeGallery2D
silex run Sources/Apps/Calculator
silex run Sources/Games/Minesweeper
```

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
a scale-and-opacity bounce, and offers **RECOMMENCER** or **MENU**. It uses the
pixel face's celebration or crying emoji when covered and a crisp ASCII face
otherwise. From the parent Silex workspace, the equivalent explicit command is:

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
appear in module names: `Sources/FallingBodies/Model.sx` becomes
`FallingBodies.Model` and remains accessible as
`Package.FallingBodies.Model`. You can also enter a demonstration directory
and run `silex run`; the parent manifest and its dependencies remain active.

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
