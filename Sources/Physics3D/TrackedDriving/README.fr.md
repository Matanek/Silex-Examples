# Conduire deux chenilles

Six manœuvres montrent comment deux bandes de roues suspendues font avancer
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
- **R** : recréer et rejouer le choix courant.
- **Espace** : suspendre/reprendre ; **Échap** : quitter.

Les boutons font les mêmes actions. Chaque choix recrée le véhicule au départ
et joue huit secondes : réception freinée pendant deux secondes, gaz à 80 %
pendant deux secondes, puis freinage et retour au repos pendant quatre secondes.
Il s’arrête ensuite pour permettre la comparaison ; R rejoue. La caméra suit
le châssis et la grille donne l’échelle en mètres. Le repère blanc reste fixe.

C’est un parcours de validation interactif, suivant les recettes Jolt/Silex
qualifiées : 100 kg, six roues de 30 cm, suspension 10000 N/m et 1000 N·s/m,
deux bandes d’inertie 2 kg·m², moteur 15 N·m et rapports ±1 avec différentiel 6.
La simulation avance à 120 Hz ; les mêmes recettes sont vérifiées à 60 Hz.
Les bandes sont un couplage mécanique idéal, sans maillons ni géométrie de
collision continue de chenille. Le contact utilise les rayons des six roues
sur un plan. Cette scène ne représente pas encore un essai tout-terrain.

## Vérification sans fenêtre

```sh
silex test Silex-Examples/Sources/Physics3D/TrackedDriving/Model.sx --nocache
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --controls-check
```

`--oracle-check` émet les 8 652 états des six recettes à 60/120 Hz dans le
format du témoin de qualification, pour contrôler que le rendu emploie bien
la même simulation. `--smoke` ouvre une fenêtre « TEST AUTOMATIQUE », joue les
six recettes, vérifie le cadrage et les transforms, puis se ferme avec son
marqueur final. Une fermeture anticipée n’est pas un succès de ce contrôle.
