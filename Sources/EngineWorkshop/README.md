# Shape a vehicle sound signature

Choose a vehicle, start it and hold **Space** to rev. **M** or the button toggles
ignition. The workshop uses GFX.Audio’s procedural parts generator; it needs
no bank of recordings.

From the `SilexProject/` root, select the local package and build:

```sh
silex link Packages/GFX.Audio --workspace Silex-Examples
silex compile Silex-Examples/Sources/EngineWorkshop/Main.sx --release -o Build/EngineWorkshop
Build/EngineWorkshop
```

## Choose a vehicle

The menu supplies 17 profiles:

- 1.0 L three-cylinder petrol, 1.4 L four-cylinder petrol and 1.6 L turbo diesel city cars;
- 2.0 L turbo I4, 3.2 L flat-six, 5.0 L cross-plane V8, 5.2 L V10 and 6.0 L V12 sports cars;
- 125, 250 and 500 cc two-stroke, and 250 and 500 cc four-stroke motocross bikes;
- 1,000 cc inline-four and grouped-firing V4 race motorcycles;
- 1,200 and 1,800 cc custom/chopper V-twins with 315°/405° firing intervals.

GTI, 911, Mustang, R8, Ferrari and Harley labels describe sonic inspirations,
not certified replicas of commercial models. Profiles and synthesis belong to
`GFX.Audio.Synthesis.EngineVehicles`.

## Hear the controls

**Total displacement** is entered directly in cc on a logarithmic 50..12,000
scale. It preserves bore/stroke proportions and compression ratio. This is not
one chamber’s volume. Generator geometry limits still apply: an incompatible
assembly is rejected with a message while the previous sound remains active.

**Exhaust** opens or muffles the profile through absorption and baffles; zero
keeps its stock exhaust. **Combustion** changes attack; **Intake** combines level
and absorption; **Mechanics** changes its level; **Operation** varies combustion
and slightly varies rotation. Changes wait for 120 ms without slider movement,
then crossfade over 50 ms. Editing B while listening to A switches back to B.

Throttle controls target RPM; load lowers it and strengthens the loaded sound.
Response time varies by profile and remains editable. Expand **Imposer le régime
du banc** to set RPM independently of throttle for constant-speed comparison.
The readout shows actual bench RPM; the bench slider spans the profile’s idle
to its limit. Listening volume remains independent of timbre.

**Essai 8 secondes** plays idle, acceleration, load and release. It leaves the
engine running. A bench command interrupts the audition; losing focus releases
Space.

**Mémoriser les réglages dans A** stores the current B sound definition.
**Basculer A / B** compares timbres at the same RPM and load without changing
response time. Levels are not automatically matched. Solo a branch to locate a
difference; turbo remains silent on profiles without one. Pipe dimensions and
compression remain available under **Réglages avancés**. The interface is French.

## Export and verify

```sh
Build/EngineWorkshop --list
Build/EngineWorkshop --render Build/Cross250.wav --profile cross-250-2t
Build/EngineWorkshop --render Build/Vehicles.wav --catalogue
Build/EngineWorkshop --check
Build/EngineWorkshop --trace-audio
```

Each exported profile lasts 10 seconds: the interface’s audition, shutdown and
a final faded tail. `--catalogue` concatenates all 17 in menu order (170 s) and
prints timestamps. Without `--profile`, rendering selects `city-i3`. Export
preserves initial listening volume and level differences without normalization.

`--check` exercises all 17 assemblies, displacement, exhausts, comparisons,
audition cycles, stops, rejection, drawing at three widths, the logarithmic
slider and keyboard selection/start, without a window or audio device.
`--trace-audio` reports empty-queue observations and the largest update interval
at shutdown. Feeding stays bounded: 480-frame blocks, 4,800-frame capacity at
48 kHz, at most 110 ms prepared/queued excluding the device.

The acoustic model is stylized: simplified baffle filters and two-stroke
expansion resonance, without cone, scavenging, power or road-transmission
simulation. Quality and profile recognition require listening qualification.
The [validated engine library](../EngineLibrary/README.md) remains separate.
`Measure.sx` retains its historical V8 generator measurement; it does not measure
the full catalogue.
