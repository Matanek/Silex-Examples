# Faire monter et descendre une charge sur le rail vertical

Le bras bleu est retenu par une charnière au monde. Il porte une glissière
verticale verte déportée de 0,8 m, avec une sphère or de 2 kg. Le parcours manuel
sert à lire ce mélange de deux familles et ses commandes ; les bilans de la
recette sous gravité sont déjà qualifiés dans Physics `SpatialRail3D`.

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/SpatialRail/Main.sx --release
```

La scène démarre en pause, sans changement automatique de cible.

- **Abaisser jusqu’au plan** reprend la simulation. La sphère descend sur le
  rail ; au premier contact, le moteur freine et retient la course atteinte.
  **CONTACT ATTEINT** confirme l’arrêt, avec un petit repère vert au point mesuré.
- **Lever la charge** reprend la simulation et monte vers +15 cm de course.
  **CHARGE LIBRE** indique la libération ; le repère de contact disparaît.
- **Freiner** arrête la course et tient la position courante.
- **Espace** ou **Pause/Reprendre** arrête/reprend la simulation.
- **R** ou **Remettre à zéro** remet la course à zéro en pause ; **Échap** ferme.

La course et sa cible sont affichées en centimètres, avec le numéro de commande.
Les mesures se mettent à jour dix fois par seconde. Le rail et la traverse
restent liés au bras ; seule la sphère se déplace verticalement. La caméra est
fixe. Rayon 0,15 m, plan physique à Y=1,58 m, centres initiaux Y=1,8 m, masses
2/2 kg et inerties isotropes 0,4/0,2 kg·m². Capacités : charnière 60 N·m,
glissière 40 N ; seule la sphère touche le plan, sans friction ni restitution.

La commande freine au premier contact et ne pousse pas vers une cible
inaccessible. Le parcours ajoute lecture visuelle, montée jusqu’à +15 cm et
interactions à la recette comparative ; il ne qualifie pas une chaîne arbitraire.

Contrôle sans fenêtre puis smoke graphique automatique :

```sh
silex compile Silex-Examples/Sources/Physics3D/SpatialRail/Main.sx --release -o .silex/spatial-rail
.silex/spatial-rail --controls-check
.silex/spatial-rail --smoke
```

Le contrôle synthétise clics et événements clavier jusqu’à leur effet physique,
vérifie tenue pendant dix secondes, relèvement, freinage, pause, reset et poses
affichées. Le smoke SDL/Metal suit deux passages au contact puis se ferme seul.
