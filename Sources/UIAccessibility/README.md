# Inspect and operate a desktop UI session

This interactive example presents a **Nom** field, a **Valider** button,
checkboxes, a **Profil** radio group, a **Volume** slider and a **Fichiers** panel
containing a small tree. Feedback lines display their values. It passes the
session directly to Viewer, with no additional accessibility wiring in
application code.

The **Masquer les contours des cases et radios** button compares the default
outline with `FocusAppearance.none()`. It applies to both checkboxes and the
radio group; the slider keeps its usual focus setting. Navigation and activation
remain available. The dark theme provides light labels against the Viewer
background, and the page scrolls when the window is too small.

From the workspace root, using the development toolchain supporting protocol
method bodies:

```sh
silex run Silex-Examples/Sources/UIAccessibility/Main.sx --debug
```

In the macOS accessibility inspector, find **Nom** with its text-field role and
**Ada** value, then **Valider** with its button role. Editing or activating them
through the tool must update the same feedback lines as mouse or keyboard
input. With VoiceOver, check label/value reading, focus navigation, typing and
activation. Move or resize the window to check the exposed geometry.

The button/text-field path has been confirmed with the inspector and VoiceOver.
To qualify the new controls:

1. Activate **Notifications**: its checked state and visible feedback change.
2. Choose **Énergique** in **Profil**: exactly one option is checked;
   **Indisponible** remains disabled.
3. Adjust **Volume**: initial value 12, minimum 10, maximum 20; increment and
   decrement actions update the same state as mouse dragging.
4. Check **Verrouiller le volume**: the slider becomes disabled and rejects
   changes; uncheck it to restore adjustment.
5. Toggle **Notifications** again, then return to the group and slider:
   references remain usable after the interface is reevaluated.

The **Fichiers** panel contains **Documents** (two children) and **Images**.
Expand Documents, select Notes, then collapse and reopen the panel to compare
visible state with the semantic source. An accessibility client can also change the
selected/expanded attributes when the actions are advertised. The **Nom**
field references its visible title, which refers back to the field.

Headless tests cover these actions and rejection of disabled actions. They do
not qualify the new controls with VoiceOver or the Linux/Windows bridges.

`--cpu-check` verifies the model and semantic actions without a window. It does
not verify attachment to a real window or VoiceOver.

## Inspect a Unicode selection

The **Message Unicode** field contains `Aé👩‍💻中Z` followed by a second line.
Select the combining accent, emoji or multiple lines to compare highlighting
with selection properties exposed to the system. Native indices count UTF-16
units; the toolkit keeps complete graphemes. Typing replaces the selection
and Cmd+Z restores the text on macOS.

CPU mode verifies this edit and undo through session events after selection
through the semantic source. Separate AppKit tests verify native conversion;
this mode does not replace inspection in a real window.

## Check presentation placement

The `--placed` mode places an adaptive page with room for its offset. Its
origin uses `position:Math.Vec2(24.0, 16.0)` and `anchor:Math.Vec2(0.05)`. In a 780 × 820
window, its origin is therefore at (63, 57) logical units; resizing moves it
with the anchor and adapts its size to the available space. Elements remain
described in drawing coordinates.

Launch the binary with `--placed`, click Name and Message Unicode, select text
and scroll the page with the wheel. Mouse targets and selection highlighting
should follow the offset content. In the inspector, a field’s rectangle should
match the control before and after moving or resizing the window. If an input
method displays candidates, their area should stay near the caret.

CPU mode also checks that the page and field stay inside the window across
four successive layouts and that the title is visible on startup. It does not
prove this correspondence in a real window.

## Inspect collection dimensions

At the bottom of the page, **Équipe** contains three rows and two columns:
**Personne** and **Domaine**. The inspector should show these dimensions on the
table, an index on each row, and row/column ranges of length 1 on its cells.
Indices start at 0. Clicking a row updates **Personne sélectionnée**; native
selection uses the same state.

In **Fichiers**, Documents and Images have native level 0. After expansion,
Notes and Rapport have level 1. Their row position in the model differs from
their order among the children of Documents.

CPU tests verify table data and selection. The GFX package’s AppKit tests
verify native properties and lazy queries over 50,000 rows. Complete
screen-reader navigation of collections remains to be qualified.

The table displays a continuous separator between its two columns. The last
column uses the available space (`stretch_last_column:true`), removing the
appearance of an empty column on the right. Resize handles appear on hover
or focus; the divider remains visible through the rows. CPU mode verifies
the same data and actions.

