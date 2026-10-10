# Imposer une pose et libérer deux mannequins

Les deux mannequins partagent une hiérarchie de dix membres : torse, tête,
bras, avant-bras, cuisses et jambes. Les points blancs montrent les repères
d’articulation ; les blocs colorés montrent les formes décalées par rapport
à ces repères. Le mannequin or est modifiable, le bleu sert de référence.

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/RagdollPose/Main.sx --release
```

La scène démarre en pause.

- **Pose détendue** ou **Bras levés** impose immédiatement la pose du
  mannequin or et replace les deux instances à leur hauteur initiale.
  Le mannequin bleu conserve sa pose de référence.
- **Libérer / rejouer** replace les deux mannequins, annule leurs vitesses,
  puis lance une chute libre physique de 600 ms. La pause automatique garde
  les deux poses dans le champ et permet de les relire.
- **Espace** ou **Pause/Reprendre** interrompt ou reprend la chute. Après
  sa fin, reprendre relance la même courte chute depuis la hauteur initiale.
- **R** ou **Remettre à zéro** détruit puis recrée les assemblages dans
  leur pose détendue, en pause. **Échap** ferme la fenêtre.

Les membres restent liés pendant la chute. La pose imposée est un placement
immédiat, distinct du suivi physique d’une cible motorisée. Cette scène
n’a ni sol ni moteur ; les collisions internes sont explicitement supprimées.
Les deux instances restent indépendantes et peuvent normalement se heurter,
mais leurs placements et poses de ce parcours restent séparés.

La gravité vaut −9,81 m/s² sur Y ; chaque membre pèse 2 kg avec une inertie
isotrope de 0,2 kg·m². Les articulations swing/twist sont libres en rotation.
La simulation avance à 120 Hz, interpole les repères lus par `write_pose`
et actualise les mesures à 10 Hz. Les meshes sont préparés une seule fois.
Le contrôle sans fenêtre vérifie les parentés locales, les ancrages, les
origines des formes, la chute analytique à 60/120 Hz et les transforms rendus.

```sh
silex compile Silex-Examples/Sources/Physics3D/RagdollPose/Main.sx --release -o .silex/ragdoll-pose
.silex/ragdoll-pose --controls-check
.silex/ragdoll-pose --smoke
```

Le smoke impose une pose, chute, met en pause, reprend puis recrée les
assemblages pour une seconde chute. Il se ferme seul. L’essai manuel porte
sur la lisibilité des deux poses, les points d’articulation, la chute et les
commandes. Les contacts de sol, impulsions et cibles motorisées générales
restent des étapes de qualification distinctes du socle ragdoll.
