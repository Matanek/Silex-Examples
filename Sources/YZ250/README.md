# Compare the KTM 250 SX recording and the E/G mix

From the `SilexProject/` root:

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

- **Prise originale** plays the recorded throttle blip from 17.85 to 19.55 s.
- **Mix E/G intégral** plays clip H, with E's texture through 1.08 s followed
  by G's sustain. Both buttons use the same volume.
- **Ralenti** starts the idle loop from 6.39–7.31 s of the recording.
- **Space** gives a quick throttle blip. The opening takes about 0.40 s
  before joining H. Releasing Space returns to the slider position.
- **Ouverture des gaz** adjusts throttle. The gentle recording supplies two
  partial-throttle plateaus. At 90% or more, the rise continues into H.
  Returning the slider to zero closes the throttle.
- **M** stops playback. Losing focus releases the throttle.

Both openings use 12.92–14.81 s of the recording. The joins shorten the rise
while each span plays at its original speed. The gentle opening takes about
1 s before joining H if the throttle permits it. This bench uses acoustic
thresholds and loops. A game would supply RPM and its rate of change from its
physics, with load informing texture selection. Use `Build/YZ250-KTM --yz250`
for the Yamaha bench. [Yamaha bench guide](Docs/EN/README.md).

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --release -o Build/YZ250-KTM
Build/YZ250-KTM --ktm-check
```

The check compares generator output with both embedded clips and exercises
the quick opening, both partial plateaus, release and reopening. `PrepareKtm.py`
packs `A-Source.wav`, `H-Mix-E-G.wav` and `Decoded.wav` from the comparison
folder. [Assets/Ktm.json](Assets/Ktm.json) records hashes and audio windows.

- [Guide français](README.fr.md)