`full_height_resize:true` is enabled in Équipe. Hover and drag the separator
between Personne and Domaine from a row or the empty space below the rows to
resize the first column without selecting a row. The handle and its feedback
cover the body; the same handle remains available in the header and from the
keyboard. The toolkit default stays false for header-only resizing.

The inspector can now request rows through `AXRows`, excluding headers and
wrappers, and request a table cell by its coordinates. The hierarchy and indexed
access use the same identities. CPU mode checks this relationship on Équipe;
AppKit tests verify its native translation without a window. These proofs do
not replace a screen-reader path.

## Gesture CPU profile

The volume label directly uses `Text(volume, format:...)`: moving the slider
updates this text without rebuilding the entire form. Actions, locking and
the accessible source retain the same state.

[InteractionProfile.sx](InteractionProfile.sx) replays slider and column gestures
on this same model without a window. It separates input, drawing, Canvas
preparation and accessibility notifications, with and without observation of
the entire tree. Its measurements cover CPU work; they measure neither the GPU,
presentation nor window FPS.

The profile accepts `--bursts` to compare one and eight motions per drawing,
including the host’s IME target queries. This complements the one-position-per-
drawing profile; toolkit tests check layout counts separately.

`PresenterProfile.sx` replays slider and scrolling separately, with and without
observing the accessible tree. It times input, accessibility synchronization
before drawing, drawing, Scene2D Canvas replacement and synchronization after
drawing, in Viewer's order. This remains a CPU profile and opens neither a
window nor a GPU device.

`SessionProfile.sx` replays the same gestures through `Canvas.Session` and the
presenter's complete events. Its `--trace` option also retains the
`TraceSession` wrapper. Use this variant to compare the contract actually held
by the host: retaining a source or session through a protocol can change cycle
collector traversal. Compare frozen executables with identical options; this
CPU profile does not prove the window's FPS.

`ScalingProfile.sx` separately measures 64 idle updates and 64 single-state
mutations with 16, 128 and 1,024 bound labels mounted in a ScrollView. It counts
formatting calls and times phases after mounting and warmup. `--check-cache`
asserts zero idle formatting calls and one per local mutation. This CPU profile
opens no window or GPU device; it does not by itself qualify a complete
application, a virtualized collection or rendering. `--stages` separates update
and drawing times, compares mutations of the first and last label and counts
recorded text commands. This instrumented variant is for attribution; compare
identical options.

`ColumnResizeProfile.sx` replays column resizing through `Canvas.Session`,
full events and Viewer-style IME queries, without a window or GPU. It compares
one and eight motions per drawing, with and without accessibility observation,
on the placed demo and a 50,000-row/six-column table. Observation of the large
table is limited to the first eight children at each level. It counts cell
descriptions and separates input, accessibility before/after drawing, UI drawing
and Scene2D replacement. Compare identical cases and frozen binaries; CPU-only
wall times do not establish window FPS.

## Measure window phases

`--trace-frame` enables Viewer’s collector while retaining the ordinary session
and source. It takes precedence over `--trace-drag` when both are supplied.
`ui_frame_trace` CSV is written to stdout after closing. Redirect stdout to a
file, reach the Team table, drag its separator quickly for a few seconds and
close the window. The ring retains the latest 8,192 frames.

`update_ms` covers Viewer, session and accessibility work during update;
`prepare_ms` then covers Scene2D preparation. `submit_ms` covers rendering,
submission and CPU waits, without isolating GPU execution. `poll_pre_ms` covers
polling/pre-update and the inter-frame remainder, including remaining marker
cost. Motion/wheel and command counters distinguish input bursts, preparation
and waits. Comparing a native trace with a CPU replay does not qualify untraced
FPS; it provides attribution evidence.

## Trace the real window

The demo displays FPS in its title, both normally and with `--placed`, with or
without tracing. The average render-loop rate updates at most twice per second
and includes the real elapsed time of long stalls.

`--trace-drag` retains the latest 4,096 loop samples in memory and writes CSV to
stdout after the window closes. Redirect stdout to a file when launching the
binary. Move the slider and then the separator, and close the window to obtain
the trace.

`interval_ms` measures elapsed time between updates; `delta_ms` is the delta
provided by Viewer, clamped to 100 ms by the application. The trace counts
events and times handle, update, drawing and IME queries. `source_queries` counts
calls to the accessible Source and its row views; `source_ms` measures their
combined duration, including the timers used by this optional trace.

To assess fluidity, first run the demo without `--trace-drag`: FPS remain
visible. The diagnostic wrapper retains additional references and adds timers;
its overhead can be noticeable. Enable it afterwards to locate a slowdown,
comparing runs that use the same option.
The rest of the interval includes rendering, native work outside the Source, waiting and scheduling; it
is not isolated GPU time. Tracing is optional and preserves the default session.

