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
Sources/FallingBodies/Main.sx
Sources/EmbeddedWebView/Main.sx
Sources/EmbeddedWebView/Web/...
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
silex run Sources/RetainedDocumentViewport.sx
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
silex run Sources/FallingBodies/Main.sx
silex run Sources/RotatingPhysicsContainer/Main.sx
silex run Sources/ShapeGallery2D/Main.sx
```

Their `Module.*` imports are explicitly relative to each source directory. The
manifest declares `"sources": "Sources"`, so this physical directory does not
appear in module names: `Sources/FallingBodies/Model.sx` becomes
`FallingBodies.Model` and remains accessible as
`Package.FallingBodies.Model`. You can also enter a demonstration directory
and run `silex run Main.sx`; the parent manifest and its dependencies remain
active.

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

`RetainedDocumentViewport.sx` preloads 50,000 lines and renders only the
visible rows through `GFX.Font` and `GFX.Canvas`. Its generated source remains
unique per line and rotates through 1,237 glyphs supported by the bundled
monospace face, so the load does not collapse to a tiny ASCII cache. The status
bar reports live FPS, the longest observed frame and the first visible line.
The `--verify` mode pins the submitted Canvas command count below 40, proving
that the 50,000 retained lines are not sent to the renderer. It is a read-only
load probe, not a substitute for a scrollable `GFX.UI.TextArea`: use the
keyboard, mouse wheel or controlled vertical scrollbar to move through the
retained document while evaluating latency. The interactive default uses Scene2D's hinted R8 glyph atlas; a
compiled executable accepts `--vector` for the outline-only comparison and
`--profile-coverage`, `--profile-vector` or `--profile-settle` for bounded
profiles. `--invert-wheel` reverses mouse-wheel navigation while leaving the
platform-normalized direction as the default.

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
