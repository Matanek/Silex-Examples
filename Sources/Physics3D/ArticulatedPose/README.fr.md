# Commander une épaule et un coude sous charge

Le bras bronze et la charge or pèsent chacun 2 kg. L’épaule blanche reste
fixée au support ; le coude cyan suit le bras. Les tiges grises montrent les
liaisons entre les deux articulations et les centres des masses. Le repère
rouge X, vert Y, bleu Z suit l’épaule ; le trait bleu au coude suit son axe de
flexion. Ces repères tournent avec les membres, pas avec les axes du monde.

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/ArticulatedPose/Main.sx --release
```

La scène démarre en pause. Aucune pose ne change automatiquement en usage manuel.

- **Pose +** commande X +14°, Y +11°, Z −9° à l’épaule et +20° au coude.
- **Pose −** inverse les quatre cibles : le coude fléchit dans le repère du
  bras pendant que l’épaule réoriente l’ensemble.
- **Recentrer** commande les quatre angles à zéro.
- **Espace** ou **Pause/Reprendre** arrête/reprend les deux membres.
- **R** ou **Remettre à zéro** restaure la pose initiale en pause ; **Échap** ferme.

Le pivot blanc doit rester fixé et le coude cyan doit suivre le bras sans
rupture de liaison. La charge doit suivre le coude. Les mesures distinguent
les angles d’épaule et l’angle du coude relatif au bras : une rotation mondiale
de la charge peut ainsi changer alors que l’angle local du coude reste stable.
Tester la lisibilité des deux mouvements, leur fluidité et les commandes.

Le poids déforme les servos élastiques ; le recentrage ne doit pas aligner
exactement les angles à zéro. L’épaule possède un budget de 60 N·m par axe,
raideur 120 et amortissement 20 ; le coude 40 N·m, raideur 80 et amortissement 15.
La simulation avance à 120 Hz, interpole les deux poses et affiche les mesures
à 10 Hz. Les meshes et orientations des tiges sont préparés une fois.
Les inerties sont isotropes, 0,4/0,2 kg·m² ; le sol et le support sont visuels.

La recette sans contacts correspond au consommateur qualifié
`GFX.Physics/Tests/Consumer/Tests/ArticulatedPose3D.sx`. Ses équilibres sont
comparés au témoin Jolt épinglé. Les écarts transitoires restent mesurés sans
parité générale. Ce parcours prépare les poses articulées ; la façade ragdoll,
la hiérarchie et l’auto-filtrage restent à construire.

Contrôle sans fenêtre puis smoke SDL/Metal de douze secondes physiques :

```sh
silex compile Silex-Examples/Sources/Physics3D/ArticulatedPose/Main.sx --release -o .silex/articulated-pose
.silex/articulated-pose --controls-check
.silex/articulated-pose --smoke
```

Le contrôle synthétise les clics et touches jusqu’à leur effet physique.
Le smoke parcourt les poses opposées puis recentre, interrompt les deux
membres, vérifie ancrages, équilibres et transforms rendus, puis se ferme seul.
