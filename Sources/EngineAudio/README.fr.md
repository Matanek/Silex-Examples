# Essayer les moteurs et les boîtes

[English](README.md)

## Banc multi-profils engine-sim

Le mode `--reference` pilote le noyau du projet
[engine-sim](https://github.com/ange-yaghi/engine-sim) d'Ange Yaghi, avec son profil
Chevrolet 454 V8 destiné au premier épisode. Démarreur, combustion, écoulements,
inertie et synthèse sont calculés par cette référence. Le compte-tours lit son
régime réel. Ce banc de qualification macOS ARM64 fonctionne dans un processus
séparé ; il ne remplace pas encore le générateur réutilisable de GFX.Audio et
n'établit pas sa qualification en jeu.

Préparer d'abord le [témoin natif](../../Tools/EngineReference/README.fr.md), puis
compiler depuis la racine du workspace ou du groupe de Spec :

```sh
silex compile Silex-Examples/Sources/EngineAudio/Main.sx --release -o Build/EngineAudio-Reference
Build/EngineAudio-Reference --reference
```

**M** ou le bouton démarre et coupe l'allumage. Attendre que le démarreur entraîne
le moteur, puis maintenir **Espace** pour accélérer ; relâcher pour décélérer.
La fenêtre commence moteur éteint et relâche les gaz lorsqu'elle perd le focus.
La coupure laisse finir les combustions et ralentir la mécanique.

Choisir le profil avec la liste déroulante. Couper le contact et attendre
l’arrêt du moteur et du véhicule avant un changement. Le chargement est indiqué
au compte-tours ; la fenêtre continue de traiter les événements et la lecture
commence après une réserve audio. Le flux précédent est libéré à chaque changement.

| Profil | Caractère / cycle |
|---|---|
| Monster / Chevrolet 454 | V8 7,4 L accepté, quatre temps |
| Berline / BMW M52B28 | Six cylindres en ligne, quatre temps |
| Sportive / Ferrari F136 | V8, quatre temps |
| Moto routière / Harley | V2 de cruiser, quatre temps |
| Moto sportive / Hayabusa | Quatre cylindres en ligne, quatre temps |
| Camion essence / 454 stock | V8, quatre temps ; pas un diesel |
| Moto cross 450 | Mono générique, quatre temps |
| Moto cross 250 | Mono générique, deux temps ; prototype à lumières |

Les six premiers moteurs reprennent les configurations mécaniques du dépôt
original. Les deux cross sont des adaptations locales du mono Honda TRX520,
avec géométrie, inertie, distribution et régime propres. Les réponses
d’échappement sont choisies parmi celles disponibles au commit verrouillé ;
ces profils ne certifient pas le son ou les performances d’un véhicule commercial.
Le deux temps allume à chaque tour et utilise des lumières de transfert et
d’échappement. Le balayage vient d’un réservoir à pression prescrite qui
simplifie le carter-pompe : sa qualité reste à apprécier à l’écoute.

**Banc libre** conserve l’écoute au point mort et sa charge réglable. Les
boutons Libre, 1 000 et 1 500 permettent les comparaisons de régime. La charge
des nouveaux profils suit leur cylindrée ; le 454 initial conserve son rendu.
**Route** ajoute un véhicule longitudinal et sa transmission. Choisir ce mode
avant de démarrer. L’accélération change le régime, l’effort moteur et la vitesse.
Le compte-tours affiche AUTO ou MANUEL, le rapport (N au point mort) et les km/h.
Les rapports et masses sont des réglages de démonstration.

- **A** : alterner boîte automatique et manuelle.
- **↑ / ↓** ou les boutons + / − : passer un rapport et entrer en manuel.
- **N** : point mort, en manuel.
- **S maintenu** : frein de roue ; relâcher Espace produit aussi du frein moteur.
- **M** : contact ; le moteur garde son inertie à la coupure.

La boîte débraye, coupe brièvement les gaz et reprend progressivement l’effort.
Le départ utilise un embrayage automatique, y compris en commande manuelle des
rapports. Le deux temps démarre dans sa plage de puissance avec du patinage.
Un rétrogradage qui dépasserait le régime limite est refusé et signalé ; une
commande refusée n’est pas différée jusqu’à une vitesse plus basse. Les seuils
auto et leur temporisation évitent les passages répétés autour d’un même régime.
La perte de focus relâche gaz et frein. Il n’y a pas de marche arrière.

Les réglages initiaux conservent la texture et le filtrage du profil original,
sans réverbe ajoutée. « Texture » règle son bruit d’écoulement et sa variation
temporelle ; à zéro, les irrégularités physiques des combustions restent présentes.
« Échappement » mélange le signal brut et la réponse impulsionnelle choisie.
Volume et réverbe courte sont séparés. La charge supplémentaire et les régimes
maintenus s’appliquent au Banc ; en Route, le véhicule produit la charge.
Le panneau de réglages défile si nécessaire. Texte et fond du sélecteur et de
sa liste ouverte ont des couleurs explicites pour conserver le contraste.

```sh
Build/EngineAudio-Reference --fleet-check
Build/EngineAudio-Reference --reference-check
Build/EngineAudio-Reference --reference-render Build/EngineReference/Bridge.wav
Build/EngineAudio-Reference --reference --smoke
```

Le contrôle sans fenêtre vérifie départ silencieux, démarreur progressif,
ralenti, texture à zéro, accélération, inertie d'arrêt, silence final et
redémarrage. Le rendu WAV conserve la texture initiale et écrit le scénario
principal, 576 000 frames stéréo à 44,1 kHz (environ 13,06 s). Le smoke au Banc
dure neuf secondes ; en Route, 35 secondes avec départ, rapports et freinage. Le test d'écoute et d'interaction native reste nécessaire.
Les réglages exacts de chaque passage de la vidéo ne sont pas établis ; ce mode
est un rendu du profil original, pas une reproduction certifiée de son montage.

On peut sélectionner un profil et un mode au lancement :

```sh
Build/EngineAudio-Reference --preset cross2 --road
Build/EngineAudio-Reference --preset moto --manual
Build/EngineAudio-Reference --preset cross4 --road --smoke
```

Clés : `454`, `berline`, `sport`, `cruiser`, `moto`, `truck`, `cross4`, `cross2`.
`--fleet-check` vérifie les huit démarrages/arrêts, les transitions de profil,
la boîte, le point mort et le freinage, puis compare le PCM et la télémétrie
Route synchrones et asynchrones avec quatre requêtes en vol.

## Corps de l’explosion du cross 4T

Le profil 4T amortit les résonances médium et aigu de la réponse d’échappement,
avec des constantes de 24 et 14 ms, tout en conservant la queue grave. Cela
vise un impact plus rond et mat, suivant le repère d’un kick de batterie donné
à l’écoute. Le régime et le calcul mécanique restent ceux du moteur simulé.
Le rendu `dry` ci-dessous retire le souffle pour juger le corps seul ; le
curseur Souffle permet ensuite d’écouter les deux couches ensemble.

## Souffle du cross quatre temps

Le profil cross 450 4T active un fond d’admission/échappement à 60 %. Le curseur
**Souffle** dose cette couche indépendamment de Texture et de Réverbe. À zéro,
on retrouve le signal de pression précédent. Le souffle augmente sous
accélération, suit le régime et finit en silence à l’arrêt, avec un lissage de
90 ms. Les autres profils le démarrent à zéro ; Réglages initiaux et changement
de profil restaurent la valeur du catalogue.

Cette couche utilise un bruit reproductible coloré par GFX.Audio, mélangé
avant le volume et la réverbe, avec une marge pour les crêtes de combustion.
Elle complète le timbre du banc ; l’origine exacte du fond de l’enregistrement
(admission, échappement, ambiance ou micro) reste à apprécier à l’écoute.

```sh
Build/EngineAudio-Reference --airflow-check
Build/EngineAudio-Reference --airflow-render Build/EngineReference/Cross4-Breath.wav
Build/EngineAudio-Reference --airflow-render Build/EngineReference/Cross4-Dry.wav dry
```

Les rendus conservent sept secondes de ralenti après le démarrage. Le contrôle
vérifie continuité entre blocs, bypass, bornes, niveau sous accélération,
silence à l’arrêt et lecture asynchrone 4T identique au rendu synchrone.

## Raccourci et fluidité du témoin

La touche **M** suit son symbole logique sur AZERTY, QWERTY et les autres
positions de clavier ; les majuscules fonctionnent, l'auto-répétition ne bascule
pas le contact. Les combinaisons système/Contrôle/Alt sont laissées disponibles.
L'aiguille a un amortissement visuel de 25 ms, indépendant du régime et du son.
La valeur numérique conserve le régime mesuré.

En mode référence interactif, la fenêtre consomme les blocs prêts sans attendre
le helper. Cinq blocs de 480 frames tiennent dans le flux audio ; jusqu'à quatre
requêtes FIFO restent en vol, pour que le moteur continue entre deux trames.
Les écritures partielles gardent leur bloc et leur position. Cette réserve
représente au plus environ 98 ms de PCM écrit/préparé/commandé, auxquels
s'ajoutent le quantum du helper et le périphérique. Le rendu hors ligne garde
son chemin synchrone pour la comparaison déterministe.

```sh
Build/EngineAudio-Reference --reference-async-check
Build/EngineAudio-Reference --reference --smoke --frame-profile
```

Le premier contrôle compare 576 000 frames à commandes identiques, y compris
changements de contact, texture et réverbe, avec quatre requêtes en file. PCM
et télémétrie doivent rester identiques, sans bloc dupliqué. Le second affiche
les intervalles d'updates et les temps d'alimentation/construction du dessin,
après 0,5 seconde de chauffe. Ces mesures ne sont pas actives dans l'essai normal.
Elles ne constituent pas une mesure directe des présentations de l'écran.

## Prototype procédural précédent

Le lancement sans `--reference` garde le prototype décrit ci-dessous, pour
comparaison et pour ses contrôles de non-régression. Son caractère sonore n'a
pas été accepté.

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
