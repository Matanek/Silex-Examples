# Compare the KTM 250 SX recording and the E/G mix

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

- **Prise originale** plays the recorded throttle blip from 17.85 to 19.55 s.
- **Mix E/G intégral** plays clip H, with E's texture through 1.08 s followed
  by G's sustain. Both buttons use the same volume.
- **Ralenti** starts the idle loop from 6.39–7.31 s of the recording.
- **Space** opens the throttle. The opening uses 12.92–14.81 s at its recorded
  speed, then joins H's rise. Holding Space extends the plateau. Releasing
  during the opening returns to idle. After the join, release selects a nearby
  cadence in the recorded fall.
- **M** stops playback. Losing focus releases the throttle.

A long live hold repeats about 0.19 s of the plateau. The KTM mode embeds
1.12 MiB of stereo PCM. Use `Build/YZ250-KTM --yz250` to launch the Yamaha bench with fixed
RPM and load controls. [Yamaha bench guide](Docs/EN/README.md).

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --release -o Build/YZ250-KTM
Build/YZ250-KTM --ktm-check
```

The check compares generator output with both embedded clips and the recorded
opening between joins, sample by sample. It also exercises release, sustain
and reopening. `PrepareKtm.py`
packs `A-Source.wav`, `H-Mix-E-G.wav` and `Decoded.wav` from the comparison
folder. [Assets/Ktm.json](Assets/Ktm.json) records hashes and audio windows.

- [Guide français](README.fr.md)
