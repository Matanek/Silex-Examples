# Conduire deux chenilles et franchir une rampe

Huit manœuvres montrent comment deux bandes de roues suspendues font avancer
et tourner un châssis. Les roues gardent leur axe ; les vitesses relatives des
bandes produisent les courbes et leur contre-rotation produit le pivot.
Les rayons colorés lisent la rotation physique de chaque roue. Bleu à gauche,
orange à droite ; les petits repères verts indiquent les appuis présents.
Le bandeau donne les vitesses réelles des deux bandes et les phases de conduite.

Depuis la racine du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release
```

- **Z** : avancer ; **S** : reculer.
- **← / →** : courbe à gauche / à droite.
- **P** : pivot, bandes en sens opposés.
- **G** : avancer sans adhérence ; les roues tournent, le châssis reste sur place.
- **B** : rampe finie ; **F** : témoin plat avec les mêmes commandes.
- **R** : recréer et rejouer le choix courant.
- **Espace** : suspendre/reprendre ; **Échap** : quitter.

La scène démarre sur la rampe. B et F recréent le véhicule et jouent quatorze
secondes : deux secondes de stabilisation, cinq secondes à 80 % de gaz, puis
sept secondes de freinage modéré à 4 %. Sur la rampe, regarder les appuis verts
se perdre au sommet, le châssis poursuivre son vol, puis les six roues reprendre
leur charge à la réception. La phase et le compteur d’appuis suivent ces états.

Les boutons font les mêmes actions. Les six manœuvres précédentes (Z/S/flèches/P/G)
restent des séquences de huit secondes : réception freinée pendant deux secondes,
gaz à 80 % pendant deux secondes, puis freinage au repos pendant quatre secondes.
Il s’arrête ensuite pour permettre la comparaison ; R rejoue. La caméra suit
le châssis et la grille donne l’échelle en mètres. Le repère blanc reste fixe.

C’est un parcours de validation interactif, suivant les recettes Jolt/Silex
qualifiées : 100 kg, six roues de 30 cm, suspension 10000 N/m et 1000 N·s/m,
deux bandes d’inertie 2 kg·m², moteur 15 N·m et rapports ±1 avec différentiel 6.
La simulation avance à 120 Hz ; les mêmes recettes sont vérifiées à 60 Hz.
Les bandes sont un couplage mécanique idéal, sans maillons ni géométrie de
collision continue de chenille. Le contact utilise les rayons des six roues
sur le plan et le dessus d’une rampe de 8 × 0,4 × 6,03 m inclinée de 0,1 rad.
Le profil mécanique reste le même. Le freinage modéré isole le franchissement :
le freinage maximal depuis environ 58 km/h fait basculer la référence Jolt à
120 Hz. La recette ne qualifie ni ce freinage extrême, ni les terrains généraux,
ni la boîte automatique au sol.

## Vérification sans fenêtre

```sh
silex test Silex-Examples/Sources/Physics3D/TrackedDriving/Model.sx --nocache
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --controls-check
```

`--oracle-check` émet les 8 652 états des six recettes à 60/120 Hz dans le
format du témoin de qualification, pour contrôler que le rendu emploie bien
la même simulation. `--ramp-check` émet les 5 044 états du témoin plat/rampe,
identiques au benchmark `TrackedRamp.sx`. `--smoke` ouvre une fenêtre « TEST AUTOMATIQUE », joue les
huit recettes, vérifie le cadrage et les transforms, puis se ferme avec son
marqueur final. Une fermeture anticipée n’est pas un succès de ce contrôle.
