# Valider la YZ250 à l’écoute

Ce prototype isolé utilise le fichier fourni **2023 YZ250 + FMF Full Exhaust
PURE SOUND**. Il conserve les 13,19 secondes de PCM stéréo et permet de tenir
un régime estimé tout en faisant varier une charge acoustique. Il n’ajoute
aucun moteur au catalogue et ne modifie ni le Chevrolet 454 ni la cross 500 4T.

Depuis la racine `SilexProject/` :

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

## Comparer les trois écoutes

- **A · Référence** : écouter le fichier décodé à sa vitesse d’origine.
- **B · Reconstruction** : écouter le même parcours à travers le recouvrement
  des grains, toujours à vitesse d’origine. Cette comparaison vérifie que le
  traitement conserve la matière avant de juger le pilotage.
- **C · Moteur piloté** : donner des gaz avec l’accélérateur ; le régime monte
  automatiquement, puis redescend au relâchement.

En C, **Accélérateur** est le mode par défaut. Maintenir **Espace** donne les
pleins gaz ; le relâcher revient à la position du curseur. La charge freine la
montée et réduit le régime atteint. Les gaz et la charge déterminent aussi le
choix des passages enregistrés ; le relâchement privilégie les portions de
descente en régime. Une perte de focus relâche Espace.

**Banc à régime imposé** retrouve le premier comportement : choisir directement
le régime, puis modifier uniquement la charge acoustique pour comparer le timbre.

Chaque bouton lance l’écoute correspondante. **M** ou « Lecture / arrêt »
bascule la lecture ; une reprise redémarre le parcours. Les commandes de gaz,
de banc et de charge agissent sur C ; le volume est commun aux trois écoutes. A et B
s’arrêtent à la fin du fichier, tandis que C peut être tenu indéfiniment.

Commencer par A puis B : la mécanique, les coups de gaz, les irrégularités et
la stéréo doivent rester reconnaissables. Passer ensuite en C, choisir un
régime en donnant puis relâchant les gaz. Comparer une montée à faible charge
avec une montée à forte charge. Utiliser le banc pour tenir un régime et
déplacer seulement la charge. Juger les attaques, la matière mécanique, les
raccords, les éventuels effets de boucle et la réponse aux commandes. Le test
automatisé ne décide pas si le résultat est réaliste.

## Ce que les commandes représentent

La plage estimée de l’analyse est **3 660..10 500 tr/min**, sous l’hypothèse
d’un monocylindre deux temps. Aucun compte-tours n’accompagne l’enregistrement :
le calibrage absolu et les éventuelles ambiguïtés harmoniques restent à vérifier.
Le prototype n’invente pas de ralenti en dessous de la plage analysée.

Le mode accélérateur ajoute une réponse de régime simplifiée pour l’écoute,
sans courbe de couple ni inertie mesurées. Gaz relâchés, il revient au plancher
enregistré ; le bouton d’arrêt coupe la lecture. Cette réponse est intégrée sur
l’horloge audio et ne dépend pas de la fréquence des images de l’interface.

Sur le banc, la charge 0..1 choisit principalement entre les portions dont le
régime baisse et celles dont il monte. En mode accélérateur, ce choix dépend
aussi des gaz et de l’évolution du régime. Ce n’est pas une mesure de couple ni une simulation
thermodynamique. Un fichier unique ne fournit pas une grille complète de tous
les régimes sous toutes les charges. La prise de son et l’échappement FMF font
partie du timbre capturé ; il n’existe pas encore de rendu d’habitacle ou de
caméra indépendante.

Le rendu C recouvre quatre fenêtres stéréo de 120 ms, renouvelées toutes les
30 ms. Il choisit les passages proches du régime et de la charge demandés,
recherche un alignement par corrélation et limite la transposition à 0,75..1,33.
Il conserve les échantillons complets, sans normalisation par grain ni réduction
à une forme d’onde périodique. Le prototype reste local à l’exemple tant que
l’écoute n’est pas validée ; aucune API publique supplémentaire n’est créée.

## Exporter et vérifier

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --debug -o Build/YZ250-Prototype
Build/YZ250-Prototype --check
Build/YZ250-Prototype --render Build/YZ250
```

L’export crée `YZ250-Reference.wav`, `YZ250-Reconstruction.wav` et
`YZ250-Controlled.wav`, à 44 100 Hz stéréo PCM16 et au même gain de 0,7.
Le troisième fichier dure 12 s : deux coups de gaz, le premier à faible charge,
le second à forte charge, chacun suivi d’un relâchement. Un bref fondu ferme
les exports.

`--check` compare A et B sur le fichier entier, vérifie la sélection de matière
par la charge à régime constant, les sorties finies, l’arrêt, les commandes
invalides, l’indépendance vis-à-vis des tailles de blocs et les boutons/layouts
sans périphérique audio. Il vérifie aussi la montée automatique aux gaz, l’effet
de la charge, le retour au plancher après relâchement et le passage au banc.

`Assets/Analysis.json` conserve le hash du MP3 d’origine, le hash du PCM, les
estimations et leurs limites. Le prototype lit uniquement ses assets embarqués.
Le MP3 archivé demeure inchangé. Pour refaire la préparation avec le WAV stéréo
PCM16 44,1 kHz décodé et le MP3 d’origine :

```sh
python3 Silex-Examples/Sources/YZ250/Prepare.py Build/YZ250-Source.wav \
  '.archives/EngineSounds/2023 YZ250 + FMF Full Exhaust PURE SOUND.mp3' \
  Silex-Examples/Sources/YZ250/Assets
```
