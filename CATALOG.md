# Catalogue et provenance

Ce catalogue distingue les applications de démonstration des exemples
techniques qui restent dans les packages. Les commits indiqués correspondent à
l'inventaire initial ; ils documentent l'origine, pas une synchronisation
automatique.

## Démonstrations retenues

| Démonstration | Source actuelle | Origine |
| --- | --- | --- |
| Analog clock | `Sources/AnalogClock.sx` | `GFX.Scene2D/Examples/Clock.sx` |
| Boids simulation | `Sources/BoidsSimulation.sx` | `GFX.Scene2D/Examples/Boids.sx` |
| Cornell box | `Sources/CornellBox.sx` | `GFX.Scene3D/Examples/CornellBox.sx` |
| 3D cube | `Sources/Cube3D.sx` | `GFX.Scene3D/Examples/Cube.sx` |
| Easing gallery | `Sources/EasingGallery.sx` | `GFX.Animation/Examples/EasingGallery.sx` |
| Embedded WebView | `Sources/EmbeddedWebView/Main.sx` | `GFX.WebView/Examples/EmbeddedFiles.sx` |
| Falling bodies | `Sources/FallingBodies/Main.sx` | adaptation de `GFX.Physics/Examples/World2D/FallingBody.sx` |
| 3D lighting | `Sources/Lighting3D.sx` | `GFX.Scene3D/Examples/Lighting.sx` |
| PBR materials | `Sources/PBRMaterials/Main.sx` | `GFX.Scene3D/Examples/TestPBR.sx` |
| Plot gallery | `Sources/PlotGallery.sx` | composition des exemples de `Plot/Examples/` |
| Rotating physics container | `Sources/RotatingPhysicsContainer/Main.sx` | `GFX.Physics/Examples/World2D/BoxRotation.sx` |
| 2D shape gallery | `Sources/ShapeGallery2D/Main.sx` | `GFX.Canvas/Examples/ShapeGallery2D.sx` |
| Terminal window | `Sources/TerminalWindow.sx` | `GFX.UI.Terminal/Examples/QuickStart.sx` |
| 2D timeline | `Sources/Timeline2D.sx` | `GFX.Animation/Examples/Timeline2D.sx` |
| 3D timeline | `Sources/Timeline3D.sx` | `GFX.Animation/Examples/Timeline3D.sx` |
| UI control gallery | `Sources/UIControlGallery.sx` | `GFX.UI/Examples/VisualShowcase.sx` |
| 3D viewport axis | `Sources/ViewportAxis3D.sx` | `GFX.Scene3D/Examples/ViewportAxis.sx` |
| 3D world | `Sources/World3D/Main.sx` | `GFX.Scene3D/Examples/World.sx` |

## Commits d'origine

```text
GFX.Physics     79014e74aa244f86530231dfb30abff4f446230b
GFX.Scene2D     959464737a66a08c77abab82c80d1483bfbd53b5
GFX.WebView     2d85e88a09260776f62fbda319d7b329911fe2bc
GFX.UI.Terminal 41eb79bd75ec2fcea7bfa2a45f73d6d9257a8455
GFX.UI          c95676e7294a714cd963bdf2169b01e0e43f9f12
GFX.Canvas      0bb0aa02125375d6d768d3a65ae70cb150759339
Plot            b6586ba8a88059489ec4879fe18c95a54a8f12ec
GFX.Animation   1008702712881cb5564d0ce07c3256e4be3d4109
GFX.Scene3D     4bc4078bc39f723612ffb771ecc74b1943d1f87b
```

## Candidats visuels à évaluer

Ils ne sont pas intégrés automatiquement :

- fenêtres et entrées GFX de base ;
- triangles `GFX.GPU` et passe alternative `GFX.Rendering` ;
- lecture audio et audio spatial ;
- panneaux FPS et performances autonomes ;
- exemples minimaux `GFX.Viewer` ;
- console applicative et terminal système complets ;
- bridge bidirectionnel `GFX.WebView` ;
- exemples Canvas focalisés sur l'image, le texte et les surfaces ;
- cascade de codecs du package `Image`.

Ces programmes restent utiles dans leur package tant qu'ils montrent surtout
une API isolée ou une infrastructure, plutôt qu'une démonstration destinée à
être présentée telle quelle.
