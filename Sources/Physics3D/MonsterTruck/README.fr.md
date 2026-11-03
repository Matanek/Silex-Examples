# Monster truck à pneus souples

[English](README.md)

Conduire un pickup à quatre pneus déformables dans une arène géométrique de
freestyle : tables de saut, butte à quatre accès, grandes rampes, réception,
cuvette et petites bosses. Le sol brun conserve une grille pour lire la vitesse.
Les faces jaunes et rouges montrent les trajectoires, avec des bordures blanches.

## Lancer et conduire

Depuis la racine du workspace contenant `Silex-Examples/`, préparer une banque
native v3 avec les outils de `Packages/GFX.Audio/Native/EngineSimulator`, puis
compiler sans ouvrir de fenêtre :

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release -o Build/MonsterTruck-Drive-Response
Build/MonsterTruck-Drive-Response --engine-library /chemin/absolu/vers/EngineLibrary
```

Le son Chevrolet 454 est actif par défaut. Sans option, la banque est cherchée
sous `Build/EngineLibrary-Monster-Package`, relatif au répertoire courant. Le
chemin absolu explicite fonctionne depuis tout dossier. `--silent` conserve la
conduite sans ouvrir de moteur sonore ni de périphérique audio. Le HUD montre
le régime du moteur physique et le rapport engagé. L’interface et le rendu gardent leurs commandes habituelles.

| Commande | Action |
| --- | --- |
| Z maintenu | Accélération normale progressive |
| Maj + Z | Turbo : 25 % de couple supplémentaire, réponse plus franche |
| S maintenu | Marche arrière ; inversion progressive si le camion avance |
| Maj + S | Freinage renforcé sur quatre roues pour lever l’arrière |
| Q / D | Direction avant, gauche / droite depuis la caméra arrière |
| A / E ou ← / → | Direction arrière selon la direction voulue pour le nez |
| T | Coupler / séparer les essieux directeurs |
| Espace maintenu | Frein à main arrière |
| P | Gonflage Monster / Bas / Ferme, sans recommencer |
| Plus court / Plus long | Modifier le rapport de pont à l’arrêt, gaz relâchés |
| R | Recommencer avec le gonflage et la démultiplication sélectionnés |
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

Le moteur, l’embrayage et les différentiels de `GFX.Physics.WheelDrive3D`
entraînent réellement les jantes. Le moteur a un couple nominal maximal de
240 N·m, entre 850 et 7000 tr/min, pour les masses de ce montage de démonstration. La boîte
automatique utilise trois rapports rapprochés, 3,2 / 2,6 / 2,1, et une marche
arrière de −3,2. Elle monte à 4200 tr/min et descend à 1700 tr/min ; ses
transitions ouvrent puis referment l’embrayage. Une roue recevant du couple
sans appui empêche les montées de rapport. Le lancement dose la prise d’embrayage.

Le différentiel central redistribue le couple vers le pont qui conserve de
l’appui lorsque l’autre patine. Ce transfert est fourni par GFX.Physics avec
`differential_limited_slip_ratio:2.2` ; il évite de dépenser le couple dans les
roues avant délestées pendant l’accélération. La répartition gauche/droite de
chaque essieu reste distincte.

Le rapport de pont initial vaut 8, réglable de 6 à 12 avec les boutons. Une
valeur supérieure raccourcit la transmission : à régime égal, les roues tournent
moins vite ; à vitesse de roue égale, le moteur tourne plus vite. La multiplication
du couple change aussi. L’adhérence, la charge et les changements de rapport
continuent de limiter l’accélération réelle. Le réglage est refusé si le véhicule
ou les roues tournent encore, ou si les gaz ne sont pas relâchés. R conserve le
réglage ; les fichiers `Transmission.sx` et `Model.sx` portent la configuration
et la politique de conduite de cette démo.

En conduite normale, un gouverneur réduit progressivement la combustion à
l’approche de 4800 tr/min. Maj multiplie le couple disponible par 1,25 et ouvre
une réserve de régime jusqu’à 7000 tr/min. Cela donne de la reprise même lorsque
le régime normal est déjà atteint. Un moteur entraîné par les roues peut dépasser
le régime de combustion demandé, dans la limite physique de 7000 tr/min.
Le HUD indique « Turbo : actif » pendant la commande Maj + Z. Une impulsion
permet de cabrer ; maintenir le boost peut retourner le camion.

Le couple de chaque roue produit
une réaction opposée sur le châssis. Le frein avant atteint 1000 N·m par roue. Avec Maj, le freinage
agit sur les quatre roues : 1250 N·m à l’avant et 937,5 N·m à l’arrière. Le
frein à main arrière atteint 2200 N·m. Au sol, Z et S transmettent le nouveau
sens dès le premier pas, même lorsque le camion roule encore dans l’autre
sens. L’embrayage patine sous pression limitée pendant cette transition ; le
couple opposé ralentit puis relance le véhicule. Le régime de combustion est
limité pendant le patinage pour éviter un à-coup au raccrochage. La pression
tient compte du rapport de pont : une boîte plus courte réduit la
pression transitoire pour éviter un freinage brutal aux roues. La pleine
prise revient progressivement en 0,2 s. La masse et l’adhérence déterminent
toujours le temps nécessaire pour inverser le déplacement.

Maj avec la pédale opposée conserve le freinage renforcé suivant le déplacement
du châssis. En vol, la décision de freinage suit le sens de rotation des roues :
les pédales gardent leur sens pendant un salto. La pédale opposée freine les roues avant de les entraîner dans l’autre
sens ; Espace conserve le frein arrière pour agir sur la rotation en l’air.

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
Build/MonsterTruck-Drive-Response --check
Build/MonsterTruck-Drive-Response --scene-check
Build/MonsterTruck-Drive-Response --arena-check
Build/MonsterTruck-Drive-Response --slope-check
Build/MonsterTruck-Drive-Response --ramp-check
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/DriveChecks.sx --release -o Build/MonsterTruck-Drive-Checks
Build/MonsterTruck-Drive-Checks
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/AirborneChecks.sx --release -o Build/MonsterTruck-Airborne-Checks
Build/MonsterTruck-Airborne-Checks
```