## Complete macOS qualification

Add `--complete` to an interactive launch to show Navigation/Préférences tabs,
Select/ComboBox, menu, toolbar, help and dialog. The Équipe table has a sortable
Personne column. Keep `--placed` to exercise a shifted presentation origin.

In the inspector, check columns, headers and sorting, tree selection/disclosure,
tabs and modal dialog. Query text spans and positions with combining accents
and emoji, including after scrolling. Use VoiceOver to check reading/actions
on these new paths; CPU and headless AppKit checks do not replace that system
run. The previously confirmed button/field path needs no identical retest.
`--cpu-check` keeps its output and additionally checks tabs, columns and dialog
cancellation without opening a window.

## Linux — experimental AT-SPI bridge

The same demo exercises the Linux bridge. ARM64 and x64 cross-builds from the
Mac verify emission and linking; they do not qualify a Linux desktop or Orca.
The Windows UI Automation bridge remains in preparation.

On a Linux machine with a graphical session, the `libdbus-1` library and the
`org.a11y.Bus` session service, launch the matching Linux binary with
`--complete --placed`. Launch is manual: headless tests on the Mac do not imply
native Linux testing.

Use an AT-SPI client to check names, roles, disabled states and actions for the
same controls. Also check tabs, lists, tree disclosure, table headers and cells,
and opening and closing the dialog. With Orca, qualify navigation, change
announcements and Unicode editing. Native AT-SPI text positions count Unicode
scalars; editor selections preserve whole graphemes.

Test placement, resizing and different scales on X11, then Wayland. An unknown
screen position on Wayland remains unavailable; relative coordinates must not
be turned into a fabricated global position. Closing the window while a client
retains objects must make them unavailable without crashing either process.

For a new build from the development workspace:

```sh
silex compile Silex-Examples/Sources/UIAccessibility/Main.sx --target linux-x64 --debug --output /tmp/ui-accessibility-linux-x64
```

Replace `linux-x64` with `linux-arm64` for ARM64. These remain experimental
candidates until this native qualification is completed.

## Windows — experimental UI Automation bridge

ARM64 and X64 builds from macOS prove emission and linkage, not Windows execution
or Narrator navigation. These tests require the development compiler with native
C entries and their records. From the workspace root, build for the tester’s
architecture:

```sh
silex compile Packages/GFX/Tests/Accessibility/Windows.sx --target windows-x64 --debug --output /tmp/WindowsUIA-CPU-x64.exe
silex compile Silex-Examples/Sources/UIAccessibility/Main.sx --target windows-x64 --debug --output /tmp/UIAccessibility-Windows-x64.exe
```

Copy both files to Windows and run them in PowerShell:

```powershell
.\WindowsUIA-CPU-x64.exe
.\UIAccessibility-Windows-x64.exe --complete --placed
```

Replace `x64` with `arm64` for ARM64. The headless fixture expects
`Windows UIA CPU protocol: passed`, followed by exit code 0. It checks COM
identity and references, native arrays, callbacks from a native thread, Unicode
BSTRs with BOM/NUL, and unavailability after detachment.

Use Inspect or Accessibility Insights for structure, then Narrator for actual
navigation. Check these paths:

1. Read Nom/Ada and its label, change the name through ValuePattern, invoke
   Valider: one visible change per action.
2. Toggle Notifications, select Énergique, set Volume between 10 and 20, then
   lock it: RangeValue remains readable while mutation is rejected.
3. Open Documents, select Notes, collapse/reopen: identities and events remain
   consistent with visible values.
4. Inspect Équipe: two columns, three rows, headers and editable cells. GetItem
   requests one cell; reading its value does not require its mounted child.
5. In Unicode text, read, search, move anchor/caret by grapheme, word and line,
   and check visible rectangles. Top/bottom ScrollIntoView reveals a range
   without changing focus or selection; after editing, a retained range stays
   clamped to current content.
6. Move/resize the window and change display/scale (100/150/200%): hit testing
   and rectangles match visible controls, including with `--placed`.
7. Act through the client after the window has been idle: visible feedback
   appears without moving the mouse.
8. Close while retaining UIA references, including during a callback: subsequent
   calls become unavailable without a crash or hang.

Record architecture, Windows version, scale, client/reader, commands, binary
hashes, action and expected/observed results, with logs. Attributes remain
plain-text attributes; retained ranges do not follow moves through edit anchors.
A custom Source supplies text geometry and reveal operations for the corresponding
requests. The bridges remain experimental until these native checks are complete.
