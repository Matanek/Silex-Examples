# Compare the KTM 250 SX recording and the E/G mix

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

- **Prise originale** plays the recorded throttle blip from 17.85 to 19.55 s.
- **Mix E/G intégral** plays clip H, with E's texture through 1.08 s followed
  by G's sustain. Both buttons use the same volume.
- **Space** opens the throttle. The interactive mode joins H's rise, extends
  the plateau while the key is held, then joins the recorded fall. Releasing
  early joins the fall at a nearby cadence. Idle uses 6.39–7.31 s of the same
  KTM recording.
- **M** stops playback. Losing focus releases the throttle.

A long live hold repeats about 0.19 s of the plateau. The KTM mode embeds
826 KiB of stereo PCM. Use `Build/YZ250-KTM --yz250` to launch the Yamaha bench with fixed
RPM and load controls. [Yamaha bench guide](Docs/EN/README.md).

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --release -o Build/YZ250-KTM
Build/YZ250-KTM --ktm-check
```

The check compares generator output with both embedded clips sample by
sample and exercises rise, release, sustain and reopening. `PrepareKtm.py`
packs `A-Source.wav`, `H-Mix-E-G.wav` and `Decoded.wav` from the comparison
folder. [Assets/Ktm.json](Assets/Ktm.json) records hashes and audio windows.

- [Guide français](README.fr.md)
