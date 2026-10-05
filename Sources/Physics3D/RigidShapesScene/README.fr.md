# Corps rigides, balayages et ouverture de terrain

Lancer depuis la racine du workspace, ou celle du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/RigidShapesScene/Main.sx --release
```

Au premier plan, le cylindre jaune, le cylindre effilé bleu et la capsule
effilée orange tombent sur leurs plateformes. La sphère verte passe dans
l’ouverture de la grille et se pose sur le plan inférieur. La grille choisit
explicitement la diagonale `first_to_opposite` et retire les triangles qui
utilisent son sommet central masqué. Le plan physique est infini ; son dessin
montre seulement une région de la scène.

Au fond, trois volumes bleus — capsule, boîte et enveloppe convexe — avancent
jusqu’à leur première collision. Les points verts marquent les témoins de
contact. Les maillages et ces trois requêtes sont préparés une seule fois au
démarrage ; les mises à jour du rendu concernent les sept poses mobiles.
Le monde avance avec un pas fixe de 1/120 s ; le rendu interpole ses deux poses.

**Espace** met en pause, **R** relance les chutes, **Échap** ferme la fenêtre.
Les cycles recommencent automatiquement toutes les quatre secondes. Le mode
`--smoke` vérifie deux cycles puis ferme sa seule fenêtre ; les FPS sont
rapportés chaque seconde. Le premier échantillon comprend l’échauffement.

Le CCD du moteur reste translationnel à orientations initiales. Pour un
témoin headless de sa limite en rotation :

```sh
silex run Silex-Benchmarks/Sources/Physics3D/RotationLimit.sx --release
```

Une rotation de 180° pendant un pas manque le mur dans les deux scénarios,
même avec une translation parallèle. Les 36 sous-pas le détectent dans ces
cas ; ce nombre n’est pas une garantie universelle de CCD rotationnel.
Les grilles physiques sont exactes, immuables et fixes ; elles ne fournissent
pas de compression, de mise à jour locale quantifiée ni de garantie pour un
relief arbitraire ou un très grand terrain.
