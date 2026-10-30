# Cross a ramp with two tracks and automatic shifting

Drive continuously and observe three forward and reverse gears, torque
interruptions and clutch engagement. Six suspensions, blue/orange spokes and
green support markers follow physical states. The panel reports gear, RPM,
clutch engagement and both track speeds.

From the workspace root or the Spec Worktree group root:

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release
```

- Hold **Z/S**: forward/reverse. Changing direction brakes before driving the
  tracks the other way; it does not return the vehicle to the start.
- Hold **Q/D** or **←/→**: turn. At very low speed without throttle, the tracks
  counter-rotate to pivot.
- Hold **Space**: brake. Releasing throttle allows coasting; light braking holds
  the vehicle when nearly stationary.
- **B/F**: add the ramp/return to the flat plane at the current pose. Removing
  support can naturally let the chassis fall.
- **M**: enable/disable the driving cycle from the current state. A driving
  input takes over. Automatic shifting also works while driving manually;
  the driver cycle and transmission are separate.
- **P**: pause/resume; **R alone**: return to the start on the selected terrain,
  retaining the gearbox profile; **Escape**: quit.

Five buttons control terrain, driver, pause and reset. Releases and focus loss
clear driving input. B/F and M retain pause; R resumes. Commands retain vehicle
identity, pose, velocities and clock; driving continues beyond sixteen seconds.
Inputs never impose chassis poses/velocities or wheel rotation.

## Observe gear changes

The window starts facing the ramp. **F**, then **R**, compare the same start
on the flat plane; **B**, then **R**, restore the ramp. Hold Z to see 1/2/3 and the clutch open
and engage again. Brake to observe downshifts and neutral. S drives through
the same sequence in reverse. Keyboard driving modulates torque and track
speed differences with vehicle speed, targeting about 9 m/s for maneuverability;
the engine and suspensions match the qualified witness.

To run the qualified cycle without throttle modulation, enable **M**, then
explicitly press **R** to start over: 2 s settling, 4 s at 80 % throttle and 10 s
at 4 % braking, followed by holding at rest. It never restarts itself. The panel
distinguishes the driver cycle from automatic shifting. R alone recreates the
vehicle. The camera follows the chassis; grid spacing is one meter. On the
ramp the driver climbs, loses all six supports for about 0.39 s, lands and
brakes to rest. The panel reports flight and recovered supports; green
markers disappear during flight.

## Model and qualification

100 kg, isotropic inertia 100 kg·m², six 30 cm wheels, 10000 N/m springs and
1000 N·s/m dampers, track inertia 2 kg·m², 15 N·m engine and differential 6.
Ratios are 2/1.4/1 and −2/−1.4/−1, thresholds 1800/1200 RPM, switch 0.5 s,
engagement 0.3 s, latency 0.5 s. Moderate braking applies 60 N·m per track. Tracks are
an ideal coupling without articulated links; contacts use six rays.

The standalone `TrackedAutomaticRun.py` witness in Silex-Benchmarks qualifies
forward/reverse shifts on a plane and upshift inhibition without support or
with opposing tracks. The scene reproduces the two forward/reverse cases
exactly. Eight historical manual recipes, including ramp traversal, remain
in automated tests with unchanged witnesses.

`TrackedAutomaticRampRun.py` also compares flat and ramp courses with automatic
shifting at 60/120 Hz, Native Debug/Release. The scene exactly reproduces these
two 16 s courses: an 8 × 0.4 × 6.03 m box tilted by 0.1 rad, ascent, flight,
landing and rest. Shift sequences and clutch behavior remain qualified through
this course. Already being in third gear during flight does not prove upshift
inhibition without support; that retains its independent plane witnesses.

These recipes do not prove prolonged high-speed straightness, general terrain,
extreme braking or linked tracks.

## Verify

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --controls-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --automatic-physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --automatic-ramp-physics-check
```

`--controls-check` checks held input, releases/focus, turns, braking, reverse,
pause, driver and five buttons in both profiles, retaining state and checking
R separately. `--physics-check` retains manual recipes; `--automatic-physics-check`
checks 1/2/3/2/1/neutral, clutch, rest and profile retention through reset at 60/120 Hz.

`--oracle-check` emits 8,652 historical states; `--ramp-check`, 5,044 flat/ramp states;
`--automatic-check`, 5,764 forward/reverse states identical to the qualified benchmark.
`--smoke` runs eight manual recipes, checking framing, wheels, supports and ramp.
`--live-smoke` runs 18 s of automatic continuous controls, terrain changes, driver,
pause and manual takeover without a reset. Closing early does not pass these
checks; the “TEST AUTOMATIQUE” windows close when complete.

