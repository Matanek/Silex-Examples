# Comparer les contacts de roue sur une arête

Un châssis de 100 kg repose sur quatre roues suspendues. Un moteur de 30 N·m
entraîne les roues arrière à travers une boîte automatique. Les contacts des
pneus font accélérer, tourner et freiner le véhicule. Les jantes blanches
montrent leur rotation ; la bande jaune indique l’avant. La caméra suit le
châssis et le quadrillage métrique rend le déplacement visible. Une bande
violette surélevée se trouve devant lui ; le mode **sphère** est choisi au départ.

Depuis la racine du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

Pour comparer, attendre la réception puis appuyer sur **Z** et laisser le
véhicule traverser la bande violette. Les sphères trouvent ses arêtes et la
caisse monte. **T** recrée le véhicule avec des contacts par rayon : refaire Z,
les rayons passent à côté de la bande et la caisse reste sur ses appuis au sol.
T change de nouveau le mode ; le bouton **Contacts** indique le choix courant.
Le moteur et la bande restent identiques dans les deux parcours.

Après la réception, **Z** accélère devant, **S** demande la marche arrière et
**X** relâche l’accélérateur. Ces commandes restent choisies après relâchement
de la touche. **←/→** choisissent un braquage maintenu ; **↑** recentre.
**F/H** activent ou libèrent leurs freins. **R** repart d’un véhicule neuf,
accélérateur relâché et roues droites. Les boutons ont les mêmes effets.

- **Z / Accélérer** choisit un accélérateur de 60 % et le sens avant.
- **S / Reculer** choisit 50 % et le sens arrière. La boîte ouvre puis reprend
  son embrayage ; un véhicule qui avançait doit d’abord ralentir.
- **X / Relâcher** remet l’accélérateur à zéro. Les pneus continuent à rouler.
- **←/→ / Braquer** choisit 18° aux roues avant ; **↑** recentre. Droite et
  gauche suivent le véhicule, repéré par sa bande jaune, et non le bord de l’écran.
- **F / Frein** active ou libère les quatre freins de 1500 N·m par roue.
- **H / Frein à main** active ou libère les seuls freins arrière de 20 N·m.
- **T / Contacts** alterne rayon/sphère et recrée le véhicule, accélérateur,
  direction et freins relâchés. La sphère balayée a un rayon de 12 cm ; le rayon
  physique de roue reste 30 cm. La bande mesure 1,68 × 0,18 × 4 m et ses arêtes
  passent à 6 cm des axes de roues. Ce volume de contact est une approximation,
  il ne reproduit pas toute la forme cylindrique du pneu.
- **G / Adhérence** change le mode et recrée le véhicule. Sans adhérence,
  les suspensions portent toujours le châssis et les rotors restent reliés au
  moteur, mais les courbes de friction sont nulles. Z fait tourner les roues
  sans pousser le châssis ; P montre une glissade que les freins ne peuvent arrêter.
- **P / Pousser devant** applique une impulsion de 200 N·s selon l’avant du
  châssis, distincte du moteur. **V** pousse de côté avec la même impulsion.
- **B / Bondir** applique 500 N·s verticalement : perte puis reprise d’appui.
- **C / Surcharger** ajoute une force vers le bas pendant deux secondes ;
  les suspensions se compriment jusqu’aux butées puis se détendent.
- **Espace / Pause** fige le châssis, les roues, le régime et la surcharge.
- **R / Recréer** conserve le mode choisi, relâche l’accélérateur et les freins,
  recentre la direction et recrée le véhicule en hauteur.
- **Échap** ferme la fenêtre.

Accélérateur, braquage et freins se combinent. Relâcher l’accélérateur avec X
avant de tester un arrêt, puis F pour le frein normal. Un nouvel appui sur F
le libère. Les actions reprennent une simulation en pause ; l’auto-répétition
est ignorée. G, R et T réinitialisent toutes les commandes ; G et R conservent le mode de contact choisi.

Le panneau indique vitesse, braquage, hauteur, appuis et efforts de suspension,
puis régime moteur, rapport, embrayage et accélérateur. Rapport 0 : point mort ;
rapport négatif : marche arrière. Les changements de rapport sont automatiques.
Au repos : environ 88 cm, quatre appuis et 981 N.

## Vérifications

```sh
silex compile Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release -o .silex/vehicle-suspension
.silex/vehicle-suspension --physics-check
.silex/vehicle-suspension --controls-check
.silex/vehicle-suspension --smoke
```

Le parcours **TEST AUTOMATIQUE** se ferme après les essais de suspension,
roulement, adhérence, braquage et freins, puis accélération, marche arrière,
arrêts, roues motorisées sans adhérence et pause du moteur sur sol simple.
Il compare ensuite le même obstacle en rayon puis en sphère : appuis de bande,
montée de caisse, changement de mode et nouvelle pause. Attendre sa fermeture
normale. Il contrôle physique, transforms rendus et cadrage depuis la vraie
caméra ECS. Les dimensions et la pose du mesh de bande sont comparées à son
corps physique ; les points d’appui sur la bande restent dans le cadre utile.
Les parcours sans fenêtre vérifient physique à 60/120 Hz et
commandes clavier/boutons ; ils ne remplacent pas l’appréciation du rendu.

Simulation à 120 Hz ; poses, longueurs et angles sont interpolés au rendu.
Les meshes sont créés une fois et partagés, la grille se recentre par tranches
de cinq mètres et le panneau se rafraîchit au plus dix fois par seconde ou
après commande. Les appuis observés au début d’un pas peuvent présenter un
léger décalage avec la pose finale interpolée lors d’un impact.

Guides SDK : [suspensions](../../../../Packages/GFX.Physics/Docs/FR/VehicleSuspension3D.md),
[pneus](../../../../Packages/GFX.Physics/Docs/FR/PassiveTires3D.md),
[direction et freins](../../../../Packages/GFX.Physics/Docs/FR/VehicleControls3D.md)
et [groupe moteur](../../../../Packages/GFX.Physics/Docs/FR/VehiclePowertrain3D.md).
