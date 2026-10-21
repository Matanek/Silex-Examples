# Inspect and operate a UI session on macOS

This interactive example presents a **Nom** field, a **Valider** button and two
feedback lines, as well as checkboxes, a **Profil** radio group and a
**Volume** slider. It passes the session directly to Viewer, with no additional
accessibility wiring in application code.

The **Masquer les contours des cases et radios** button compares the default
outline with `FocusAppearance.none()`. It applies to both checkboxes and the
radio group; the slider keeps its usual focus setting. Navigation and activation
remain available. The dark theme provides light labels against the Viewer
background, and the page scrolls when the window is too small.

From the workspace root, using the development toolchain supporting protocol
method bodies:

```sh
silex run Silex-Examples/Sources/UIAccessibility/Main.sx --debug
```

In the macOS accessibility inspector, find **Nom** with its text-field role and
**Ada** value, then **Valider** with its button role. Editing or activating them
through the tool must update the same feedback lines as mouse or keyboard
input. With VoiceOver, check label/value reading, focus navigation, typing and
activation. Move or resize the window to check the exposed geometry.

The button/text-field path has been confirmed with the inspector and VoiceOver.
To qualify the new controls:

1. Activate **Notifications**: its checked state and visible feedback change.
2. Choose **Énergique** in **Profil**: exactly one option is checked;
   **Indisponible** remains disabled.
3. Adjust **Volume**: initial value 12, minimum 10, maximum 20; increment and
   decrement actions update the same state as mouse dragging.
4. Check **Verrouiller le volume**: the slider becomes disabled and rejects
   changes; uncheck it to restore adjustment.
5. Toggle **Notifications** again, then return to the group and slider:
   references remain usable after the interface is reevaluated.

Headless tests cover these actions and rejection of disabled actions. They do
not qualify the new controls with VoiceOver or the Linux/Windows bridges.

`--cpu-check` verifies the model and semantic actions without a window. It does
not verify attachment to a real window or VoiceOver.
