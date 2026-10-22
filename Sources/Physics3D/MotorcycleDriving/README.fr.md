# Conduire une moto et comparer son équilibre

Maintenir les commandes fait rouler et braquer la moto librement. Le châssis
bronze, les deux roues et leurs suspensions suivent la simulation. La roue
avant braque ; les rayons colorés montrent la rotation réelle des roues.
Les petits repères verts indiquent les appuis. La caméra suit le châssis et
la grille donne l’échelle en mètres ; le poteau blanc reste fixe au départ.

Depuis la racine du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release
```

- Maintenir **Z** : gaz à 80 % ; relâcher : roue libre, embrayage ouvert.
- Maintenir **S** : freinage débrayé, prioritaire sur les gaz.
- Maintenir **← / →** : braquer à gauche / à droite ; relâcher : recentrer.
- **A** : activer/couper l’assistance d’équilibre.
- **L** : activer/couper la limite de braquage liée à la vitesse.
- **P** : appliquer une impulsion latérale de roulis de 150 N·m·s.
- **R** : recréer au départ en conservant les deux réglages d’assistance.
- **Espace** : suspendre/reprendre ; **Échap** : quitter.

Les boutons commandent les cinq actions ponctuelles. Les gaz, le frein et le
braquage se relâchent à la perte de focus, à la pause et à la recréation. Une
poussée demandée pendant la pause attend la reprise ; une recréation l’annule.

Pour comparer l’équilibre, appuyer sur R, attendre les deux appuis puis sur P.
Avec l’assistance, la moto se redresse. Couper l’assistance avec A, recréer avec
R et répéter la poussée : elle tombe. Sans perturbation, une moto exactement
verticale peut rester verticale même avec l’assistance coupée. L est une limite
de direction, pas le correcteur d’équilibre ; la différence apparaît surtout
en braquant à vitesse élevée.

Cette scène de validation emploie le profil qualifié contre Jolt : 100 kg,
inertie isotrope 100 kg·m², roues de 30 cm, ressorts de 10000 N/m amortis à
1000 N·s/m, moteur idéal de 20 N·m et transmission manuelle 3×3,42 vers la roue
arrière. La simulation avance à 120 Hz. L’assistance est un actuateur idéal,
sans simulation de pilote. Les contacts des roues sont des rayons sur un plan ;
les pneus ne sont pas des corps rigides séparés. Ce n’est pas encore un parcours
tout-terrain ni une moto calibrée sur un véhicule réel.

## Vérification sans fenêtre

```sh
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --nocache
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --controls-check
```

`--oracle-check` émet les 8 652 états des six recettes qualifiées à 60/120 Hz :
départ, virages miroirs, absence d’adhérence et poussée avec/sans assistance.
Le mode interactif ne rejoue pas ces séquences. `--smoke` ouvre une fenêtre
« TEST AUTOMATIQUE », exécute ces six recettes, vérifie cadrage, transforms,
roues braquées, appuis, pause et recréation, puis se ferme avec son marqueur
final. Une fermeture anticipée ne valide pas ce contrôle.
