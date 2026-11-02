# Essayer le moteur V8

[English](README.md)

Maintenir **Espace** fait monter le régime de 800 à 6 600 tr/min ; relâcher
ramène progressivement au ralenti avec une variation de frein moteur.
Le compte-tours et le son suivent le même modèle. La perte de focus relâche
les gaz ; un nouvel appui est nécessaire au retour.

Depuis `SilexProject/`, ou la racine du groupe de travail d'une Spec :

```sh
silex run Silex-Examples/Sources/EngineAudio/Main.sx --release
```

La fenêtre contient quatre réglages : échappement feutré/ouvert, texture
régulière/rugueuse, charge et volume. La charge augmente l'effort audible et
ralentit la montée en régime du banc. Le bouton « Réglages initiaux » restaure
les valeurs de départ. Le volume est lissé dans les échantillons ; il ne
relance pas la lecture. Le profil est un V8 fixe pour ce premier essai.

Ce prototype utilise `GFX.Audio.Synthesis.Engine` : pulsations de combustion,
deux échappements, bruit modulé, résonances et saturation douce. Il n'utilise
aucune boucle enregistrée et ne simule pas les pièces ou les gaz d'un moteur.
Le profil privilégie un corps de combustion prolongé dans le grave, en gardant
la fréquence des combustions liée au régime. Le niveau initial du banc est
ajusté pour comparer les timbres. La qualité reste à apprécier à l'écoute.

## Vérifier sans ouvrir la fenêtre

La CLI ne transmet pas les options de ce programme : compiler d'abord, puis
passer les arguments à l'exécutable. Toujours compiler depuis la racine du
workspace ou du groupe de Spec, avec ce chemin d'entrée explicite :

```sh
silex compile Silex-Examples/Sources/EngineAudio/Main.sx --release -o .silex/engine-audio
.silex/engine-audio --check
.silex/engine-audio --render .silex/engine-audio.wav
```

`--check` vérifie les événements clavier et de focus, la réponse du régime,
la construction du dessin et la continuité du modèle entre blocs, sans ouvrir
le périphérique audio. `--render` écrit 12 secondes en WAV stéréo 48 kHz :
ralenti, montée, maintien puis décélération. Un dernier argument `smooth`
supprime la rugosité et ferme l'échappement ; `sine` fournit un témoin sinusoïdal
à fréquence de combustion équivalente. Leurs niveaux diffèrent ; égaliser les
niveaux avant une comparaison perceptive. Ces témoins n'isolent pas chaque filtre.

`--measure` émet les temps de 1 000 blocs de synthèse de 480 frames après
échauffement. Il exclut transfert PCM, interface et périphérique ; ce n'est pas
une mesure de latence ni une qualification globale pour le jeu.

`--smoke` ouvre un scénario automatique de cinq secondes, clairement indiqué
dans la fenêtre, puis ferme. Il vérifie l'exécution native et l'alimentation,
sans remplacer un essai réel d'Espace et des curseurs.

## Horloges et limites

Le banc fait évoluer son régime par quanta audio de 10 ms, indépendamment des
frames graphiques. La lecture retient au plus 2 880 frames de file et un bloc
de 480 frames, soit 70 ms d'avance de production à 48 kHz. La sortie du mixer
et du périphérique s'ajoute à cette avance, ainsi que la propagation acoustique
du profil d'échappement ; le compteur n'est pas une mesure
de la frame exacte entendue. La lecture commence lors de la première mise à
jour de la fenêtre, après sa préparation.

Le journal de fermeture indique les observations de file vide. Ce compteur
échantillonné n'est pas un historique exhaustif des interruptions audibles.
Le débit de synthèse seul ne suffit pas à certifier le comportement sous une
charge de jeu ; cette qualification et le raccord au monster truck sont ultérieurs.
