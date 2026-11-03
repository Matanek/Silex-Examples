# Composer et écouter un moteur

Cette nouvelle démo emploie exclusivement le générateur par pièces de GFX.Audio.
Le banc `EngineAudio` reste disponible séparément pour comparer ses sons.

Depuis la racine du workspace ou du groupe de Spec :

```sh
silex compile Silex-Examples/Sources/EngineWorkshop/Main.sx --release -o Build/EngineWorkshop
Build/EngineWorkshop
```

**M** ou le bouton bascule le contact. Le régime demandé, la charge et
l’accélérateur pilotent le son ; **Espace** maintenu donne des gaz à 7 000 tr/min.
Relâcher revient au régime choisi. La perte de focus relâche cette commande.
Le volume d’écoute est séparé des quatre voies du moteur.

Choisir V8, mono 450 quatre temps ou mono 250 deux temps, puis modifier les
pièces. Les changements sont préparés après 120 ms sans mouvement de réglage et
fondus sur 50 ms. La dernière modification en attente remplace la précédente.
Les longueurs affichées concernent la première ligne ; les autres lignes
conservent leurs écarts de parcours. Les autres réglages d’échappement sont
appliqués aux lignes ensemble.

- **Bloc et culasse** : cylindres, cycle, alésage, course, chambre et durée de combustion.
- **Admission** : conduit, boîte à air et absorption du filtre.
- **Échappement** : collecteurs, lignes et silencieux.
- **Mécanique et turbo** : masse, amortissement, roue, pression maximale et inertie.
- **Écoute des pièces** : isoler une voie en mettant les autres niveaux à zéro.

La cylindrée et la compression géométrique se calculent depuis les pièces.
Un assemblage incompatible est refusé en conservant le son précédent. Ajuster
la chambre lorsque le rapport dépasse 2..25. « Remonter le modèle initial »
restaure les pièces et le mix du modèle sélectionné, sans imposer un redémarrage.

La page défile et les cartes se réorganisent selon la largeur de fenêtre.
La synthèse, les phases, les filtres et les transitions appartiennent au package.
La démo possède uniquement le banc de régime, les contrôles et l’alimentation
du flux borné : blocs 480 frames, file 1 440 frames à 48 kHz, au plus 40 ms de
PCM préparé/en file hors sortie du périphérique.

```sh
Build/EngineWorkshop --check
Build/EngineWorkshop --render Build/EngineWorkshop.wav
silex compile Silex-Examples/Sources/EngineWorkshop/Measure.sx --release -o Build/EngineWorkshop-Measure
Build/EngineWorkshop-Measure
```

`--check` n’ouvre ni fenêtre ni périphérique ; il vérifie modèles, remplacement
de dimensions/topologie/turbo, dessin à trois largeurs et arrêt. Le WAV contient
12 s : ralenti, montée en charge avec turbo, changement de silencieux, retour et
arrêt. Le programme de mesure séparé chronomètre cinq fois 480 000 frames par source, pour un puis
huit V8 avec turbo à 6 000 tr/min ; périphérique, transfert PCM et UI exclus.

Le modèle acoustique est simplifié. Les sons et la lisibilité de l’atelier
restent à qualifier par l’écoute et l’usage ; le 2T ne simule pas encore le pot
de détente à cônes ou le balayage détaillé. Aucun son n’est présenté comme une
reproduction exacte d’un véhicule commercial. L’ancien banc n’est pas remplacé.
