# Commander deux charnières perpendiculaires

Le bras bleu pivote autour de l’axe Z rouge du support. La charge or de
2 kg pivote autour de l’axe X vert situé au bout du bras. La liaison or
montre son déport en profondeur. Le but de l’essai manuel est de vérifier
que ces mouvements et leurs commandes se comprennent dans la vue oblique.

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/SpatialHinges/Main.sx --release
```

La scène démarre en pause et ne change aucune cible automatiquement.

- **Monter/Baisser le bras** : vise ±20° environ autour du pivot rouge.
  La charge suit ce support, en conservant son angle relatif au bras.
- **Lever/Abaisser la charge** : vise ∓26° environ autour de l’axe vert,
  en conservant la position du bras. Une cible déjà atteinte reste tenue ;
  choisir le bouton opposé pour voir un autre mouvement.
- **Freiner les deux** : interrompt les déplacements et retient les angles
  courants sous gravité. Les commandes de mouvement et de freinage reprennent
  la simulation depuis la pause.
- **Espace** ou **Pause/Reprendre** : arrête ou reprend les poses.
- **R** ou **Remettre à zéro** : revient à la pose horizontale en pause.
  **Échap** ferme la fenêtre.

Les cibles, angles entiers et numéro de commande confirment immédiatement
l’action ; le déplacement prend quelques secondes. Les moteurs demandent
±0,2 rad/s avec des capacités de 60/40 N·m, puis freinent près de la cible.
Le bras a une masse de 2 kg, inertie isotrope 0,4 kg·m² ; la charge une
inertie de 0,2 kg·m² et un déport de 0,8 m. Les collisions sont désactivées ;
la plateforme et les formes affichées sont illustratives. La caméra est fixe.

La qualification des réactions, documentée dans le guide `SpatialHinges3D`
du package `GFX.Physics`, porte sur un parcours à petits angles, deux masses
et deux déports avec Jolt.
Cette scène étend les poses observées, avec contrôles géométriques et de tenue
propres à son parcours ; elle ne revendique pas de parité Jolt à ces angles,
ni de contacts spatiaux ou de chaîne arbitraire.

Contrôle sans fenêtre et smoke graphique automatique :

```sh
silex compile Silex-Examples/Sources/Physics3D/SpatialHinges/Main.sx --release -o .silex/spatial-hinges
.silex/spatial-hinges --controls-check
.silex/spatial-hinges --smoke
```

Le contrôle synthétise de vrais clics et événements clavier puis vérifie les
mouvements séparés, cibles atteintes, freinage, pause, reset et poses Scene3D.
Le smoke exerce les deux axes, leur inversion simultanée et le freinage,
avec pause/reprise, puis ferme sa fenêtre explicitement automatique.
