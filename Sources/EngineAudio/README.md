# Try the engines and gearboxes

[Français](README.fr.md)

## Multi-profile engine-sim bench

`--reference` runs Ange Yaghi’s original engine-sim core in a separate process,
feeding its PCM into GFX.Audio. The accepted Chevrolet 454 remains the default.
This macOS ARM64 qualification bench is separate from the reusable simplified
GFX.Audio generator; game integration is still being evaluated.

Prepare the [native helper](../../Tools/EngineReference/README.md), then compile
from the workspace or Spec group root:

```sh
silex compile Silex-Examples/Sources/EngineAudio/Main.sx --release -o Build/EngineAudio-Reference
Build/EngineAudio-Reference --reference
```

Choose a profile in the drop-down with the engine switched off and the vehicle
stationary. Loading is shown on the dial; event processing continues and audio
starts after a reserve is available. The previous stream is released on replacement.

| Profile | Character / cycle |
|---|---|
| Monster / Chevrolet 454 | Accepted 7.4 L V8, four-stroke |
| Sedan / BMW M52B28 | Inline six, four-stroke |
| Sports car / Ferrari F136 | V8, four-stroke |
| Road motorcycle / Harley | Cruiser V-twin, four-stroke |
| Sports motorcycle / Hayabusa | Inline four, four-stroke |
| Gasoline truck / stock 454 | V8, four-stroke; not a diesel |
| Motocross 450 | Generic single, four-stroke |
| Motocross 250 | Generic single, two-stroke port prototype |

The first six retain upstream mechanical configurations. The motocross profiles
are local adaptations of the Honda TRX520 single, with their own geometry,
inertia, timing and RPM range. Exhaust responses are selected from those
available at the pinned commit. These profiles do not certify a commercial
vehicle’s exact sound or performance. The two-stroke fires every revolution and
uses transfer and exhaust ports. A prescribed-pressure transfer reservoir
simplifies crankcase pumping; its sound still requires listening feedback.

**Banc libre** is the neutral listening bench with adjustable load. Libre,
1,000 and 1,500 select free idle or held speeds. New profiles scale bench load
to displacement; the initial 454 keeps its accepted rendering. **Route** adds
a longitudinal vehicle and transmission. Choose this mode before starting.
The dial shows AUTO or MANUEL, gear (N for neutral) and km/h. Masses and ratios
are demonstration settings.

- **M** or the button toggles ignition. Cranking and coast-down take time.
- Hold **Space** for throttle; release for overrun.
- **A** toggles automatic/manual gear selection.
- **↑ / ↓** or + / − selects a gear and enters manual mode.
- **N** selects manual neutral.
- Hold **S** for the wheel brake.

Clutch pressure falls, throttle is briefly cut and drive progressively returns
during a shift. Clutch operation is automatic even with manual gear selection.
The two-stroke launches above idle with clutch slip. Unsafe downshifts are
refused and displayed; a rejected request is not deferred until a lower speed.
Automatic thresholds and a cooldown prevent hunting. Losing focus releases
throttle and brake. Reverse is not implemented.

Texture controls air-flow noise and timing jitter; physical combustion remains
variable at zero. Exhaust mixes raw output with the chosen impulse response.
Volume and short room reverb are separate Silex treatments. Additional load and
held RPM apply only to Banc; in Route the vehicle provides load. The settings
panel scrolls. The select field and open list use explicit light text, dark
backgrounds and contrasting selection colours.

```sh
Build/EngineAudio-Reference --preset cross2 --road
Build/EngineAudio-Reference --preset moto --manual
Build/EngineAudio-Reference --fleet-check
Build/EngineAudio-Reference --reference-check
Build/EngineAudio-Reference --reference-async-check
Build/EngineAudio-Reference --reference-render Build/EngineReference/Bridge.wav
Build/EngineAudio-Reference --preset cross4 --road --smoke
```

Profile keys: `454`, `berline`, `sport`, `cruiser`, `moto`, `truck`, `cross4`,
`cross2`. The fleet check tests all eight profile lifecycles, selection guards,
auto/manual shifts, neutral and braking, then compares synchronous/asynchronous
road PCM, RPM, speed and gear with four outstanding FIFO requests. The 454 checks
cover silent start, cranking, idle, zero texture, throttle, stopping inertia and
restart. Its WAV contains 576,000 stereo frames at 44.1 kHz. The automatic smoke
lasts nine seconds on Banc, 35 seconds in Route with launch, shifts and braking.
Native visual and listening feedback is still needed.

## Four-stroke motocross airflow

The cross 450 4T profile starts an intake/exhaust background layer at 60%.
**Souffle** controls it independently of Texture and Reverb. Zero restores the
previous pressure signal. Airflow follows RPM, grows under throttle and settles
to silence at rest, with 90 ms smoothing. Other profiles start at zero. Profile
selection and reset-to-defaults restore the catalogue value.

This uses reproducible noise coloured through GFX.Audio, mixed before volume
and reverb while leaving headroom for combustion peaks. It complements the
bench timbre; the recording’s exact background origin (intake, exhaust,
environment or microphone) still requires listening feedback.

```sh
Build/EngineAudio-Reference --airflow-check
Build/EngineAudio-Reference --airflow-render Build/EngineReference/Cross4-Breath.wav
Build/EngineAudio-Reference --airflow-render Build/EngineReference/Cross4-Dry.wav dry
```