Elles couvrent la physique, les gonflages, le centrage, les figures sur appuis
courts, les commandes, le HUD, les raccords du terrain et le roulage lent sur
les vraies facettes inclinées. `DriveChecks` compare aussi la reprise à la
propulsion antérieure, le boost en roulant, un cabrage récupérable et les
rapports de pont extrêmes. `AirborneChecks` couvre les orientations, les pédales
au sol/en vol et les rotations aériennes complètes. Les états sont comparés à
un et quatre workers.

`--single` choisit un worker pour jouer. `--profile` ouvre un parcours automatique
pendant douze secondes ; `--profile-slope` ouvre un test de six secondes,
freins maintenus sur une rampe. Le titre et le HUD identifient ces mesures.
`--profile-ramp` ouvre une mesure de douze secondes : montée lente de biais,
puis freinage sur la pente. `--ramp-check` vérifie huit approches sans fenêtre,
avec contrôle des talons et du sol. Les temps sans rendu ne permettent pas de
conclure sur les FPS graphiques.

## Son Chevrolet réutilisable

La source est `GFX.Audio.Engines.Library.driven_engine("454")` ; la démo ne
recopie aucun calcul acoustique. Elle fournit régime et charge par
`OperatingState`, puis reçoit des blocs prêts sans attente dans la boucle
physique. La file contient au plus cinq blocs de lecture et quatre demandes
natives, environ 98 ms hors périphérique. R réinitialise aussi le son.

Le son reçoit `engine_rpm` et le couple de combustion normalisé issus du moteur
physique. Il accompagne donc les passages de rapport, l’embrayage et les roues
en l’air, sans simuler une deuxième boîte. Le générateur de GFX.Audio reste
indépendant de GFX.Physics : `Library.engine` fournit son fonctionnement autonome
et sa boîte optionnelle ; `Library.driven_engine` accepte régime, charge et
contact fournis par n’importe quel jeu ou simulation. La configuration du camion
n’est pas imposée à ces autres usages.

Contrôle croisé hors ligne, sans fenêtre ni périphérique sonore :

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/TransmissionChecks.sx --release -o Build/MonsterTruck-Transmission-Checks
Build/MonsterTruck-Transmission-Checks /chemin/absolu/vers/EngineLibrary
```

Il vérifie les trois rapports, l’inversion de marche, les restrictions de
réglage, la stabilité des pneus, la corrélation régime/charge, la production PCM
et le reset, ainsi qu’une trajectoire physique identique avec et sans lecture
des données audio. `--scene-check` contrôle aussi les boutons à la souris,
Espace après focus et la conservation du réglage après R. L’écoute interactive
et la tenue graphique restent à contrôler sur la machine utilisée.

`ReversalChecks.sx` contrôle aussi les deux sens à 2 et 18 m/s, les rapports de
pont extrêmes à 12 m/s, l’annulation d’une inversion, le délai du couple et la
stabilité pendant la reprise d’embrayage :

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/ReversalChecks.sx --release -o Build/MonsterTruck-Reversal-Checks
Build/MonsterTruck-Reversal-Checks
```
