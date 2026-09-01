# Catalogue et provenance

Ce catalogue distingue les applications de démonstration des recettes
documentaires et des preuves automatisées des packages. Les commits indiqués
correspondent à l'inventaire initial ; ils documentent l'origine, pas une
synchronisation automatique.

## Démonstrations retenues

| Démonstration | Source actuelle | Origine |
| --- | --- | --- |
| Analog clock | `Sources/AnalogClock.sx` | `GFX.Scene2D/Examples/Clock.sx` |
| Application command console | `Sources/ApplicationCommandConsole.sx` | `GFX.UI.Terminal/Examples/ApplicationConsole.sx` |
| Application GPU triangle | `Sources/ApplicationGPUTriangle/Main.sx` | `GFX.GPU/Examples/TriangleApplication.sx` |
| Application window | `Sources/ApplicationWindow.sx` | `GFX/Examples/ApplicationWindow.sx` |
| Boids simulation | `Sources/BoidsSimulation.sx` | `GFX.Scene2D/Examples/Boids.sx` |
| Character mover 2D | `Sources/CharacterMover2D.sx` | `GFX.Physics/Examples/CharacterMover2D.sx` |
| Composed system terminal | `Sources/ComposedSystemTerminal.sx` | `GFX.UI.Terminal/Examples/SystemTerminal.sx` |
| Cornell box | `Sources/CornellBox.sx` | `GFX.Scene3D/Examples/CornellBox.sx` |
| 3D cube | `Sources/Cube3D.sx` | `GFX.Scene3D/Examples/Cube.sx` |
| Dedicated system terminal | `Sources/DedicatedSystemTerminal.sx` | `GFX.UI.Terminal/Examples/QuickStart.sx` |
| Direct GPU triangle | `Sources/DirectGPUTriangle/Main.sx` | `GFX.GPU/Examples/TriangleDirect.sx` |
| Direct window and input loop | `Sources/DirectWindowInputLoop.sx` | `GFX/Examples/WindowAndInput.sx` |
| Easing gallery | `Sources/EasingGallery.sx` | `GFX.Animation/Examples/EasingGallery.sx` |
| Embedded WebView | `Sources/EmbeddedWebView/Main.sx` | `GFX.WebView/Examples/EmbeddedFiles.sx` |
| Physics 2D body control | `Sources/Physics2D/BodyControl.sx` | création propre au catalogue pour les contrôles publics de `GFX.Physics` |
| Physics 2D shape response | `Sources/Physics2D/ShapeResponse.sx` | création propre au catalogue pour la réponse dynamique et les matériaux de `GFX.Physics` |
| Falling bodies | `Sources/Physics2D/FallingBodies/Main.sx` | adaptation de `GFX.Physics/Examples/World2D/FallingBody.sx`, migrée vers `Plugins.Physics2D` |
| FPS statistics panel | `Sources/FPSStatsPanel.sx` | `GFX.Stats/Examples/FPSPanel.sx` |
| Generated HTML WebView | `Sources/GeneratedHTMLWebView.sx` | composition de la recette `HTML/Docs/Recipes.md#buildandparse` et de `GFX.WebView` |
| 3D lighting | `Sources/Lighting3D.sx` | `GFX.Scene3D/Examples/Lighting.sx` |
| PBR materials | `Sources/PBRMaterials/Main.sx` | `GFX.Scene3D/Examples/TestPBR.sx` |
| Rendering performance panel | `Sources/PerformanceStatsPanel.sx` | `GFX.Stats/Examples/PerformancePanel.sx` |
| Plot gallery | `Sources/PlotGallery.sx` | composition des exemples de `Plot/Examples/` |
| Rotating physics container | `Sources/Physics2D/RotatingPhysicsContainer/Main.sx` | `GFX.Physics/Examples/World2D/BoxRotation.sx`, migré vers `Plugins.Physics2D` |
| Bundle content transitions | `Sources/Bundle/Transitions.sx` | création propre au catalogue |
| Bundle window replacement | `Sources/Bundle/WindowReplacement.sx` | création propre au catalogue |
| Bundle multiple windows | `Sources/Bundle/MultipleWindows.sx` | création propre au catalogue |
| 2D shape gallery | `Sources/ShapeGallery2D/Main.sx` | `GFX.Canvas/Examples/ShapeGallery2D.sx` |
| Silex logo | `Sources/SilexLogo.sx` | création propre au catalogue |
| Spatial audio | `Sources/SpatialAudio.sx` | `GFX.Audio/Examples/PlaySpatialSound.sx` |
| 2D timeline | `Sources/Timeline2D.sx` | `GFX.Animation/Examples/Timeline2D.sx` |
| 3D timeline | `Sources/Timeline3D.sx` | `GFX.Animation/Examples/Timeline3D.sx` |
| UI control gallery | `Sources/UIControlGallery.sx` | `GFX.UI/Examples/VisualShowcase.sx` |
| 3D viewport axis | `Sources/ViewportAxis3D.sx` | `GFX.Scene3D/Examples/ViewportAxis.sx` |
| WebView bridge | `Sources/WebViewBridge.sx` | `GFX.WebView/Examples/BridgeWebPage.sx` |
| 3D world | `Sources/World3D/Main.sx` | `GFX.Scene3D/Examples/World.sx` |

