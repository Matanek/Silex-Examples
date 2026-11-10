# Piloter la YZ250 avec une petite banque de sons

Depuis la racine `SilexProject/` :

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

La fenêtre **YZ250 · banque compacte · H1 · ESPACE = gaz** utilise la matière
réelle de l’enregistrement fourni, avec une banque PCM16 stéréo de **768 Kio**.
Elle remplace le précédent banc à grains A/B/C à cette entrée. Le prototype
spectral P1 reste séparé et ne constitue plus la version proposée à l’écoute.
Le Chevrolet 454, la 500 4T et GFX.Audio sont inchangés.

## Donner des coups de gaz

- Maintenir **Espace** démarre le moteur si nécessaire et ouvre les gaz.
- Relâcher **Espace** revient à la position du curseur de gaz, zéro par défaut.
  Le régime retombe automatiquement.
- **Accélérateur** démarre le mode de conduite au curseur. La charge ralentit
  la montée mais ne bloque pas le plein régime lorsque les gaz sont ouverts.
- **Banc à régime fixe** impose le régime du curseur. Espace repasse en
  accélérateur pour tester immédiatement une réaction aux gaz.
- **M** ou **Lecture / arrêt** arrête ou reprend. Une répétition d’Espace après
  un arrêt ne redémarre pas le moteur : relâcher puis appuyer à nouveau.

La perte du focus relâche Espace. La position de gaz au curseur reste conservée.
Le statut affiche le mode, les gaz effectifs et le régime. Commencer par des
coups de gaz courts, maintenir ensuite les gaz plusieurs secondes, puis écouter
la retombée. Comparer différentes charges et vérifier le son à régime fixe.
Le volume ne change pas la réponse du moteur.

## Ce qui conserve le caractère de la référence

Le programme lit douze courtes boucles issues du PCM réel du fichier **2023
YZ250 + FMF Full Exhaust PURE SOUND.mp3**. Chaque boucle conserve **32 tours**
avec leurs explosions, leur bruit et leur texture mécanique. Elles ne sont pas
réduites à un cycle ou reconstruites à partir de quelques harmoniques.

La préparation hors ligne corrige la hauteur à l’intérieur de chaque extrait.
Elle suit la phase de la fondamentale autour du chemin de hauteur estimé,
écarte l’intervalle où cette phase devient ambiguë, puis rééchantillonne le PCM
selon les tours du moteur. Quatre tours supplémentaires servent au raccord de
boucle. Un filtrage limite les fréquences susceptibles de se replier lors de la
transposition aux régimes voisins.

La banque couvre six régimes estimés et deux textures : retombée et montée en
régime. Les boucles voisines sont mélangées progressivement sur une phase moteur
commune. Leur position reste continue même quand leur volume est nul. Cela
supprime la sélection répétée d’extraits et les changements de hauteur internes
qui rendaient le précédent mode C instable.

Le contrôle du régime et de la charge reste calculé sur l’horloge audio.
La réponse aux gaz est simplifiée, sans identification de couple ni d’inertie.
Une forte charge allonge la montée ; elle ne réduit pas la consigne de plein
régime. La texture suit l’ouverture des gaz et leur évolution. Le son reste
stéréo, sans normalisation automatique ni compresseur.

## Taille et limites

`Assets/Compact.pcm` contient douze segments de 64 Kio, **786 432 octets au total**.
Cette banque est la seule donnée audio embarquée par `Bank.sx`. Le chargement la
décode une fois en float32 : environ 1,5 Mio en mémoire. Les anciens assets
`Reference.pcm` et `Grains.bin` restent des données historiques de préparation ;
ils ne sont plus embarqués ni lus par la démo H1.

Les tr/min restent des estimations acoustiques **3 660–10 500** sans compte-tours.
Le ralenti n’est pas enregistré. Les deux textures de charge sont des indices
de montée/retombée, pas des mesures de couple. Une source de treize secondes ne
couvre pas toutes les situations ; des répétitions et des différences de timbre
entre boucles restent à juger à l’écoute. Le microphone et l’échappement FMF
font partie de la référence. Ce prototype hybride attend une validation humaine
avant toute généralisation.

`Assets/Compact.json` donne les empreintes de l’original et du PCM, les fenêtres
retenues, l’intervalle de phase exploitable, les niveaux et la taille de la banque.
Les archives sont uniquement lues par la préparation.

## Vérifier et exporter

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --debug -o Build/YZ250-H1
Build/YZ250-H1 --check
Build/YZ250-H1 --render Build/YZ250-H1
python3 Silex-Examples/Sources/YZ250/VerifyCompact.py Build/YZ250-H1
```

Les six WAV stéréo PCM16 utilisent un gain commun de 0,7 :

| Suffixe | Contenu |
| --- | --- |
| `Fixed-4500`, `Fixed-7000`, `Fixed-9500` | 8 s à régime fixe, texture de charge 0,7 |
| `Load-Low`, `Load-High` | 8 s à 7 000 tr/min, charge 0 puis 1 |
| `Throttle` | 12 s : deux coups de gaz, montée et maintien à fond, retombée puis gaz partiels |

Chaque export possède un CSV de régime, de phase, de charge acoustique et de gaz.
Les paliers de l’interface restent continus sans limite de durée.

Les contrôles couvrent 21 points régime/charge, la cadence, la sortie finie sans
saturation, le freinage par la charge sans plafond artificiel, le maintien et le
relâchement, l’indépendance des blocs, l’arrêt et les entrées invalides.
Ils suivent aussi le chemin événement clavier → accélérateur : appui Espace,
auto-répétition, relâchement, perte du focus, arrêt M et retour du banc. Le runtime
UI vérifie les boutons et trois largeurs sans ouvrir de périphérique audio.

`VerifyCompact.py` mesure la hauteur et les variations de niveau dans les WAV,
le plein régime et la retombée ; il vérifie la taille et l’empreinte de la banque.
Le résultat est écrit dans `*-Verification.json`. Ces mesures ne remplacent pas
la validation du caractère sonore.

Pour reproduire la banque depuis le décodage original sans gain, PCM16 stéréo
44,1 kHz :

```sh
python3 Silex-Examples/Sources/YZ250/PrepareCompact.py \
  Build/YZ250-Source.wav \
  Silex-Examples/Sources/YZ250/Assets/Analysis.json \
  '.archives/EngineSounds/2023 YZ250 + FMF Full Exhaust PURE SOUND.mp3' \
  Silex-Examples/Sources/YZ250/Assets
```

Python utilise seulement sa bibliothèque standard. Il n’est pas requis à la
lecture de la démo compilée. L’ancien `Prepare.py` prépare uniquement les assets
historiques du banc à grains ; il ne reconstruit pas la banque compacte.
