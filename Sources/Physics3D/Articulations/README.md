# Seven manual 3D articulations

Run from the workspace root with the local Physics candidate available:

```sh
silex run Silex-Examples/Sources/Physics3D/Articulations/Main.sx --release
```

The window starts paused. Previous / Next selects a mechanism and returns it
to its initial pose. Click its action button to start or reverse it. Each click
updates a counter and resumes even when paused. Space and the Pause / Resume
button share the same dispatcher; R and Reset restore the selected mechanism
and leave it paused. Escape closes the window. Key repeat is ignored.

| Mechanism | Visible action |
|---|---|
| Cone | A bar pivots to either green angular boundary. |
| Swing / twist | A bar changes its inclination and axial rotation. |
| Six DOF | A bar translates left/right and rotates around its own axis. |
| Gear | Two supported rotors turn in opposite directions at a 2:1 ratio. |
| Rack and pinion | A supported rotor drives a horizontal sliding rack. |
| Pulley | Guided masses move oppositely while their cable keeps its length. |
| Path | An oriented carriage follows a closed Hermite route and reverses. |

Gold denotes the driven body; blue denotes the other body when present.
Green shows cone bounds, guides, the pulley cable or path samples. Live
measurements report position, angle, cable length or constraint phase.

This is a focused constraint demonstration with zero gravity and collision
filters disabled. Bearings and sliders retain the gear, rack and pulley axes.
It does not qualify arbitrary loaded spatial chains, toothed contact or a
complete pulley machine. Physics owns simulation; Scene3D only receives
interpolated poses at 120 Hz. Fixed render pools are created once, reused when
selecting a family, and two body transforms are interpolated per frame, with at most 24 decorative
gear or rack teeth updated from those same poses.
Telemetry refreshes at 10 Hz; UI drawings refresh only when state changes.

The compiled executable accepts `--controls-check` for a window-free event →
button/shortcut → action → motion check of all seven families. `--smoke`
opens a clearly labelled automatic window, verifies bounds, rendered poses,
pause and reversal, then closes after visiting all seven. It exposes no
interactive buttons. Native keyboard feel and visual readability remain a
separate manual check of the default mode.
