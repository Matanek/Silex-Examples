# Inspect and operate a UI session on macOS

This interactive example presents a **Nom** field, a **Valider** button and two
feedback lines. It passes the session directly to Viewer, with no additional
accessibility wiring in application code.

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

This test qualifies the initial AppKit path; it does not qualify the remaining
controls or Linux/Windows bridges.

`--cpu-check` verifies the model and semantic actions without a window. It does
not verify attachment to a real window or VoiceOver.
