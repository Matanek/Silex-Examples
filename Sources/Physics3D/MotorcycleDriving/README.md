# Ride a motorcycle and compare its balance

Hold the controls to drive and steer freely. The bronze chassis, two wheels
and suspensions follow the simulation. The front wheel steers; colored spokes
show actual wheel rotation. Small green markers indicate contacts. The camera
follows the chassis and the grid marks meters; the white post stays at the start.

From the workspace root:

```sh
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release
```

- Hold **Z**: 80% throttle; release to coast with the clutch open.
- Hold **S**: brake with the clutch open; braking overrides throttle.
- Hold **← / →**: steer left/right; release to center.
- **A**: enable/disable balance assistance.
- **L**: enable/disable the speed-dependent steering limit.
- **P**: apply a 150 N·m·s lateral roll impulse.
- **R**: recreate at the start while retaining both assistance settings.
- **Space**: pause/resume; **Escape**: quit.

Buttons perform the five one-shot actions. Throttle, braking and steering
release when focus is lost, on pause and on recreation. A push requested while
paused waits for resume; recreation cancels it.

To compare balance, press R, wait for both contacts, then press P. With
assistance, the motorcycle recovers. Disable assistance with A, recreate with R
and repeat the push: it falls. Without a perturbation, an exactly upright
motorcycle may remain upright even with assistance disabled. L limits steering;
it does not control balance. Its effect is clearest when steering at high speed.

This validation scene uses the profile qualified against Jolt: 100 kg,
isotropic inertia 100 kg·m², 30 cm wheels, 10000 N/m springs with 1000 N·s/m
damping, an ideal 20 N·m engine and a manual 3×3.42 transmission driving the
rear wheel. Simulation runs at 120 Hz. Assistance is an ideal actuator with no
rider simulation. Wheel contacts use rays on a plane; tires are not separate
rigid bodies. This is not yet an off-road course or a motorcycle calibrated
against a real vehicle.

## Check without a window

```sh
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --nocache
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --controls-check
```

`--oracle-check` emits the 8,652 states from the six qualified recipes at
60/120 Hz: departure, mirrored turns, zero grip and assisted/unassisted pushes.
Interactive mode does not replay these sequences. `--smoke` opens a
“TEST AUTOMATIQUE” window, runs all six recipes, checks framing, transforms,
steered wheels, contacts, pause and recreation, then closes with its final
marker. Closing it early does not validate this check.
