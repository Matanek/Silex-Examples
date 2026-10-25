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
