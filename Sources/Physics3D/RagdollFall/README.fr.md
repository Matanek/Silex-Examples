# Chute de deux mannequins : impulsion et sol

Le mannequin or commence avec les bras levés ; le bleu conserve une pose
détendue. Tous deux possèdent dix corps et neuf articulations libres, sans
moteur. Les boîtes de collision ont les mêmes dimensions que les meshes.
Le monde utilise huit passes de correction de position pour tenir les ancrages
pendant les impacts ; le réglage Physics par défaut reste à quatre.
Leurs collisions internes sont désactivées ; le sol et les contacts entre
instances participent à la simulation.

Depuis la racine du workspace ou du groupe de Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/RagdollFall/Main.sx --release
```

- **Libérer / rejouer** remet les poses initiales et démarre la chute.
- **Pousser le torse**, ou **P**, applique une impulsion excentrée de
  `(6, 2, 3)` N·s au torse or et reprend la simulation si elle était en pause.
  Pendant les quatre secondes, plusieurs impulsions peuvent se cumuler.
- **Espace** ou le bouton de pause fige/reprend les deux assemblages.
- **R** ou **Remettre à zéro** détruit et recrée les assemblages en pause.
- **Échap** ferme la fenêtre.

Après quatre secondes de simulation, une pause automatique permet de relire
les poses. Libérer, P ou reprendre après cette fin démarre un nouvel essai
depuis les poses initiales. Les touches logiques sont indépendantes de leur
position physique ; l’auto-répétition n’applique pas une série d’impulsions.
Les points blancs sont les repères d’articulation. Le compteur affiche le
nombre d’impulsions, les contacts courants et le temps simulé.

## Qualification

```sh
silex test Silex-Examples/Sources/Physics3D/RagdollFall/Model.sx
silex test Silex-Examples/Sources/Physics3D/RagdollFall/Main.sx
```

Les binaires proposent `--physics-check` (quatre recettes de quatre secondes,
avec/sans impulsion à 60/120 Hz, répétées après recréation), `--controls-check` (événements UI et clavier
jusqu’à l’effet physique) et `--smoke` (SDL/Metal, impulsion, pause exacte,
reprise, reset, seconde chute et fermeture automatique). Aucun de ces contrôles
ne produit de capture. Ancrages et coins des boîtes sont vérifiés en modes natifs
Debug/Release ; les buffers de pose et la géométrie sont réutilisés dans le rendu.

Le témoin Jolt headless qualifie séparément une chaîne de trois sphères et une
chute symétrique. Cet exemple à dix membres est un parcours consommateur testé,
sans revendication de trajectoire identique à Jolt pour ses impacts. Il ne
qualifie ni limites actives ni pose motorisée. Le parcours
[RagdollPose](../RagdollPose/README.fr.md) conserve l’essai des poses et de la
chute libre courte.
