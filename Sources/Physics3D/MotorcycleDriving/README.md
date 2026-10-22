# Ride over a motorcycle ramp and compare balance

Ride freely: the chassis, suspensions, steered front wheel and colored spokes
follow their physical states. Green markers show contacts; the grid marks
meters and the camera follows the chassis.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release
```

- Hold **Z**: normal throttle, at 40%; release to coast.
- Hold **W**: request full throttle to lift the front wheel.
- Hold **S**: brake with the clutch open; braking overrides Z and W.
- Hold **← / →**: steer; release to center progressively.
- **A**: enable/disable the automatic roll rider.
- **L**: enable/disable the speed-dependent steering limit.
- **P**: apply a physical 150 N·m·s roll impulse.
- **B**: compare ramp and flat terrain, restarting from the start.
- **R**: recreate at the start, retaining terrain and the A/L choices.
- **Space**: pause/resume; **Escape**: quit.

The scene starts facing an orange ramp approximately 12 m ahead. Wait for
contacts, then hold Z straight ahead: the motorcycle climbs, loses both
supports and lands on the plane. Suspensions extend in flight and take the
load again at landing. The interface distinguishes unsupported flight from a
rear-wheel ride and reports the landing. B restarts on the flat plane, then
restores the ramp on the next press, retaining A/L. B and R resume a paused
simulation and release held controls.

To ride on the rear wheel, recreate with R, wait for contacts, then hold W.
Power and weight transfer physically lift the front wheel. Throttle is
modulated from pitch and pitch rate to prevent flipping backwards; no pose
or artificial pitch impulse is imposed. Release W and brake to lower the
wheel. Z provides more moderate driving.

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
provides up to 80 N·m; a manual 3×3.42 transmission drives the rear wheel.
The 30 cm wheels sit at +1.25 m and −0.75 m from the chassis, shifting weight
distribution rearwards. Springs remain at 10000 N/m and 1000 N·s/m. Simulation
runs at 120 Hz, steering input is bounded before smoothing, and a complete
reversal takes 0.3 s. The rider targets at most 0.5 rad of roll. Contacts use
rays on a plane and a fixed 8 × 0.4 × 6.03 m ramp centered at (0, 0.1, 15) m,
rotated −0.1 rad about X. Tires are not separate rigid bodies. This profile is
not calibrated against a real motorcycle.

## Check without a window

```sh
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Model.sx --nocache
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --nocache
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --controls-check
```

`--oracle-check` emits 17,292 states from six 16-second recipes at 60/120 Hz:
departure/braking, mirrored reversals, a rear-wheel ride, recovery followed by
a collision, and a fall without the rider. They use the same profile and
controls as the Silex-Benchmarks `MotorcycleHandling` witness. Physical checks
also hold turns for three seconds, followed by ten direction changes per
second. `--ramp-check` additionally emits 5,764 flat/ramp states identical to
the `MotorcycleRamp` witness, which verifies ballistic flight, finite box
contacts and landing at 60/120 Hz. Qualification covers this straight approach
with Z, not every terrain or maneuver. Interactive mode replays no sequences.

`--smoke` opens a “TEST AUTOMATIQUE” window, runs seven recipes
(the previous six plus the ramp), checks framing, actual transforms, wheels, contacts, pause and recreation, then closes
with its final marker. Closing it early does not validate this check. After
a collision, proof covers persistent cutout and no sustained rolling: less
than 2 cm and 0.05 rad pose variation during the final two seconds. It does
not promise exactly zero angular velocity at ground contact.
