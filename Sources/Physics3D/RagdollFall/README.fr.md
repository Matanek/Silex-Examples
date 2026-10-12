# Chute de deux mannequins : impulsion et sol

Le mannequin or commence avec les bras levés ; le bleu conserve une pose
détendue. Tous deux possèdent dix corps et neuf articulations bornées, sans
moteur. Coudes et genoux fléchissent dans un seul sens ; épaules et hanches ont
des limites latérales symétriques entre gauche et droite. Le cou reste dans
un cône limité. Ces réglages donnent une anatomie stylisée aux boîtes, sans
prétendre reproduire toute la mobilité humaine.
Les boîtes de collision ont les mêmes dimensions que les meshes.
Le monde utilise 32 passes de correction de position pour tenir les ancrages
pendant les impacts ; le réglage Physics par défaut reste à quatre.
Les membres non voisins peuvent entrer en collision : un avant-bras rencontre
le torse. Les paires parent/enfant restent filtrées au niveau de leur
articulation ; les limites des épaules empêchent le haut du bras de traverser
la poitrine. Le sol et les contacts entre instances participent à la simulation.

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
nombre d’impulsions, les contacts courants et le temps simulé, actualisés à
10 Hz. Les commandes et changements de pause ont un retour immédiat.

## Qualification

```sh
silex test Silex-Examples/Sources/Physics3D/RagdollFall/Model.sx
silex test Silex-Examples/Sources/Physics3D/RagdollFall/Main.sx
```

Les binaires proposent `--physics-check` (quatre recettes de quatre secondes,
avec/sans impulsion à 60/120 Hz, répétées après recréation), `--controls-check` (événements UI et clavier
jusqu’à l’effet physique) et `--smoke` (SDL/Metal, impulsion, pause exacte,
reprise, reset, seconde chute et fermeture automatique). Aucun de ces contrôles
ne produit de capture. Les contre-épreuves vérifient le contact avant-bras/torse,
le filtrage des voisins et la correction des flexions interdites. Les chutes
contrôlent les erreurs angulaires (< 0,08 rad), pénétrations entre membres
non voisins et haut du bras/torse (< 5 cm), ancrages (< 4 cm) et pénétrations
du sol (< 5 cm), à chaque pas en modes natifs
Debug/Release ; les buffers de pose et la géométrie sont réutilisés dans le rendu.

Pour diagnostiquer un coût, `--profile-cost` sépare le travail UI en pause du
coût de 480 pas physiques après échauffement. `--profile-scene` mesure la cadence
de la fenêtre réelle pendant deux pauses et deux chutes, puis ferme la fenêtre.
Le mode `--smoke` ajoute les vérifications détaillées à chaque pas physique ;
sa cadence mesure aussi ce travail de validation. Utiliser le lancement
interactif **Release**, sans ces options, pour apprécier la fluidité de la démo.

Le témoin Jolt headless qualifie séparément une chaîne de trois sphères et une
chute symétrique. Cet exemple à dix membres est un parcours consommateur testé,
sans revendication de trajectoire identique à Jolt pour ses impacts. Il ne
qualifie pas une pose motorisée ni la parité Jolt des limites pendant ces impacts. Le parcours
[RagdollPose](../RagdollPose/README.fr.md) conserve l’essai des poses et de la
chute libre courte.
