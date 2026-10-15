# Suspensions : poids, appuis et rebond

Un châssis de 100 kg tombe sur quatre roues suspendues. Les ressorts portent
son poids, les tiges blanches montrent leur longueur et les repères verts
signalent les appuis au sol. Roues et châssis suivent la simulation physique.

Depuis la racine du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

- **B / Bondir** applique une impulsion verticale : les roues quittent le sol,
  se détendent, puis reprennent leurs appuis à la réception.
- **C / Surcharger** ajoute une force vers le bas pendant deux secondes :
  les suspensions se compriment jusqu’aux butées puis reviennent sous le poids seul.
- **Espace / Pause** fige le mouvement et la durée restante de surcharge.
- **R / Recréer** détruit puis recrée le véhicule en hauteur.
- **Échap** ferme la fenêtre.

Bondir, surcharger et recréer reprennent une simulation en pause. Une nouvelle
surcharge remplace sa durée restante par deux secondes ; elle ne s’additionne
pas à la précédente. L’auto-répétition du clavier ne répète pas les actions.

Le panneau affiche hauteur du châssis, nombre d’appuis et somme des efforts
normaux. Au repos, la hauteur est proche de 88 cm et l’effort total de 981 N.
Les efforts augmentent à la réception et sous surcharge ; ils sont nuls en vol.
Les roues ne sont pas encore motrices : cette scène illustre les suspensions,
sans adhérence de pneu, direction ou freinage.

## Vérifications

```sh
silex compile Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release -o .silex/vehicle-suspension
.silex/vehicle-suspension --physics-check
.silex/vehicle-suspension --controls-check
.silex/vehicle-suspension --smoke
```

Le parcours automatique porte le titre **TEST AUTOMATIQUE** et se ferme après
chute, saut, perte/reprise d’appui, surcharge, pause et recréation. Il contrôle
les données physiques, le cadrage et les transforms des éléments affichés.
Les commandes ordinaires n’y sont pas affichées. Les parcours sans fenêtre
vérifient la physique à 60/120 Hz et les événements clavier/boutons.

La simulation avance à 120 Hz et le rendu interpole les poses et les longueurs.
Les meshes sont construits une fois et partagés ; le panneau se rafraîchit
au plus dix fois par seconde, ainsi qu’après une commande. Les appuis sont
observés au début du pas, puis la pose finale est interpolée. Cette temporalité
peut décaler très légèrement un repère lors d’un impact.

Le SDK et son témoin Jolt sont décrits dans le
[guide des suspensions](../../../../Packages/GFX.Physics/Docs/FR/VehicleSuspension3D.md).
