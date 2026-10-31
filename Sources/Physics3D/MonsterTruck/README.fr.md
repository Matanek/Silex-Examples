# Monster truck à pneus souples

[English](README.md)

Cette démo assemble un pickup surélevé, quatre pneus déformables à bande de
roulement plate et des suspensions physiques dans un même monde. Le parcours
comprend des bosses, des blocs de plusieurs hauteurs, des marches et deux tremplins.

Utiliser Release pour l’essai interactif.

## Lancer la démo

Depuis la racine du workspace contenant `Silex-Examples/`, avec les packages locaux
liés à ce workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release
```

Cette commande compile puis ouvre une fenêtre interactive. Pour préparer le binaire
sans ouvrir de fenêtre :

```sh
silex compile Silex-Examples/Sources/Physics3D/MonsterTruck/Main.sx --backend native --release -o /private/tmp/silex-monster-truck-demo
```

Après compilation, lancer `/private/tmp/silex-monster-truck-demo` sans option pour
jouer. Ce chemin absolu permet de jouer depuis n’importe quel dossier.

| Commande | Action |
| --- | --- |
| Z maintenu | Accélérer ; inverser le couple si le véhicule recule |
| S maintenu | Freiner de l’avant et demander immédiatement le recul |
| Q / D maintenu | Roues avant, gauche / droite depuis la caméra arrière |
| A / E ou ← / → maintenu | Roues arrière, commande prioritaire sur le couplage |
| T | Coupler / séparer les deux essieux directeurs |
| Espace maintenu | Frein à main sur les roues arrière |
| Maj + Z | Boost |
| P | Gonflage : monster / bas / ferme, sans recommencer |
| R | Recommencer avec le gonflage sélectionné |
| Molette | Régler la distance de la caméra de poursuite |
| Échap | Quitter |

Le mode initial couple les deux essieux. Appuyer sur T pour les commander séparément
: Q/D pour l’avant, A/E ou les flèches pour l’arrière. Les touches arrière prennent
aussi la priorité en mode couplé. Braquer les deux essieux dans le même sens permet
un déplacement en crabe ; en sens opposés, le virage est plus serré. Les touches
arrière orientent les roues : lorsque seul l’arrière braque à gauche en marche
avant, le nez part à droite.

Le HUD est placé à gauche et indique le secteur courant. Les flèches jaunes donnent
le sens du parcours ; les damiers marquent le départ et la réception. Les bosses
sont cyan, les blocs orange, les tremplins rouges et les grandes marches violettes.

Pour un premier essai, partir tout droit : franchir la bosse et les deux reliefs
décalés, puis les trois blocs de 30, 50 et 70 cm. Continuer vers le tremplin et sa
zone de réception. Après ce passage, essayer les grandes marches et les bosses
alternées des deux zones latérales. Comparer ensuite le franchissement d'un même
obstacle avec les trois gonflages, sans réinitialiser le véhicule.

## Montage physique et limites

Chaque pneu mesure 2,20 m de diamètre pour 1,32 m de largeur, avec une jante de 1,32
m de diamètre et des rebords de 1,56 m. Il comporte 192 sommets et 384 triangles.
Ses flancs et 96 diagonales internes résistent au cisaillement latéral tout en
permettant l’écrasement au contact du sol. Son profil comporte une bande plate et
des flancs presque verticaux. Les 48 liaisons de talons issues du prototype
`SoftTire` échangent des impulsions avec la jante ; aucun sommet n'est fixé
artificiellement à celle-ci. Les quatre suspensions SixDOF relient leurs jantes
dynamiques au châssis dynamique, sans support fixe ni maintien vertical. Le moteur
applique un couple maximal de 1250 N·m par roue, avec sa réaction opposée au
châssis. En mode couplé, le braquage arrière vaut −65 % du braquage avant ; l’angle
diminue progressivement avec la vitesse, jusqu’à un minimum de 20°. S freine les
roues avant à 1000 N·m par roue et engage le couple inverse sur l’arrière pendant la
décélération ; Espace bloque la paire arrière à 2200 N·m par roue. La vitesse
traverse physiquement zéro avant que le camion recule. Les attaches de talons sont
dimensionnées pour le couple accru. Le centre de masse du châssis représente un
groupe moteur/transmission bas et légèrement avancé, pour exploiter la puissance. La
commande du moteur monte progressivement, avec un couple proportionnel à son
amplitude. Les suspensions offrent ±80 cm de course avec des ressorts de 1800 N/m et
un amortissement de 300 N·s/m. Les jantes possèdent un fût et deux rebords de
collision qui protègent les talons. Le pilotage tourne à 120 Hz, avec huit couplages
à 960 Hz et un sous-pas souple par couplage. Le profil rigide utilise huit
itérations de vitesse.

Les pressions 700, 250 et 1000 sont des coefficients du solveur, sans étalonnage en
bars. L’empattement mesure 4,10 m. Le châssis pèse 150 kg ; chaque jante ajoute 20
kg et chaque carcasse 9,6 kg. Les crampons affichés suivent les sommets déformés ;
les contacts sont ceux des sphères de collision des sommets. L'auto-collision et les
contacts souple/souple ne sont pas disponibles.

## Contrôles sans fenêtre

Une fois le binaire compilé :

```sh
/private/tmp/silex-monster-truck-demo --check
/private/tmp/silex-monster-truck-demo --scene-check
```

Ces deux modes quittent avant la création de l'application graphique. Le premier
exerce repos, gonflage, conduite, direction, freinage, franchissement et comparaison
à un/quatre workers, ainsi que le centrage des pneus sous direction arrière
alternée, l’inversion moteur et la course sur un choc de référence. Le second
contrôle commandes, reset, maillages, dimensions du HUD et cadrage par calcul, sans
capturer d’image.

`--single` choisit un worker pour l'essai interactif. `--profile` ouvre une fenêtre
automatique pendant douze secondes et mesure les frames ; ce n'est pas le mode de
jeu. Les temps sans rendu ne permettent pas de conclure sur les FPS du camion.