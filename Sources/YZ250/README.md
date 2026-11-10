# Drive the YZ250 with a compact sound bank

The current **H4** prototype uses actual recorded stereo texture in **896 KiB**
of PCM: original attacks and isolated listening test G for settled RPM above
6,000. Hold **Space** to start and open the throttle; release it to close the
throttle. RPM responds automatically. H4 bounds audio peaks and lowers base RPM
to an adjustable 1,800. Load changes the settled take's level; other timbres and
random phrase shifts are excluded from G. The 32-cycle loop still repeats. A dedicated
worker feeds audio independently of GUI rendering. Inertia defaults to
×4 for longer rises; choose ×1 to restore H2's quick response. Load slows acceleration without capping
full-throttle RPM. A fixed-RPM bench is also available.

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

Look for **YZ250 · banque compacte · H4 · ESPACE = gaz**. This entry replaces
the earlier A/B/C grain bench. The spectral procedural P1 experiment remains
separate. Chevrolet 454 and 500 four-stroke sounds are unchanged.

- [Guide français](Docs/FR/README.md)
- [English guide](Docs/EN/README.md)

The recorded loops are pitch-corrected offline and share a continuous crank
phase during playback. They retain multiple recorded firing cycles and noise,
rather than reconstructing a waveform from harmonic parameters. Estimated RPM,
load proxies and listening-driver response are not measured engine dynamics.
Listening approval remains required before generalization.
