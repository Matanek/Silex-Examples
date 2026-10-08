# Commander une crémaillère jusqu’à ses butées

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/RackServo/Main.sx --release
```

La scène démarre en pause. Le pignon jaune entraîne la barre bleue, retenue
par une glissière. Les repères verts marquent les deux fins de course.

- **Vers la droite**, puis **Vers la gauche** : la barre rejoint chaque butée.
  Le moteur reste actif et pousse la butée ; l’état et le couple l’indiquent.
  Chaque bouton choisit explicitement son côté et reprend la simulation.
- **Revenir au centre** : le moteur ramène la barre au milieu du rail.
- **Espace** ou **Pause/Reprendre** : arrête ou reprend la simulation.
- **R** ou **Remettre à zéro** : rétablit la pose initiale, en pause.
  **Échap** ferme la fenêtre.

Le rapport vaut 2 rad/m, la course ±0,6 m. Les cibles du pignon sont ±1,5 rad,
avec 12 N·m au maximum, une raideur de 15 et un amortissement de 8. Le pas
physique est fixe à 120 Hz. La butée arrête la barre à ±1,2 rad de pignon,
avant sa cible ; au repos le couple vaut ±4,5 N·m. Les dents et repères sont
décoratifs : la transmission vient de la contrainte, sans collision de dents.

La charnière prend le chemin angulaire court. Des cibles ±2 rad pousseraient
l’autre sens à l’inversion et pourraient rester bloquées par le rail ; cet
exemple choisit des commandes dont le chemin atteint le côté demandé.
La correction de pose à la première butée reste progressive. Le témoin
comparatif conserve les écarts transitoires de Silex et Jolt à 60/120 Hz ; il
ne garantit pas une phase inférieure à 0,002 rad à chaque pas et toute cadence.

Vérification sans fenêtre :

```sh
silex compile Silex-Examples/Sources/Physics3D/RackServo/Main.sx --release -o .silex/rack-servo
.silex/rack-servo --controls-check
```

Ce contrôle synthétise les clics et touches, vérifie les deux butées, le centre,
le reset et les poses transmises au rendu. Le smoke natif ouvre une fenêtre
et la ferme après neuf secondes simulées ; le lancer seulement quand une
fenêtre convient :

```sh
.silex/rack-servo --smoke
```

Le lancement normal reste manuel. La scène ne qualifie ni une chaîne spatiale
quelconque, ni des axes libres, ni des collisions de formes.
