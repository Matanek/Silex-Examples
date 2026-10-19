# Ressentir les suspensions, le tangage et le roulis

Un châssis de 100 kg repose sur quatre roues suspendues. Un moteur de 30 N·m
entraîne les roues arrière à travers une boîte automatique. Les contacts des
pneus font accélérer, tourner et freiner le véhicule. Les jantes blanches
montrent leur rotation ; la bande jaune indique l’avant. La caméra suit le
châssis et le quadrillage métrique rend le déplacement visible. Une bande
violette surélevée se trouve devant lui ; le mode **cylindre 40 cm** est choisi au départ.

Les suspensions **souples** sont choisies au départ. **Z** fait cabrer la
caisse ; **X puis F** fait plonger son nez au freinage. Les flèches gauche et
droite font incliner la caisse vers l’extérieur des virages. **M** recrée
le véhicule avec le réglage ferme précédent ; refaire les mêmes manœuvres
pour comparer. Le bouton indique le réglage et les mesures donnent le tangage
et le roulis physiques. Attendre la réception avant d’accélérer.

**A** compare l’anti-roulis : après un premier virage avec **Z et ←/→**,
appuyer sur A, attendre la nouvelle réception, puis refaire la même manœuvre.
La caisse penche moins vers l’extérieur. Le bouton indique le choix courant.
Le départ reste souple, sans anti-roulis, comme le réglage précédent ; M permet
toujours de comparer souple/ferme. Gaz, pneus et amortisseurs restent identiques
entre les deux essais A. En ligne droite, le cabrage et la plongée restent présents.

Le preset souple utilise 1 200 N/m et 160 N·s/m par roue, contre 10 000 et
1 000 pour le ferme. Sa détente maximale de 77,985 cm compense la compression
statique plus grande et conserve une hauteur de repos d’environ 87,55 cm.
Le moteur, la masse, l’inertie et les pneus sont identiques entre presets.
Les rotations viennent des efforts aux contacts et des quatre suspensions.
Les cylindres larges limitent plus le roulis que les rayons ; les détecteurs
restent comparables avec T, sans promettre la même inclinaison.

Depuis la racine du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

Pour comparer, attendre la réception puis appuyer sur **Z** et laisser le
véhicule traverser la bande violette. Les pneus de 40 cm trouvent un appui
sur ses bords et la caisse monte. **T** recrée le même véhicule avec des pneus
de 8 cm : refaire **Z**, ils passent à côté et la caisse garde ses appuis au sol.
Leur largeur visible change avec leur largeur physique. Le moteur, le rayon
de roue et la bande restent identiques.

T parcourt ensuite **rayon → sphère → cylindre 40 cm → cylindre 8 cm → rayon**.
Le bouton indique le mode courant. Les rayons centraux manquent également la
bande ; la sphère de recherche de 12 cm atteint ses arêtes.

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
- **A / Anti-roulis** active ou désactive deux barres de 1000 N/m et recrée
  seulement le véhicule, commandes relâchées et simulation reprise. R, M, T et G
  conservent ce choix. Le couplage cesse pour une paire lorsqu’une roue perd son appui.
- **M / Suspension** alterne souple/ferme et recrée le véhicule, commandes
  relâchées et simulation reprise. R, G et T conservent ce choix.
- **T / Contacts** parcourt les quatre modes et recrée le véhicule, gaz,
  direction et freins relâchés. Les cylindres ont une largeur totale de 40 ou
  8 cm, un rayon de 30 cm et un axe orienté par le braquage ; le mode sphère
  conserve un rayon de recherche distinct de 12 cm. La bande mesure
  1,68 × 0,18 × 4 m et passe à 6 cm des axes de roue : 4 cm de demi-largeur
  ne suffisent pas à la toucher, 20 cm suffisent.
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
Il compare ensuite le même obstacle en rayon, sphère, cylindre large puis
cylindre étroit : appuis de bande, montée de caisse, changement de mode et
pause. Il poursuit avec le preset souple sur sol simple : cabrage, plongée,
virages opposés, retour au repos, pause et recréation ferme/souple. Attendre
sa fermeture normale. Il contrôle physique, transforms rendus et cadrage depuis la vraie
caméra ECS. Les largeurs rendues des pneus/moyeux et les dimensions/pose du
mesh de bande sont comparées à leurs réglages physiques ; les points d’appui
sur la bande restent dans le cadre utile.
Les parcours sans fenêtre vérifient physique à 60/120 Hz (dont les deux presets, les longueurs de suspension,
le retour au repos et l’absence de balancement moteur sans adhérence) et
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

## Vérifier la comparaison anti-roulis

Le parcours sans fenêtre `-- --anti-roll-check` compare les virages opposés et
la ligne droite en rayon/cylindre large à 60/120 Hz, la récupération après
freinage, l’absence d’effet sans adhérence et le franchissement avec pneus
40/8 cm. Le même SDK produit ces réactions aux points d’appui physiques.
Le choix n’ajoute aucun angle de présentation et ne définit pas de limite
d’inclinaison maximale. Les barres reproduisent le couplage de ressorts Jolt,
qui dépend aussi du pas fixe et de l’amortissement.

Le smoke conserve les essais précédents puis compare les deux virages avec
barres, les transforms rendus, la pause et la recréation. Les fenêtres
TEST AUTOMATIQUE se ferment à la fin. L’essai interactif sert à apprécier la
souplesse et la lisibilité de cette différence.
