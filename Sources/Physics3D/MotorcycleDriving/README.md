# Jump a steeper ramp with the cross profile

Ride freely with the motocross-inspired test profile: the chassis, suspensions, steered front wheel and colored spokes
follow their physical states. Green markers show contacts. The ground uses
`World3D/Assets/DarkGrid.png`: small cells measure one meter and remain anchored
to the world while driving. A rear chase camera smooths its position and heading.
It keeps the horizon level through turns, wheelies and jumps; after a crash,
its heading settles. R and B immediately reset it at the start.

Metrics and all six buttons share a compact panel on the left. The center
and upper scene remain clear so the ramp is easier to spot.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release
```

- Hold **Z**: normal throttle, at 40%; release to coast.
- Hold **W**: request full throttle to lift the front wheel.
- Hold **S**: brake with the clutch open; braking overrides Z and W.
- Hold **← / →**: turn left/right from the rear view; release to center progressively.
- **A**: enable/disable the automatic roll rider.
- **L**: enable/disable the speed-dependent steering limit.
- **P**: apply a physical 150 N·m·s roll impulse.
- **B**: compare ramp and flat terrain, restarting from the start.
- **R**: recreate at the start, retaining terrain and the A/L choices.
- **Space**: pause/resume; **Escape**: quit.

The scene starts facing an orange 16° ramp approximately 12 m ahead. Wait for
contacts, then hold Z straight ahead: the motorcycle climbs, loses both
supports and lands on the plane. Suspensions extend in flight and take the
load again at landing. The interface distinguishes unsupported flight from a
rear-wheel ride and reports the landing. B restarts on the flat plane, then
restores the ramp on the next press, retaining A/L. B and R resume a paused
simulation and release held controls.

To try a rear-wheel ride on the plane, press B, wait for contacts, then hold Z:
torque and weight transfer lift the front wheel. W requests more throttle
from the start. Wheelies are allowed at low and moderate speeds; the rider
progressively reduces the pitch margin between 29 and 50 km/h to regain the
front support as speed increases. Release the throttle and brake to lower
the wheel. No jump, pose or pitch impulse is imposed. The display shows
applied throttle and front/rear compression in centimeters, measured from
maximum suspension extension.

A disables only roll correction. Without it, this motorcycle has no simulated
rider or manual lean control: it is unstable in turns. This mode compares the
effect of automatic balance. At rest, try R then P, and repeat after A and R.
L removes the steering limit while progressive input remains active.

After a fall (about 73° chassis tilt), throttle and the rider cut out until R.
The body keeps falling physically; correction does not restart during bounces.
A then chooses the mode for the next R, shown on its button. Six buttons
perform the same one-shot actions. Focus loss, pause, B and R release Z/W/S and
steering. P requested while paused waits for resume; R cancels it.

The profile retains 100 kg and isotropic inertia of 100 kg·m². The ideal engine
provides up to 120 N·m (+50%); a manual 3×3.42 transmission drives the rear wheel.
The 30 cm wheels sit at +1.25 m and −0.75 m from the chassis, shifting weight
distribution rearwards. Springs and damping are set to 2500 N/m and 350 N·s/m. Suspension travel is
70 cm (0.2–0.9 m lengths), with mounts 10 cm above the chassis center.
Static sag is approximately 14 cm at the front and 26 cm at the rear; under
acceleration, rear compression reaches approximately 40 cm. Landing uses
almost the full travel before the motorcycle settles. Simulation
runs at 120 Hz, steering input is bounded before smoothing, and a complete
reversal takes 0.3 s. The rider targets at most 0.5 rad of roll. Contacts use
rays on a plane and a fixed 8 × 0.4 × 9 m ramp centered at (0, 1.0514218, 16.5) m,
rotated −0.28 rad about X. Its exit edge reaches 2.49 m. Tires are not separate rigid bodies. This profile is
not calibrated against a real motorcycle.

## Check without a window

```sh
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Model.sx --nocache
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --nocache
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/ChaseCamera.sx --nocache
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Ground.sx --nocache
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --controls-check
```

`--view-check` checks framing through all eight recipes with the rear camera,
level horizon, pause and reset, without a window. Ground tests verify that the
same world points retain their texture phase after recentering.

`--oracle-check` emits 17,292 states from six 16-second recipes at 60/120 Hz:
departure/braking, mirrored reversals, a rear-wheel ride, recovery followed by
a collision, and a fall without the rider. They use the same profile and
controls as the Silex-Benchmarks `MotorcycleHandling` witness. Physical checks
also hold turns for three seconds, followed by ten direction changes per
second. `--ramp-check` additionally emits 5,764 flat/ramp states identical to
the `MotorcycleRamp` witness, which verifies ballistic flight, finite box
contacts and landing at 60/120 Hz. Qualification covers this straight approach
with Z, not every terrain or maneuver. Interactive mode replays no sequences.

`--cross-check` emits 8,646 cross-profile states: Z held from rest, the ramp,
and Z applied after reaching approximately 16 km/h. `MotorcycleCross` retains the chassis budgets through landing and checks
throttle, slope memory, gravity and rotors independently. The recipe retains physical flight, regained supports and braking.
The rider retains the loaded supports’ slope during flight and modulates
throttle, imposing no aerial pitch torque or pose. Both earlier witnesses
retain their road settings as regressions; free driving starts with cross. W has consumer behavior checks for lift,
compression, braking and regained supports; pointwise Jolt parity during a
prolonged full-throttle wheelie remains unqualified.

`--smoke` opens a “TEST AUTOMATIQUE” window, runs eight recipes
(the six historical cases, road ramp, then cross ramp), checks framing, actual transforms, wheels, contacts, pause and recreation, then closes
with its final marker. Closing it early does not validate this check. After
a collision, proof covers persistent cutout and no sustained rolling: less
than 2 cm and 0.05 rad pose variation during the final two seconds. It does
not promise exactly zero angular velocity at ground contact.
