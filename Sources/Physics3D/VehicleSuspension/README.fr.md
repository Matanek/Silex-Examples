# Braquage, freins et suspensions

Un châssis de 100 kg tombe sur quatre roues suspendues. Les ressorts portent
son poids ; les tiges blanches montrent leur longueur et les repères verts
signalent les appuis au sol. Les barres blanches des jantes tournent avec
l’angle physique des roues. Les pneus sont passifs : leur contact avec le sol
entraîne leur rotation. Le braquage agit sur les roues avant ; les freins ralentissent leurs rotors
et le contact transmet l’effort. P lance le châssis par impulsion ; le groupe
motopropulseur reste à venir.

Depuis la racine du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

Après la réception, **P** lance le véhicule ; **←/→** le font tourner et **F**
l’arrête. **↑** recentre les roues. Le braquage est maintenu après relâchement
de la touche, jusqu’à un autre choix. Droite et gauche suivent le repère du
véhicule, indiqué par sa bande jaune. **F/H** activent ou libèrent leurs freins.
Refaire avec **G** pour comparer sans adhérence : les roues braquent mais le
véhicule glisse, même avec les freins actifs.
La caméra suit le châssis et le quadrillage métrique rend son déplacement
visible. La bande jaune marque l’avant du châssis (+Z). Les boutons font les mêmes actions que le clavier.

- **P / Pousser devant** applique une impulsion de 200 N·s selon l’avant du
  châssis. Les pneus entraînés par le contact roulent et prennent une partie
  du mouvement initial.
- **←/→ / Braquer** choisit un angle maintenu de 18° aux roues avant ; **↑** recentre.
- **F / Frein** active ou libère les quatre freins, limités à 1500 N·m par roue.
- **H / Frein à main** active ou libère les seuls freins arrière, limités à 20 N·m.
- **V / Pousser de côté** applique 200 N·s latéralement. Avec adhérence, le
  contact s’oppose à la dérive ; sans pneu, la vitesse latérale persiste.
- **G / Adhérence** change le mode et **recrée** le véhicule en hauteur. Le
  mode sans adhérence garde les suspensions mais retire les pneus virtuels :
  ses roues ne tournent pas et ne transmettent aucun effort tangentiel.
- **B / Bondir** applique 500 N·s verticalement : perte puis reprise d’appui.
- **C / Surcharger** ajoute une force vers le bas pendant deux secondes ;
  les suspensions se compriment jusqu’aux butées puis se détendent.
- **Espace / Pause** fige le châssis, les angles des roues et la surcharge.
- **R / Recréer** conserve le mode choisi et recrée le véhicule en hauteur. R et G libèrent les freins et recentrent la direction.
- **Échap** ferme la fenêtre.

Les actions physiques et la recréation reprennent une simulation en pause.
Une nouvelle surcharge remplace sa durée restante par deux secondes. Les
poussées successives s’additionnent ; l’auto-répétition du clavier est ignorée.
Le panneau affiche le mode, la vitesse, le braquage, la hauteur, les appuis et la somme des
efforts normaux. Au repos : environ 88 cm, quatre appuis et 981 N.

## Vérifications

```sh
silex compile Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release -o .silex/vehicle-suspension
.silex/vehicle-suspension --physics-check
.silex/vehicle-suspension --controls-check
.silex/vehicle-suspension --smoke
```

Le parcours **TEST AUTOMATIQUE** se ferme après chute, saut, perte/reprise
d’appui, surcharge, pause, roulement, poussées, comparaison d’adhérence, virage, arrêt et frein arrière.
Il vérifie les données physiques, les transforms rendus et le cadrage depuis
la caméra ECS utilisée. Les commandes ordinaires n’y sont pas affichées.
Les parcours sans fenêtre contrôlent la physique à 60/120 Hz et les événements
clavier/boutons. Ils ne remplacent pas l’observation de la lisibilité du rendu.

La simulation avance à 120 Hz. Le rendu interpole poses, longueurs, braquage et angles
en dépliant leurs passages par ±2π. Les meshes sont créés une fois et partagés ;
le quadrillage se recentre seulement à chaque franchissement de cinq mètres.
Le panneau se rafraîchit au plus dix fois par seconde et après commande. Les
appuis sont observés au début du pas, puis la pose finale est interpolée ;
cette temporalité peut décaler légèrement un repère au moment d’un impact.

Guides SDK : [suspensions](../../../../Packages/GFX.Physics/Docs/FR/VehicleSuspension3D.md)
[pneus passifs](../../../../Packages/GFX.Physics/Docs/FR/PassiveTires3D.md)
et [commandes de roue](../../../../Packages/GFX.Physics/Docs/FR/VehicleControls3D.md).
