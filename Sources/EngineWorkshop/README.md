# Listen to and adapt the reference engines

EngineWorkshop uses `GFX.Audio.Engines.Vehicles` and EngineLibrary’s
thermal simulator. Chevrolet 454 is the initial profile;
its definition, exhaust responses and output processing are preserved.
The simplified pulse generator is no longer used by this demo.

City petrol labels now include **extérieur feutré**, and diesel **voix TDI hybride**.
These labels and the window title's “citadines et TDI hybride” identify the
timbre correction. Diesel adds short excitations extracted from the supplied
TDI audio reference, timed by simulated RPM. It does not replay the complete
montage and its recorded engine is unidentified. Exterior petrol city cars stay
quieter than sports profiles at the same listening volume.

From the `SilexProject/` root:

```sh
silex link Packages/GFX.Audio --workspace Silex-Examples
silex compile Silex-Examples/Sources/EngineWorkshop/Main.sx --debug -o Build/EngineWorkshop
Build/EngineWorkshop
```

The embedded simulator remains a Release build. Debug applies to the Silex UI
program here, as with EngineLibrary. The native bank currently supports macOS ARM64.

## Choose and listen

**M** or the button toggles ignition. Hold **Space** to rev, including after a
button click; Enter activates the focused control. Focus loss releases Space.
Displayed RPM comes from simulation. The throttle slider supplies a continuous
pedal and load engages the bench. At 800 RPM, hold leaves idle free; higher
values hold rotation with released throttle using the reference bench’s behavior.

For the 1,200/1,800 customs, American V8 and city I4, the first 90% of the pedal
slider spans the small opening range useful on a free-revving bench. The final
10% reaches wide-open throttle; **Space** always supplies full throttle. This
makes the rise before the limiter controllable without imposing RPM or changing
the mechanics. The 454 and 500 four-stroke motocross commands are preserved.
This bench has no road transmission. Input calibration does not qualify profile
timbre.

The menu contains 18 entries:

- stock Chevrolet 454; three/four-cylinder petrol city cars and a prototype diesel;
- I4, flat-six, GM LS-based V8, LFA-based V10 and Ferrari 412 T2-based V12 sports cars;
- 125/250/500 two-stroke and 250/500 four-stroke motocross bikes;
- Hayabusa-based I4 and grouped-firing V4 race bikes;
- Harley-based 1,200/1,800 custom/chopper engines.

Changing profiles or applying displacement requires ignition off and rotation
stopped. Total displacement in cc changes dimensions and chambers, with
mechanical scaling for singles. Reference 454 retains its original geometry;
choose the American V8 for editable capacity. Rejection keeps the active engine.
The [Vehicles guide](../../../Packages/GFX.Audio/Docs/EN/Vehicles.md) owns model
and limitation details.

## Compare processing

**Texture** controls native synthesizer airflow noise and variations.
**Exhaust** blends raw and response-filtered audio: 100% retains the reference
response. It does not simulate baffles. **Ambience** adds the existing spatial
effect; volume remains independent. Intake is offered only for four-stroke
singles that supply intake flow.

**Mémoriser B dans A** and **Basculer A / B** compare listening settings on the
same running engine without replacing geometry or driving commands. Editing
processing switches back to B. **Essai 8 secondes** plays startup, progressive
throttle, load and release, leaving ignition on. A driving command interrupts
this audition. The interface is French.

## Export and verify

```sh
Build/EngineWorkshop --list
Build/EngineWorkshop --render Build/Chevrolet454.wav
Build/EngineWorkshop --render Build/Cross250.wav --profile cross-250-2t
Build/EngineWorkshop --render Build/Vehicles.wav --catalogue
Build/EngineWorkshop --check
Build/EngineWorkshop --trace-audio
```

Export uses the chosen profile’s initial settings at 44,100 Hz stereo. Each
clip lasts 10 seconds: audition, shutdown and a faded tail. The catalogue
concatenates all 18 clips (180 s) and prints timestamps. Levels are not normalized;
export does not read settings from an existing interactive window.

`--check` compares 454 PCM with EngineLibrary during startup, acceleration,
load and ignition cut, then checks A/B, replacement guards, keyboard controls,
logarithmic slider and drawing at three widths without a device. It also measures
RPM progression at 25/50/75% on all four calibrated pedals and checks access to
wide-open throttle. GFX.Audio’s
consumer test exercises all 18 definitions and continuous throttle. Interactive
feeding stays bounded to five output blocks and four computations of 480 frames,
about 98 ms excluding the device. UI consumes ready blocks without waiting for
simulation. `--trace-audio` reports empty-queue observations and the largest
update interval, not historical device underruns.

Diesel mechanics remain a spark-ignition approximation without diesel injection
or auto-ignition; the recorded voice does not change that physical model.
The sports I4 does not simulate a turbo. Two-strokes retain the
simulator’s simplified ports/scavenging without conical expansion chambers.
Affected profiles display these limits. Variants require listening qualification;
454 parity protects the sound reference. `Measure.sx` still measures the parts
prototype, not this native chain.
