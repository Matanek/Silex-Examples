# Monster truck à pneus souples

[English](README.md)

Cette démo assemble un pickup surélevé,
quatre pneus déformables à bande de roulement plate et des suspensions physiques
dans un même monde. Le parcours comprend des bosses, des blocs de plusieurs
hauteurs, des marches et deux tremplins.

Utiliser Release pour l’essai interactif.

## Lancer la démo

Depuis la racine du workspace contenant `Silex-Examples/`, avec les packages
locaux liés à ce workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release
```

Cette commande compile puis ouvre une fenêtre interactive. Pour préparer le
binaire sans ouvrir de fenêtre :

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release -o /private/tmp/silex-monster-truck-demo
```

Après compilation, lancer `/private/tmp/silex-monster-truck-demo` sans option
pour jouer. Ce chemin absolu permet de jouer depuis n’importe quel dossier.

| Commande | Action |
| --- | --- |
| Z maintenu | Accélérer ; freiner d'abord si le véhicule recule |
| S maintenu | Freiner, puis reculer |
| Q / D maintenu | Tourner à gauche / droite depuis la caméra arrière |
| Espace maintenu | Frein à main sur les roues arrière |
| Maj + Z | Boost |
| P | Gonflage : cross / bas / ferme, sans recommencer |
| R | Recommencer avec le gonflage sélectionné |
| Molette | Régler la distance de la caméra de poursuite |
| Échap | Quitter |

Le HUD est placé à gauche et indique le secteur courant. Les flèches jaunes
donnent le sens du parcours ; les damiers marquent le départ et la réception.
Les bosses sont cyan, les blocs orange, les tremplins rouges et les grandes
marches violettes.

Pour un premier essai, partir tout droit : franchir la bosse et les deux reliefs
décalés, puis les trois blocs de 30, 50 et 70 cm. Continuer vers le tremplin et
sa zone de réception. Après ce passage, essayer les grandes marches et les
bosses alternées des deux zones latérales. Comparer ensuite le franchissement
d'un même obstacle avec les trois gonflages, sans réinitialiser le véhicule.

## Montage physique et limites

Chaque pneu comporte 192 sommets et 384 triangles. Son profil comporte une
bande plate et des flancs presque verticaux. Les 48 liaisons de talons issues du
prototype `SoftTire` échangent des impulsions avec la jante ; aucun sommet n'est
fixé artificiellement à celle-ci. Les quatre suspensions SixDOF relient leurs
jantes dynamiques au châssis dynamique, sans support fixe ni maintien vertical.
Le moteur applique un couple, avec sa réaction opposée au châssis. Les jantes
possèdent un fût et deux rebords de collision qui protègent les talons.
Le pilotage tourne à 120 Hz, avec quatre couplages à 480 Hz et deux sous-pas
souples par couplage. Le profil rigide utilise huit itérations de vitesse.

Les pressions 450, 250 et 1000 sont des coefficients du solveur, sans étalonnage
en bars. Le châssis pèse 150 kg ; chaque jante ajoute 20 kg et chaque carcasse
9,6 kg. Les crampons affichés suivent les sommets déformés ; les contacts sont
ceux des sphères de collision des sommets. L'auto-collision et les contacts
souple/souple ne sont pas disponibles.

## Contrôles sans fenêtre

Une fois le binaire compilé :

```sh
/private/tmp/silex-monster-truck-demo --check
/private/tmp/silex-monster-truck-demo --scene-check
```

Ces deux modes quittent avant la création de l'application graphique. Le premier
exerce repos, gonflage, conduite, direction, freinage, franchissement et comparaison
à un/quatre workers. Le second contrôle commandes, reset, maillages, dimensions du
HUD et cadrage par calcul, sans capturer d’image.

`--single` choisit un worker pour l'essai interactif. `--profile` ouvre une fenêtre
automatique pendant douze secondes et mesure les frames ; ce n'est pas le mode
de jeu. Les temps sans rendu ne permettent pas de conclure sur les FPS du camion.
