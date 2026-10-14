# Data tables

The gallery shows 50,000 stable keyed rows, sorting, widths, selection and editing.
From the workspace or Spec worktree group root:

```sh
silex run Silex-Examples/Sources/UITableView/Main.sx --release
```

- Click a header to cycle ascending, descending and source order; Group and Score demonstrate equal values with stable sorting.
- Drag a header's right edge to change width. Tab also reaches handles; Left/Right, Shift and Home/End adjust width.
- Select then sort: the same key remains selected and its new position is revealed.
- Try filtering, removing/adding 100 and empty data, then restore 50,000 rows. Absent selection remains application-owned.
- Reveal 100 reaches the editable Name cell. Theme changes retain edits and widths.
- Narrow the window to check horizontal scrolling: headers and cells remain aligned, the vertical rail accessible on the right.
- Scrolling is smooth and isolated at boundaries. The toolkit also supports transfer; this gallery retains the requested isolation.

Counters report work performed, without FPS measurements. The CPU path verifies
large collections, sorting, widths, filtering, keyboard and small viewports:

```sh
silex run Silex-Examples/Sources/UITableView/Main.sx --release -- --cpu-check
```

This path creates no window. Separate CPU proofs cover normalized gestures;
no new touch hardware is qualified here.
