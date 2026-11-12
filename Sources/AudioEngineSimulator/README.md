# AudioEngineSimulator

## EngineWorkshop presets

The main window combines the nine EngineWorkshop presets with a cutaway
and an overhead view. Both views animate the pistons from the engine RPM
and highlight each cylinder when its chamber fires. The ignition key, tachometer and accelerator sit beside the views or below
them in a narrow window.

Click the key or press **M** to toggle ignition. Hold **Space** to fully
depress the pedal in 0.15 s. Release **Space** to return to its starting
position in 0.3 s. The **Accélérateur** slider sets the throttle opening. Click
**Essai 8 secondes** for the EngineWorkshop audition. Selecting another
preset switches off the ignition. Click the key or press **M** to start
the selected engine.

Click a gear on the gate beside the pedal to select it. **Up** and **Down**
shift, and **N** selects neutral. The gate shows the engaged gear and speed.
Hold **S** to brake. The gearbox engages the selected gear at the current
speed. A downshift can drive the engine past the ignition cut-off and
slow the vehicle through engine braking.
In neutral, **Charge du banc** applies the bench load.

`--check-references` checks the views and controls and compares the PCM, RPM
and starter state of all nine presets with EngineWorkshop.
`--render-reference <id> <wav>` exports the same audition as 44.1 kHz stereo WAV.

## Parts-based simulator

Run the binary with `--procedural` to configure the engine parts and equipment.

The window starts with a generic four-stroke V8. Use the left panel to
choose inline or V, select the cylinder count and set total displacement.
The range depends on the cylinder count, from 50 cc on a single to 48 L
on a V16. Changing the configuration switches off the ignition. The
pistons, rods, and tachometer follow the simulation that produces the sound.
Click the key or press **M** to turn it from 11 to
1 o'clock and switch on the ignition. Hold **Space** to fully depress the
pedal in 0.15 s. The gauge shows pedal travel. Cylinder filling follows the
pedal with a short lag. Releasing Space returns the pedal to rest in 0.3 s
and increases engine braking. Resize the
window to see the panels adapt while preserving each drawing's proportions.
The overhead view sits below the cutaway. The key, tachometer and
accelerator sit to the right and move below the views in a narrow window.

Below the engine settings, **Mixage** adjusts intake and combustion from
0 to 100% during playback. Their starting levels are 20% and 100%. To
isolate either source, set the other to 0%. Changing the engine keeps
the current mix.

Use the **Échappement** panel to change the silencer or outlet layout
while the engine runs. **Tube libre** reduces absorption and removes the
baffles. **Chicanes** adds damping. **Commune** groups the cylinders,
**Deux longueurs** routes the pulses through pipes of different lengths,
and **Une dominante** attenuates the second outlet. **Origine** restores the assembly setting
for that row.

**Réglages techniques** opens the editor for engine geometry, firing phases
and exhaust. Assign cylinders to outlets numbered from 1. With zero
configured outlets, outlet 1 uses a common resonance. Numbers accept
a comma or a decimal point. **Appliquer** returns to the bench, and a
changed engine waits for the ignition to be switched on again.
Under **Mécanique**, **Rupteur (tr/min)** sets the threshold and **Coupure
(ms)** sets the delay before ignition resumes below it. The tachometer
adapts its scale to the selected threshold.

**Chevrolet 454** loads a 7.44 L V8 whose values appear in the editor. To recreate it,
start from **En V** and **8 cylindres** and enter the
[preset values](EngineConfig.sx). Changing the layout, cylinder count or
displacement slider starts from the generic values.

The configurations use a generic spark-ignition four-stroke model and
representative firing phases. The marine-size range lets you explore
large displacements.

Run from the workspace root with a `GFX.Audio` checkout that provides
`EngineSimulation`.

```sh
mkdir -p Build
silex compile Silex-Examples/Sources/AudioEngineSimulator/Main.sx --debug -o Build/AudioEngineSimulator-Window
Build/AudioEngineSimulator-Window
```

## Offline export

`--render-454 <prefix>` writes the preset's mix and three stems, with
an 850 rpm idle, a ramp to 2,600 rpm, a steady hold and a ramp down. The
CSV trace records speed and controls.

The export renders a generic four-stroke single cylinder and a twin with
a 180° firing offset.

```sh
mkdir -p Build/AudioEngineSimulator-Audio
Build/AudioEngineSimulator-Window --render Build/AudioEngineSimulator-Audio/moteur
```

In the `mono` and `bi` recordings, the starter engages at 0.25 s and
ignition starts at 0.95 s. Throttle rises from 2.20 s, closes at 4.70 s,
and ignition cuts at 5.30 s. The load stays engaged during coastdown.
Listen to the mix and the isolated friction, intake and combustion tracks.

The `frottement-reference` and `frottement-double` files run for two seconds
at 1,500 rpm with ignition off. The friction coefficient changes from 0.08
to 0.16. The 48 kHz mono WAV files retain their rendered levels. The CSV
files record the controls and cylinder state every 240 audio frames, with
the exact frame of the most recent firing.
