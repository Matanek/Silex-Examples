# Essayer le moteur V8

[English](README.md)

La fenêtre s'ouvre moteur éteint. Le bouton **Démarrer / Arrêter** ou la touche
**M** bascule le contact. Le compte-tours indique le démarrage et l'extinction ;
l'alimentation monte progressivement au démarrage. À l'arrêt, elle décroît sur
environ 350 ms ; les combustions engagées finissent et le régime continue de
retomber par inertie. La pression et la réverbe finissent ensuite de résonner.
Espace est ignoré moteur éteint. Un nouvel appui est nécessaire pour accélérer
après un changement de contact. Les réglages initiaux ne changent pas le contact.

Maintenir **Espace** fait monter le régime de 800 à 6 600 tr/min ; relâcher
ramène progressivement au régime choisi avec une variation de frein moteur.
Le compte-tours et le son suivent le même modèle. La perte de focus relâche
les gaz ; un nouvel appui est nécessaire au retour.

Depuis `SilexProject/`, ou la racine du groupe de travail d'une Spec :

```sh
silex run Silex-Examples/Sources/EngineAudio/Main.sx --release
```

La fenêtre contient cinq réglages : échappement feutré/ouvert, texture
régulière/rugueuse, charge, réverbe courte et volume. La charge modifie l'effort
audible, y compris aux régimes maintenus, et ralentit la montée en régime du banc.
Les boutons 800, 1 000 et 1 500 choisissent le régime à retrouver au relâchement
d'Espace, puis à maintenir pour comparer les timbres. Le bouton « Réglages initiaux » restaure
les valeurs de départ. Le volume est lissé dans les échantillons ; il ne
relance pas la lecture. La réverbe descend jusqu'au son sec ; son mélange est
lissé, initialement à 6 %, avec une décroissance nominale de 0,22 seconde.
Son historique continue d'avancer à zéro. Le profil est un V8 fixe.

Ce prototype utilise `GFX.Audio.Synthesis.Engine` : pulsations de combustion,
deux échappements, bruit modulé, résonances et saturation douce. Il n'utilise
aucune boucle enregistrée et ne simule pas les pièces ou les gaz d'un moteur.
Le profil utilise une décharge de pression dont la durée suit le régime,
avec un front dépendant de l'effort et une faible turbulence d'écoulement.
L'excitation n'injecte plus de sinus amorti accordé. Les cylindres ont de petites
différences et variations lentes. Le banc ajoute une
régulation de ralenti amortie et perturbée, qui fait légèrement varier le régime
affiché et fourni au générateur sous 1 800 tr/min. La texture à zéro désactive
ces variations, tout en conservant le grain intrinsèque de l'écoulement.
Ce modèle de banc ne remplace pas la physique moteur d'un jeu.
La réverbe est un traitement séparé. La qualité reste à apprécier à l'écoute.

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

Le dernier argument `dry` garde le scénario normal avec la réverbe à zéro.
`idle` maintient successivement 800, 1 000 et 1 500 tr/min pendant quatre secondes
chacun ; `idle-dry` fait le même essai sans réverbe et `regular` désactive aussi
les irrégularités de combustion et de régime, en gardant la turbulence.
Ces trois variantes permettent de concentrer l'écoute sur le
ronronnement et les changements de régime maintenu.

La variante `ignition` rend douze secondes avec départ éteint, deux démarrages
et deux arrêts. Elle permet d'écouter les dernières combustions et le silence
entre les essais.

`--measure` émet les temps de 1 000 blocs de synthèse de 480 frames après
échauffement. Il exclut transfert PCM, interface et périphérique ; ce n'est pas
une mesure de latence ni une qualification globale pour le jeu.

`--smoke` ouvre un scénario automatique de cinq secondes, clairement indiqué
dans la fenêtre, puis ferme. Il vérifie l'exécution native et l'alimentation,
avec démarrage, accélération et arrêt, sans remplacer un essai réel du contact,
d'Espace et des curseurs.

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
