# YZ250 procedural listening prototype

Generate a single-cylinder two-stroke sound without reading or embedding audio
samples. The supplied YZ250/FMF recording is used only for offline spectral
calibration. Test fixed RPM first, then slow/fast sweeps and continuous high-RPM
holds. Chevrolet 454 and 500 four-stroke sounds remain unchanged.

```sh
silex run Silex-Examples/Sources/YZ250Procedural/Main.sx
```

Run from the `SilexProject/` root. Look for **YZ250 · procédural intégral · P1**;
this is separate from the earlier sample-grain A/B/C prototype.

- [Guide français](Docs/FR/README.md)
- [English guide](Docs/EN/README.md)

The prototype is awaiting listening approval; acoustic calibration and automated
stability checks do not establish perceptual realism.