The renders keep seven idle seconds after startup. Checks cover split-block
continuity, transparent bypass, bounds, throttle response, stopped silence and
bit-exact synchronous/asynchronous 4T PCM.

## Keyboard and audio scheduling

M follows the logical symbol on AZERTY/QWERTY, including uppercase; repeats do
not toggle ignition. A/N/S also follow their logical symbols. Control/System/Alt
shortcuts remain available. The needle has 25 ms visual damping; numeric RPM is
unfiltered measured state. Dial scale and red zone follow the selected profile,
with geometry rebuilt only on profile changes.

The interactive client consumes ready PCM without waiting for the helper. Five
480-frame blocks fit the stream and up to four FIFO requests remain outstanding.
Partial writes retain their block and offset. This bounds prepared/queued/requested
PCM to about 98 ms plus the helper quantum and device. Offline rendering remains
synchronous for deterministic comparison.

```sh
Build/EngineAudio-Reference --reference --smoke --frame-profile
```

Optional instrumentation reports update intervals, feed and drawing times after
0.5 s warm-up. It does not measure actual display presentation or qualify the
cost/latency of multiple game vehicles.

## Previous procedural prototype

Running without `--reference` retains the prototype below for comparison and
regression checks. Its sound character has not been accepted.


The window opens with the engine off. The **Démarrer / Arrêter** button or **M**
toggles ignition. The tachometer indicates startup and shutdown; fuel rises
gradually during startup and falls over about 350 ms during shutdown. Engaged
combustions finish while RPM keeps falling through inertia, then pressure and
the room tail ring out. Space is ignored while off.
Press Space again to accelerate after an ignition change. Resetting settings
does not change ignition.

Hold **Space** to rev from 800 to 6,600 RPM; release it to return gradually to
the selected speed with changing engine braking. The tachometer and sound follow the same
model. Losing window focus releases the throttle; press again after returning.

From `SilexProject/`, or the root of the owning Spec worktree group:

```sh
silex run Silex-Examples/Sources/EngineAudio/Main.sx --release
```

The window provides five controls: muffled/open exhaust, regular/rough texture,
load, short reverb and volume. Load changes audible effort, including at held
speeds, and slows the bench's RPM rise. The 800, 1,000 and 1,500 buttons select
the speed to return to when Space is released and then hold for comparisons.
The reset button restores initial settings. Volume is smoothed in the samples
without restarting playback. Reverb can be turned down to dry; its mix is
smoothed, initially 6%, with a nominal 0.22-second decay. Its history keeps
advancing at zero mix. This trial has a fixed V8 profile.

The prototype uses `GFX.Audio.Synthesis.Engine`: combustion pulses, two exhausts,
modulated noise, resonances and soft saturation. It uses no recorded loop and
does not simulate mechanical parts or gas flow. The profile uses an RPM-dependent
pressure release, an effort-dependent front and weak flow turbulence. It no longer
injects a tuned damped sine into the excitation. Cylinders have small differences and slow
variations. The bench adds a disturbed, damped idle regulator that slightly
varies the displayed and supplied RPM below 1,800 RPM. Zero texture disables
these variations while retaining intrinsic flow grain. This bench model does not replace a game's engine physics.
Reverb is a separate processor. Quality still needs listening evaluation.

## Check without opening the window

The CLI does not forward this program's options: compile first, then pass
arguments to the executable. Always compile from the workspace or Spec group
root using this explicit entry path:

```sh
silex compile Silex-Examples/Sources/EngineAudio/Main.sx --release -o .silex/engine-audio
.silex/engine-audio --check
.silex/engine-audio --render .silex/engine-audio.wav
```

`--check` verifies keyboard/focus events, RPM response, drawing construction and
block continuity without opening an audio device. `--render` writes 12 seconds
of stereo 48 kHz WAV: idle, revving, hold and deceleration. A final `smooth`
argument removes roughness and muffles the exhaust; `sine` supplies a sine-wave
control at the corresponding combustion frequency. Their levels differ; match
levels before perceptual comparison. These controls do not isolate every filter.

The final argument `dry` keeps the normal scenario with zero reverb.
`idle` holds 800, 1,000 and 1,500 RPM successively for four seconds each;
`idle-dry` runs the same trial without reverb, while `regular` also disables
combustion and RPM irregularities, retaining turbulence. These three variants focus listening on the rumble and changes
between held speeds.

The `ignition` variant renders twelve seconds starting off, with two starts and
two stops. It lets you hear the final combustions and silence between trials.

`--measure` emits timings for 1,000 synthesis blocks of 480 frames after warmup.
It excludes PCM transfer, UI and device output; it is neither a latency measure
nor overall game qualification.

`--smoke` opens a clearly labelled five-second automatic scenario, then closes.
It checks native execution and feeding through startup, acceleration and stopping,
without replacing actual ignition, Space and slider interaction.

## Clocks and limits

The bench advances RPM in 10 ms audio quanta, independently of graphics frames.
Playback retains at most 2,880 queued frames plus a 480-frame block: 70 ms of
production lead at 48 kHz. Mixer/device output and the exhaust profile's acoustic
propagation add to this lead; the meter does
not measure the exact audible frame. Playback starts at the first window update,
after window setup.

The closing log reports observations of an empty stream. This sampled counter
is not a complete history of audible interruptions. Synthesis throughput alone
does not qualify behavior under game load; that work and monster truck integration
remain future steps.