`--automatic-ramp-check` emits 5,764 flat/ramp states, byte-identical to the new
qualified witness. `--automatic-ramp-physics-check` checks ascent, flight,
landing and rest against the flat control at 60/120 Hz, then explicit reset.
`--automatic-smoke` runs both courses in the native window, checking automatic
shifting, wheels, support markers, camera and final pause. Switching to the
second terrain explicitly recreates the vehicle in this test; interactive
B/F and M continue retaining the vehicle.


## Observe carrying by a moving platform

Open platform mode from the same root:

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --platform
```

Click **Déplacer lat. (B)** or **Déplacer long. (F)**: the blue platform
immediately moves at 2 m/s for 2 s, then stops. **Déplacer (M)** restarts the
last axis; during motion this button becomes **Arrêter (M)**. Every movement
starts from the current state without resetting. The chassis remains dynamic;
contact carries it without imposing a chassis pose or velocity. The panel
compares vehicle and support speeds, supports, neutral gear, RPM and track rotation.

- **B/F**: start lateral/longitudinal motion, including after a completed movement.
- **G**: lock/release the holding brake. Its effect appears during motion;
  the button shows the brake state even when stopped.
- **M**: start/stop motion. After the 2 s, one click starts it again.
- **Space**: hold the brake without disabling M.
- **ZQSD**: take over driving; this stops support motion. The G holding brake
  stays applied until released.
- **P**: pause/resume. **R alone** returns both vehicle and support to the start,
  retains axis/brake and resumes. **Escape** quits.

To compare both brake states from the same start: **R**, wait for supports,
then **F**; repeat **R**, **G**, wait for supports, then **F**. Reset helps
comparison; the movement buttons work without it.

Locked tracks carry the vehicle at almost 2 m/s. Free longitudinal rollers
let the vehicle travel at about 0.615 m/s while the platform moves faster and
the tracks rotate in the opposite relative direction. The vehicle stops near
1.23 m, compared with about 4 m when locked. Grid lines remain world references;
the 8 × 0.4 × 12 m blue box is the only physical support. Free driving can
leave its edges; R restores the start.

`TrackedPlatformRun.py` qualifies four 6 s recipes at 60/120 Hz, Native
Debug/Release. `--platform-check` emits 4,328 states identical to the benchmark;
`--platform-physics-check` checks carrying/rolling/rest and reset;
`--platform-controls-check` checks commands and buttons without implicit reset,
including restarting after completion. `--platform-click-smoke` exercises clicks
in the native window, with immediate motion, stopping, restarting and braking.
`--platform-smoke` runs all four cases in the native window, checking platform,
chassis, wheels, supports, framing and pause. Qualification covers horizontal
translation, in neutral with no throttle; these four recipes do not prove
free driving, rotating or dynamic supports, or general terrain.

## Extended driving with an explicit accuracy profile

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long
```

Long mode uses 48 velocity/4 position iterations at 120 Hz. Its 20 s cycle settles
for 2 s, accelerates for 8 s and brakes for 10 s. Press **M** or the pilot button to
start from the current position. It reaches roughly 90 km/h and travels 176 m on
the plane. **R alone** returns to the start. **ZQSD**, **Space** and **P** keep
continuous driving, braking and pause; driving input takes over from the pilot.
This workload uses flat terrain.

The 300 × 400 HUD stays on the left; the camera and grid follow the vehicle.
Body/wheel poses, suspension and gears come from simulation. Ordinary actions
retain the vehicle and clock. M restarts the program without repositioning;
R repeats the exact witness from rest. Other modes retain their solver profiles.

The forward/reverse standalone witness has 7204 states at 60/120 Hz, matching the
loaded subset of TrackedAutomaticLong. The 48/4 profile is qualified; the
original 12/4 long workload still exceeds its 5 cm parity budget at about 7.04 cm.
This scene does not resolve that 12/4 case or change the SDK. High-speed turns
and arbitrary terrain are not qualified by this workload.

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long-physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long-controls-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long-smoke
```

The “TEST AUTOMATIQUE” smoke starts one full 20 s cycle through a real click,
checks rendered poses and the moving camera/grid, then closes itself. Headless
checks also cover HUD ink, clicks, pause, manual takeover and R. This accuracy
profile increases iterations; the workload makes no measured FPS claim.

### Vehicle-relative steering directions

While driving forward or pivoting, **Q / Left arrow** turns the nose toward
the vehicle’s left; **D / Right arrow** turns it toward the vehicle’s right.
The frame follows the vehicle as its heading changes. Displayed left/right
track speeds use that same convention. This corrects interactive input mapping;
the straight automatic route and physics witnesses are preserved.

The headless check covers logical AZERTY keys and arrows while moving and
pivoting, from two initial headings:

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --steering-check
```
