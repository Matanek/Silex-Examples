# Drive the YZ250 with a compact sound bank

The current **H6** prototype schedules recorded pressure packets: throttle
changes their spacing while their time scale stays fixed. It uses G throughout
acceleration and holds, then recorded clacks on closed gas. Idle remains at
native tempo and is not swept as a pitched background layer. Embedded PCM
stays **1.25 MiB**. The previous H5 playback is available for live comparison.

Hold **Space** to start and open the throttle; use the slider for partial gas.
Release Space to return to that slider setting. The RPM scale is indicative,
without tachometer calibration. This is a listening experiment, not a measured
engine simulation.

A dedicated worker feeds audio independently of GUI rendering. Inertia defaults
to ×4 for longer rises; ×1 gives a quicker response. Load slows acceleration
without capping full-throttle RPM. A fixed-RPM bench is also available.

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

Look for **YZ250 · explosions pilotées · H6 · ESPACE = gaz**. This entry replaces
the earlier A/B/C grain bench. The spectral procedural P1 experiment remains
separate. Chevrolet 454 and 500 four-stroke sounds are unchanged.

- [Guide français](Docs/FR/README.md)
- [English guide](Docs/EN/README.md)

Idle keeps native timing; attacks and overrun use offline pitch correction.
The recordings retain multiple real firing cycles and noise,
rather than reconstructing a waveform from harmonic parameters. Estimated RPM,
load proxies and listening-driver response are not measured engine dynamics.
Listening approval remains required before generalization.
