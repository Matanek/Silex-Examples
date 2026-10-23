# Conduire deux chenilles et franchir une rampe

Piloter le véhicule en continu, changer de terrain sur place et observer ses
six suspensions. Les rayons bleus à gauche et orange à droite suivent les
rotations physiques des roues ; les repères verts montrent les appuis présents.

Depuis la racine du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release
```

- Maintenir **Z / S** : avancer / reculer. Une inversion freine avant de passer
  l’autre rapport ; elle ne remet pas le véhicule au départ.
- Maintenir **Q / D**, ou **← / →** : tourner ; à très faible vitesse sans gaz,
  les bandes tournent en sens opposés pour pivoter.
- Maintenir **Espace** : freiner. Au relâchement des gaz, le véhicule peut rouler
  sur son élan ; le frein léger le maintient lorsqu’il est presque immobile.
- **B / F** : ajouter la rampe / revenir au plat, en conservant le véhicule,
  sa pose, sa vitesse et le temps de simulation. Le retrait d’un appui peut
  naturellement le faire retomber.
- **M** : activer ou couper un cycle automatique depuis l’état courant.
  Une commande de conduite reprend immédiatement la main.
- **P** : pause/reprise ; **R** : seul reset, départ sur le terrain choisi ;
  **Échap** : quitter.

Les cinq boutons concernent le terrain, le mode automatique, la pause et le
reset. La conduite utilise les touches tenues. Les relâchements et la perte de
focus libèrent les commandes, sans recréer le véhicule. B/F et M conservent la
pause ; R reprend la simulation. La conduite libre continue après quatorze
secondes. Le châssis et les rotations ne sont jamais imposés par les commandes.

La scène démarre au pied de la rampe. Pour comparer le parcours qualifié,
activer M puis utiliser R pour repartir explicitement du départ : stabilisation
2 s, gaz à 80 % pendant 5 s, freinage modéré à 4 % pendant 7 s. Le cycle ne se
réinitialise pas tout seul. Pour conduire soi-même, maintenir une touche ZQSD.
La conduite manuelle module les gaz et la différence de vitesse des bandes
avec la vitesse du véhicule ; elle garde le même moteur et les mêmes suspensions.

La caméra suit le châssis ; la grille indique des mètres. Le panneau donne les
vitesses des bandes, l’état du pilotage et le nombre d’appuis. Regarder la
montée, la disparition des appuis au sommet, le vol puis la reprise des charges.

Le modèle utilise 100 kg, six roues de 30 cm, suspensions 10000 N/m et
1000 N·s/m, deux bandes d’inertie 2 kg·m² et un moteur de 15 N·m. Les chenilles
sont un couplage idéal, sans maillons articulés. Six rayons heurtent le plan ou
une boîte de 8 × 0,4 × 6,03 m inclinée de 0,1 rad. Le frein modéré isole le
franchissement : un freinage maximal depuis environ 58 km/h bascule dans Jolt
à 120 Hz. Ni ce freinage extrême, ni les terrains généraux, ni la boîte
automatique au sol ne sont qualifiés par ce parcours.

## Vérification sans fenêtre

```sh
silex test Silex-Examples/Sources/Physics3D/TrackedDriving/Model.sx --nocache
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --controls-check
```

`--controls-check` conserve identité, pose, vitesse, rotors et temps à chaque
commande, puis vérifie les effets des touches tenues, du freinage, de la marche
arrière, des boutons et de la pause. R est contrôlé comme recréation distincte.
`--oracle-check` émet les 8 652 états historiques ; `--ramp-check`, les 5 044
états plat/rampe. Ils gardent la simulation des témoins qualifiés.
`--smoke` joue ces huit recettes dans une fenêtre « TEST AUTOMATIQUE » et
vérifie cadrage, roue/appui, rampe, pause et recréation avant fermeture.
Une fermeture anticipée ne valide pas ce contrôle.

`--live-smoke` vérifie dans une seconde fenêtre automatique la conduite tenue,
les virages, le frein, B/F sur place, M et la reprise manuelle, la pause et
la poursuite du temps au-delà de quatorze secondes.
