# Écouter le prototype YZ250 entièrement procédural

Depuis la racine `SilexProject/` :

```sh
silex run Silex-Examples/Sources/YZ250Procedural/Main.sx
```

La fenêtre porte le titre **YZ250 · procédural intégral · P1**. Elle est distincte
du précédent banc A/B/C à grains enregistrés et de l’atelier de véhicules.
Elle démarre silencieusement. Aucun changement n’est apporté au Chevrolet 454,
à la 500 4T, ni au package GFX.Audio.

## Valider les paliers avant les montées

1. Cliquer sur **4 500 tr/min**, **7 000 tr/min**, puis **9 500 tr/min**. Chaque
   palier continue jusqu’à une autre commande. Écouter la cadence, la matière,
   le niveau et les éventuelles oscillations pendant au moins dix secondes.
2. À un régime fixe, comparer les deux extrêmes de **Charge acoustique**.
   L’énergie et la texture changent ; la cadence reste identique.
3. Essayer **Montée lente · 5 s**, puis **Montée rapide · 1 s**. Chaque bouton
   repart de 3 660 tr/min et monte automatiquement jusqu’à 10 500 tr/min.
   Le plein régime est ensuite maintenu sans limite de durée.
4. **Arrêt** coupe le son avec un fondu court. Le curseur de régime revient au
   mode de régime imposé ; **Écouter ce régime** lance le palier affiché.

Ce sont des balayages de banc pour comparer le même générateur à différentes
vitesses. Le curseur de régime impose une vitesse ; ce n’est pas un accélérateur.
Le prototype n’a pas encore de modèle de couple, d’inertie ou de transmission.
Le contrôle de charge ne freine donc pas les montées chronométrées.

## Ce qui est synthétisé

Le moteur acoustique produit une explosion par tour pour un monocylindre 2T.
Une phase continue, calculée sur l’horloge audio à 44 100 Hz, commande
64 harmoniques. Six bandes de bruit filtré représentent la matière non périodique
de l’enregistrement : souffle, échappement et texture mécanique combinés.
Le bruit est modulé à la cadence des explosions ; leur intensité varie légèrement
d’un tour à l’autre sans modifier leur date. Le régime et les gains évoluent
continûment, sans changement de banque, raccord de grains ou boucle.

Le signal est monophonique, envoyé à l’identique aux deux canaux. Il n’ajoute
ni spatialisation ni réverbération. Le gain de réserve fixe vaut 0,55 ; aucun
compresseur, écrêtage ou normalisation automatique ne stabilise artificiellement
le niveau. Le volume d’écoute est indépendant.

`Calibration.sx` contient seulement des paramètres numériques de spectre,
de filtres et d’enveloppe. Le programme ne charge ni PCM, ni WAV, ni MP3 et
n’embarque aucun cycle enregistré. Les phases des harmoniques proviennent d’une
construction à phase minimale à partir du spectre moyen, pas des phases du fichier.
C’est une synthèse acoustique paramétrique, sans simulation thermodynamique.

## Ce que fournit réellement le fichier de référence

Le calibrage exploite **2023 YZ250 + FMF Full Exhaust PURE SOUND.mp3**, fourni
dans les archives. Il mesure 109 fenêtres suivant chacune six cycles estimés.
Cette analyse en ordre moteur suit les accélérations à l’intérieur des fenêtres,
au lieu de considérer chaque extrait comme un son à hauteur constante.
Elle mesure des énergies harmoniques et résiduelles, puis les agrège sur six
régimes et deux textures de charge. Les filtres de bruit sont normalisés hors
ligne par leur énergie impulsionnelle.

`Calibration.json` conserve les empreintes de l’original, de son PCM décodé,
du chemin de hauteur analysé et des paramètres générés. Le décodage original
reste exclusivement une entrée de l’outil de calibrage hors ligne.

La source n’a ni compte-tours ni mesure de couple. La plage **3 660–10 500 tr/min**
est une estimation acoustique héritée du suivi de hauteur ; ses erreurs possibles
d’octave ne sont pas levées. La charge interpole principalement les textures de
retombée et de montée en régime. Le bas de plage est peu couvert et le ralenti
n’est pas calibré. Le microphone et l’échappement FMF influencent les paramètres.
Leur mesure ne prouve pas que ce générateur reproduit fidèlement le moteur :
la validation du timbre reste une écoute humaine avant toute généralisation.

## Exporter et vérifier

```sh
silex compile Silex-Examples/Sources/YZ250Procedural/Main.sx --debug -o Build/YZ250-Procedural
Build/YZ250-Procedural --check
Build/YZ250-Procedural --render Build/YZ250-P1
python3 Silex-Examples/Sources/YZ250Procedural/Verify.py Build/YZ250-P1
```

Les sept WAV PCM16 stéréo utilisent le même gain de volume 0,7 :

| Suffixe | Écoute |
| --- | --- |
| `Fixed-4500`, `Fixed-7000`, `Fixed-9500` | 8 s à régime fixe, charge 0,7 |
| `Load-Low`, `Load-High` | 8 s à 7 000 tr/min, charge 0 puis 1 |
| `Ramp-Slow`, `Ramp-Fast` | 1 s au départ, montée de 5 ou 1 s, puis plein régime jusqu’à 12 s |

Un fondu termine les fichiers ; les paliers de l’interface n’ont pas de fin
programmée. Chaque WAV est accompagné d’un CSV de régime et de phase.

`--check` vérifie 21 points régime/charge, l’horloge des explosions, l’absence de
saturation et de valeurs non finies, la charge indépendante de la cadence,
la montée et le maintien, l’indépendance vis-à-vis des blocs de rendu, le reset,
l’arrêt et les commandes invalides. Il teste aussi les boutons par le runtime UI
sans périphérique audio et trois largeurs de disposition.

`Verify.py` analyse les WAV eux-mêmes : pics de plusieurs harmoniques sur les
paliers, variation du niveau sur 200 ms, montée suivie en ordre moteur et hauteur
du maintien final. Il vérifie aussi l’absence de dépendance aux samples dans
les sources du générateur. Le rapport `*-Verification.json` contient les mesures.
Ces vérifications ne décident pas du réalisme.

Pour reproduire le calibrage avec le WAV PCM16 stéréo 44,1 kHz décodé sans gain :

```sh
python3 Silex-Examples/Sources/YZ250Procedural/Calibrate.py \
  Build/YZ250-Source.wav \
  Silex-Examples/Sources/YZ250/Assets/Analysis.json \
  '.archives/EngineSounds/2023 YZ250 + FMF Full Exhaust PURE SOUND.mp3' \
  Silex-Examples/Sources/YZ250Procedural
```

L’outil vérifie les empreintes avant l’analyse et écrit exclusivement dans son
répertoire de sortie. Les archives restent inchangées. Python utilise uniquement
sa bibliothèque standard et n’est pas requis pour jouer le prototype compilé.
