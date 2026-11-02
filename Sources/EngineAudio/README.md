# Try the V8 engine

[Français](README.fr.md)

## Chevrolet 454 reference mode

`--reference` drives [Ange Yaghi's engine-sim](https://github.com/ange-yaghi/engine-sim)
core with its Chevrolet 454 V8 profile for the first episode. The original
simulation computes the starter, combustion, flows, inertia and synthesis; the
tachometer reads its actual RPM. This macOS ARM64 qualification bench uses a
separate process. The reusable GFX.Audio generator and game qualification remain
unfinished.

Build the [native witness](../../Tools/EngineReference/README.md) first, then
compile from the workspace or Spec group root:

```sh
silex compile Silex-Examples/Sources/EngineAudio/Main.sx --release -o Build/EngineAudio-Reference
Build/EngineAudio-Reference --reference
```

**M** or the button starts and cuts ignition. Allow the starter to turn the engine,
then hold **Space** to accelerate and release to decelerate. The window starts
with the engine off. Losing focus releases the throttle. Cutting ignition lets
active combustion finish while the mechanical rotation decays.

Defaults keep the original profile's texture and filtering, with 20% bench load
and no added reverb. Texture controls air noise and temporal jitter; physical
combustion irregularity remains at zero. Exhaust blends the raw signal with the
original impulse response. Load brakes acceleration under throttle. The 800 button
leaves the idle free, typically around 850–900 RPM; 1,000 and 1,500 impose bench
speed after startup. Volume and short reverb remain separate Silex effects.

```sh
Build/EngineAudio-Reference --reference-check
Build/EngineAudio-Reference --reference-render Build/EngineReference/Bridge.wav
Build/EngineAudio-Reference --reference --smoke
```

The headless check covers initial silence, progressive cranking, idle, texture
zero, acceleration, coast-down, stopped silence and restart. WAV rendering keeps
the initial texture and records the main scenario: 576,000 stereo frames at
44.1 kHz, approximately 13.06 seconds. The reference smoke lasts nine seconds.
Native listening and interaction testing are still required. The exact settings
of every video segment remain unidentified; this is a render of the original
profile rather than a certified reproduction of the video's edit.

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
