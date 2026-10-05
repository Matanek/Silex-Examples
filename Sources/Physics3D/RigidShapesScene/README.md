# Rigid bodies, sweeps and a terrain opening

Run from the workspace root, or the Spec's Worktree group root:

```sh
silex run Silex-Examples/Sources/Physics3D/RigidShapesScene/Main.sx --release
```

In front, the yellow cylinder, blue tapered cylinder and orange tapered
capsule fall onto their platforms. The green sphere crosses the grid opening
and rests on the lower plane. The grid explicitly selects the
`first_to_opposite` diagonal and removes triangles using its masked central
vertex. The physical plane is infinite; its drawing displays a region of the
scene.

In back, three blue volumes — capsule, box and convex hull — travel to their
first collision. Green dots mark contact witnesses. Meshes and the three
queries are prepared once at startup; rendering updates only seven moving
poses. Physics uses a fixed 1/120-second step; rendering interpolates its two
poses.

**Space** pauses, **R** restarts the falls, **Escape** closes the window.
Cycles restart automatically every four seconds. `--smoke` verifies two
cycles then closes its single window; FPS is reported each second. The first
sample includes warmup.

The engine's CCD remains translational at initial orientations. For a
headless witness of its rotational limit:

```sh
silex run Silex-Benchmarks/Sources/Physics3D/RotationLimit.sx --release
```

A 180° rotation during a step misses the wall in both scenarios, including
with parallel translation. Using 36 substeps detects these fixtures; that
count is not a universal rotational CCD guarantee. Physical grids are exact,
immutable and fixed; they do not provide compression, local quantized
updates, or guarantees for arbitrary relief or very large terrain.
