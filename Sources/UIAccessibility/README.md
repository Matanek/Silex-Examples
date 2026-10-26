# Inspect and operate a UI session on macOS

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
events and times handle, update, drawing and IME queries. The rest of the
interval includes rendering, native accessibility, waiting and scheduling; it
is not isolated GPU time. Tracing is optional and preserves the default session.
