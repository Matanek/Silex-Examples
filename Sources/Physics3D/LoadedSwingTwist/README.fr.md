# Commander une orientation composée sous charge

La charge or de 2 kg pivote autour du point blanc fixe. Les trois tiges grises
forment une attache rigide déportée ; les axes rouge X, vert Y et bleu Z montrent
le repère moteur attaché à la charge. Les servos commandent ensemble la torsion
X et les inclinaisons Y/Z. Ce parcours rend observable la recette qualifiée
par `GFX.Physics/Tests/Consumer/Tests/LoadedSwingTwist3D.sx` ; il prépare la
lecture de poses motorisées, sans constituer un ragdoll.

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/LoadedSwingTwist/Main.sx --release
```

La scène démarre en pause. Choisir une cible reprend la simulation ; aucune
cible ne change automatiquement en usage manuel.

- **Cible +** commande environ X +14°, Y +11°, Z −9°.
- **Cible −** inverse les trois cibles ; la charge et ses axes s’orientent dans
  l’autre sens tout en conservant le pivot.
- **Recentrer** commande les trois angles à zéro.
- **Espace** ou **Pause/Reprendre** arrête/reprend le mouvement.
- **R** ou **Remettre à zéro** restaure la pose initiale en pause ; **Échap** ferme.

Les angles actuels, leurs cibles et les couples sont affichés dix fois par
seconde. L’ancrage doit rester au pivot blanc, le mouvement doit converger et
l’inversion doit être lisible. Les axes colorés suivent le repère moteur tourné
de 0,35 rad dans la charge ; ils ne désignent pas les axes fixes du monde.

Le poids décale l’équilibre par rapport à la cible. La raideur de 80 N·m/rad et
l’amortissement de 15 N·m·s/rad sont finis : **Recentrer** ne doit pas aligner
exactement les trois angles sur zéro. Chaque axe possède un budget de 30 N·m.
La simulation tourne à 120 Hz et le rendu interpole les poses ; caméra fixe,
inertie isotrope 0,4 kg·m², gravité −9,81 Y. Le déport local est
(0,5 ; 0,2 ; 0,4) m ; le sol, le support et les tiges sont visuels.
La recette n’a aucun contact ni deuxième articulation dynamique.

Les équilibres et bilans sont comparés à Jolt. L’égalité des réponses
transitoires entre moteurs reste non acquise. L’essai humain vérifie la
lisibilité et la fluidité du mouvement composé, ainsi que les commandes.

Contrôle sans fenêtre puis smoke SDL/Metal de neuf secondes :

```sh
silex compile Silex-Examples/Sources/Physics3D/LoadedSwingTwist/Main.sx --release -o .silex/loaded-swing
.silex/loaded-swing --controls-check
.silex/loaded-swing --smoke
```

Le contrôle synthétise les clics et événements clavier jusqu’à leur effet
physique, vérifie inversion, recentrage, répétition d’Espace, reset et poses
rendues. Le smoke parcourt les trois cibles, interrompt la simulation puis la
reprend, vérifie les équilibres et les transforms affichés, et se ferme seul.