Les chemins d'origine ci-dessus sont historiques. Après promotion, les copies
parfaitement couvertes ont été supprimées des packages pour l'horloge, les deux
triangles GPU, les deux parcours Window, les trois galeries Animation, Cornell
Box, Cube, Lighting, PBR, Viewport Axis, les terminaux, les WebViews embarquée
et pontée, les deux panneaux de statistiques, l'audio spatial, la galerie de
formes 2D et la galerie Plot.

Les anciennes variantes de package ont maintenant été classées. Les
démonstrations Boids et World3D restent ici sous leur forme de présentation.
Les deux applications Physics 2D historiques sont regroupées avec les
démonstrations focalisées de contrôle des corps et de réponse des formes sous
`Sources/Physics2D/`. Le benchmark Boids précis, la matrice World3D et le stress
consumer FallingBodies2D vivent dans
[`Silex-Benchmarks`](https://github.com/Matanek/Silex-Benchmarks). Le conteneur
physique tournant ne possède pas de second benchmark : sa démonstration couvre
déjà son intention.

## Commits d'origine

```text
GFX.Physics     79014e74aa244f86530231dfb30abff4f446230b
GFX             aed6c4615ff6dbe20ee8c185373dbbaa09940455
GFX.GPU         93af3caf52900c950a3e3a71a51b674f6f47991b
GFX.Scene2D     959464737a66a08c77abab82c80d1483bfbd53b5
GFX.WebView     2d85e88a09260776f62fbda319d7b329911fe2bc
GFX.UI.Terminal 41eb79bd75ec2fcea7bfa2a45f73d6d9257a8455
GFX.UI          c95676e7294a714cd963bdf2169b01e0e43f9f12
GFX.Canvas      0bb0aa02125375d6d768d3a65ae70cb150759339
Plot            b6586ba8a88059489ec4879fe18c95a54a8f12ec
GFX.Animation   1008702712881cb5564d0ce07c3256e4be3d4109
GFX.Scene3D     4bc4078bc39f723612ffb771ecc74b1943d1f87b
HTML            e1a57ffaba4bfb363619097d579278b9df29dd1a
```

## Candidats visuels à évaluer

Ils ne sont pas intégrés automatiquement :

- passe alternative `GFX.Rendering` ;
- lecture audio et audio spatial ;
- panneaux FPS et performances autonomes ;
- exemples minimaux `GFX.Viewer` ;
- bridge bidirectionnel `GFX.WebView` ;
- exemples Canvas focalisés sur l'image, le texte et les surfaces ;
- cascade de codecs du package `Image`.

Ces programmes restent utiles dans leur package tant qu'ils montrent surtout
une API isolée ou une infrastructure, plutôt qu'une démonstration destinée à
être présentée telle quelle.
