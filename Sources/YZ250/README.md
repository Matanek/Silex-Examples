# Drive the YZ250 with a compact sound bank

The current **H3** prototype uses actual recorded stereo texture in a **768 KiB**
bank. Hold **Space** to start and open the throttle; release it to close the
throttle. RPM responds automatically. H3 retains H2's recorded sound and feeds it on a
dedicated worker so GUI stalls do not interrupt playback. Inertia defaults to
×4 for longer rises; choose ×1 to restore H2's quick response. Load slows acceleration without capping
full-throttle RPM. A fixed-RPM bench is also available.

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

Look for **YZ250 · banque compacte · H3 · ESPACE = gaz**. This entry replaces
the earlier A/B/C grain bench. The spectral procedural P1 experiment remains
separate. Chevrolet 454 and 500 four-stroke sounds are unchanged.

- [Guide français](Docs/FR/README.md)
- [English guide](Docs/EN/README.md)

The recorded loops are pitch-corrected offline and share a continuous crank
phase during playback. They retain multiple recorded firing cycles and noise,
rather than reconstructing a waveform from harmonic parameters. Estimated RPM,
load proxies and listening-driver response are not measured engine dynamics.
Listening approval remains required before generalization.
