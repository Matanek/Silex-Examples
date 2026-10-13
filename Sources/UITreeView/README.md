# Explore a hierarchy with TreeView

The gallery compares 50,000 leaves in twenty folders and a 200-level branch.
Disclosures open or close branches; clicking a row selects its key. Leaf 1000
is an editable field.

From the SilexProject root:

```sh
silex run Silex-Examples/Sources/UITreeView/Main.sx --release
```

Try Up/Down, Left/Right, Home/End and Page Up/Down after Tab or a click.
Selection keeps its keys when branches close; the cursor returns to a visible
ancestor. The checkbox enables multiple selection, with Shift+Up/Down to extend
a range.

Buttons filter folders, reverse their children, remove/restore leaf 1000,
expand/collapse branches and empty/restore the tree. “200 niveaux” reveals the
last row; indentation is capped to preserve the label. “Clair / sombre” preserves
expansion and navigation. The counter reports built row descriptions, not FPS.
Wheel input is smoothed; overflowing fields and the tree isolate their scrolling.

The data index is built when replacing the source. Only rows needed by the
viewport become views. Application state preserves edited values when their
row leaves the viewport; removed editors lose focus. The `Hierarchy` model
retains the parameter snapshot used by its callbacks, following Silex lifetime
rules.

On the compiled binary, `--cpu-check` checks large trees, scrolling, collapse,
mutations, narrow sizes and no new idle descriptions without opening a window.
The actual example's tests also cover GFX key events and theme changes.
`UITreeView CPU : OK` and exit code 0 confirm this path; they do not replace
the user's visual trial.
