# Drive the YZ250 with a compact sound bank

The current **H5** prototype adds nearby recorded idle and closed-throttle
clacks from `2018_Yamaha_YZ_250x.mp3`, keeping isolated G for settled upper RPM.
Hold **Space** to start and open the throttle; release it for a progressive,
audible overrun. Base control 1,800 plays the idle take at native tempo; the
scale is not tachometer-calibrated. Embedded PCM totals **1.25 MiB**.

A dedicated worker feeds audio independently of GUI rendering. Inertia defaults
to ×4 for longer rises; ×1 gives a quicker response. Load slows acceleration
without capping full-throttle RPM. A fixed-RPM bench is also available.

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

Look for **YZ250 · ralenti / retombée · H5 · ESPACE = gaz**. This entry replaces
the earlier A/B/C grain bench. The spectral procedural P1 experiment remains
separate. Chevrolet 454 and 500 four-stroke sounds are unchanged.

- [Guide français](Docs/FR/README.md)
- [English guide](Docs/EN/README.md)

Idle keeps native timing; attacks and overrun use offline pitch correction.
The recordings retain multiple real firing cycles and noise,
rather than reconstructing a waveform from harmonic parameters. Estimated RPM,
load proxies and listening-driver response are not measured engine dynamics.
Listening approval remains required before generalization.
