# Monster truck à pneus souples

[English](README.md)

Conduire un pickup à quatre pneus déformables dans une arène géométrique de
freestyle : tables de saut, butte à quatre accès, grandes rampes, réception,
cuvette et petites bosses. Le sol brun conserve une grille pour lire la vitesse.
Les faces jaunes et rouges montrent les trajectoires, avec des bordures blanches.

## Lancer et conduire

Depuis la racine du workspace contenant `Silex-Examples/`, avec ses packages locaux :

```sh
silex run Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native
```

Pour compiler sans ouvrir de fenêtre :

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --debug -o /private/tmp/silex-monster-truck-debug-demo
```

Lancer ensuite `/private/tmp/silex-monster-truck-debug-demo` sans option, depuis
n’importe quel dossier. `run` utilise Debug par défaut ; `--release` reste
disponible pour comparer les modes.

| Commande | Action |
| --- | --- |
| Z maintenu | Accélération normale progressive |
| Maj + Z | Turbo : 25 % de couple supplémentaire, réponse plus franche |
| S maintenu | Frein avant et demande immédiate de marche arrière |
| Maj + S | Frein avant renforcé pour lever l’arrière |
| Q / D | Direction avant, gauche / droite depuis la caméra arrière |
| A / E ou ← / → | Direction arrière selon la direction voulue pour le nez |
| T | Coupler / séparer les essieux directeurs |
| Espace maintenu | Frein à main arrière |
| P | Gonflage Monster / Bas / Ferme, sans recommencer |
| R | Recommencer avec le gonflage sélectionné |
| Molette | Distance de la caméra de poursuite |
| Échap | Quitter |

En marche avant, A ou ← fait partir le nez à gauche ; les roues arrière
braquent donc à droite. Le couplage initial commande les deux essieux en sens
opposés pour serrer le virage. Les touches arrière prennent la priorité sur ce
couplage. En mode indépendant, Q + E ou D + A permet de rouler en crabe.

La caméra suit la direction du déplacement horizontal, avec un horizon fixe.
Elle conserve son dernier cap à faible vitesse ou à l’arrêt ; un cabrage ou un
retournement ne la fait donc pas pivoter avec le châssis. Le recul inverse
progressivement la vue dans la nouvelle direction de déplacement.

Commencer tout droit par la grande table, puis la butte centrale et ses quatre
accès. À gauche se trouvent un tremplin et une réception séparée ; à droite,
une cuvette à deux montées. Les petites bosses sont au fond. La piste de
contrôle, avec une bosse et trois blocs, reste à l’extrême gauche.

Pour un cabrage, donner un bref appui sur Maj + Z puis relâcher. Pour lever
l’arrière, prendre de la vitesse puis donner un bref appui sur Maj + S. Le couple
et le freinage font basculer le véhicule physiquement : doser les appuis pour
récupérer l’équilibre. Comparer ensuite un même relief avec les trois gonflages.

## Montage physique

Chaque pneu mesure 2,20 m de diamètre et 1,32 m de largeur, avec une jante de
1,32 m et des rebords de 1,56 m. Il comporte 192 sommets, 384 triangles et
96 diagonales internes de cisaillement. Les 48 liaisons de talons échangent
des impulsions avec la jante ; les sommets restent dynamiques.

Le profil Bas s’écrase davantage sous charge que Monster ; Ferme se déforme
moins. Sous la charge de référence de ce montage, le rayon chargé est d’environ
1,00 / 1,11 / 1,17 m. Les coefficients 60 / 1400 / 2600 ne sont pas des bars.
Le châssis pèse 150 kg, chaque jante 20 kg et chaque carcasse 9,6 kg.

Le moteur fournit jusqu’à 1250 N·m par roue normalement et 1562,5 N·m avec
Maj, avec réaction opposée sur le châssis. Le frein avant atteint 1000 N·m par
roue, ou 1250 N·m avec Maj ; le frein à main arrière atteint 2200 N·m.
L’inversion demande immédiatement le couple opposé, puis la vitesse traverse
physiquement zéro avant le recul.

Les quatre suspensions SixDOF offrent ±80 cm de course, des ressorts de
1800 N/m et un amortissement de 300 N·s/m. Le montage garde son centre de
masse bas. Le braquage reste disponible à haute vitesse, avec un minimum de
0,35 rad ; le couplage arrière vaut −65 % du braquage avant.

La simulation tourne à 120 Hz, avec huit couplages à 960 Hz et un sous-pas
souple par couplage ; le solveur rigide utilise huit itérations de vitesse.
Les facettes du terrain sont des solides dont les surfaces supérieures se
raccordent. Physique et rendu utilisent la même liste de volumes.

Les crampons suivent les sommets déformés ; les collisions utilisent les
sphères des sommets. L’auto-collision et les contacts souple/souple ne sont
pas disponibles.

## Vérifier

Ces commandes quittent avant la création de l’application graphique :

```sh
/private/tmp/silex-monster-truck-debug-demo --check
/private/tmp/silex-monster-truck-debug-demo --scene-check
/private/tmp/silex-monster-truck-debug-demo --arena-check
/private/tmp/silex-monster-truck-debug-demo --slope-check
/private/tmp/silex-monster-truck-debug-demo --ramp-check
```

Elles couvrent la physique, les gonflages, le centrage, les figures sur appuis
courts, les commandes, le HUD, les raccords du terrain et le roulage lent sur
les vraies facettes inclinées. Les états sont comparés à un et quatre workers.

`--single` choisit un worker pour jouer. `--profile` ouvre un parcours automatique
pendant douze secondes ; `--profile-slope` ouvre un test de six secondes,
freins maintenus sur une rampe. Le titre et le HUD identifient ces mesures.
`--profile-ramp` ouvre une mesure de douze secondes : montée lente de biais,
puis freinage sur la pente. `--ramp-check` vérifie huit approches sans fenêtre,
avec contrôle des talons et du sol. Les temps sans rendu ne permettent pas de
conclure sur les FPS graphiques.
