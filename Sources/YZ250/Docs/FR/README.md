# Piloter la YZ250 avec une petite banque de sons

Depuis la racine `SilexProject/` :

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

La fenêtre **YZ250 · banque compacte · H2 · ESPACE = gaz** utilise la matière
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
YZ250 + FMF Full Exhaust PURE SOUND.mp3**. Chaque segment stocke **32 tours** avec leurs explosions, leur bruit et leur
texture mécanique. Le plancher utilise seize tours plus réguliers, répétés deux
fois. Les trois étages chargés supérieurs assemblent deux passages de seize
tours pris pendant des montées franches. Elles ne sont pas
réduites à un cycle ou reconstruites à partir de quelques harmoniques.

La préparation hors ligne corrige la hauteur à l’intérieur de chaque extrait.
Elle suit la phase de la fondamentale autour du chemin de hauteur estimé,
écarte l’intervalle où cette phase devient ambiguë, puis rééchantillonne le PCM
selon les tours du moteur. Quatre tours supplémentaires servent au raccord de
boucle. Un filtrage limite les fréquences susceptibles de se replier lors de la
transposition aux régimes voisins.

H2 conserve à l’identique huit segments de H1, notamment les trois extraits
chargés du bas/milieu qui donnent le micro coup de gaz accepté. La courbe de
réponse aux gaz reste inchangée. La préparation sélectionne séparément un
plancher plus régulier et des passages hauts de texture montante, en privilégiant
la même accélération de référence que les extraits acceptés.

La banque couvre six régimes estimés et deux textures : retombée et montée en
régime. Les boucles voisines sont mélangées progressivement sur une phase moteur
commune. Leur position reste continue même quand leur volume est nul. Cela
supprime la sélection répétée d’extraits et les changements de hauteur internes
qui rendaient le précédent mode C instable.

Entre les étages supérieurs, le mélange compense la perte d’énergie provoquée
par la superposition de boucles peu corrélées. `BlendEnergy.sx` contient leur
covariance stéréo mesurée hors ligne. Le gain dépend des poids de mélange,
jamais du niveau audio instantané : ce n’est pas un compresseur. Le groupe
bas/milieu conserve son mélange H1 pour préserver l’attaque acceptée.

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
ils ne sont plus embarqués ni lus par la démo H2.

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
silex compile Silex-Examples/Sources/YZ250/Main.sx --debug -o Build/YZ250-H2
Build/YZ250-H2 --check
Build/YZ250-H2 --render Build/YZ250-H2
python3 Silex-Examples/Sources/YZ250/VerifyCompact.py Build/YZ250-H2
```

Les neuf WAV stéréo PCM16 utilisent un gain commun de 0,7 :

| Suffixe | Contenu |
| --- | --- |
| `Fixed-4500`, `Fixed-7000`, `Fixed-9500` | 8 s à régime fixe, texture de charge 0,7 |
| `Load-Low`, `Load-High` | 8 s à 7 000 tr/min, charge 0 puis 1 |
| `Throttle` | 12 s : deux coups de gaz, montée et maintien à fond, retombée puis gaz partiels |
| `Idle` | 8 s au plancher enregistré, charge nulle |
| `Micro` | 4 s avec une ouverture des gaz de 80 ms |
| `Progressive` | 12 s : ouverture progressive des gaz sur 4 s, maintien puis relâchement |

Chaque export possède un CSV de régime, de phase, de charge acoustique et de gaz.
Les paliers de l’interface restent continus sans limite de durée.

Les contrôles couvrent 21 points régime/charge, la cadence, la sortie finie sans
saturation, le freinage par la charge sans plafond artificiel, le maintien et le
relâchement, l’indépendance des blocs, l’arrêt et les entrées invalides.
Ils mesurent aussi l’énergie réellement rendue aux étages supérieurs et à leurs
points intermédiaires : le creux d’environ 3 dB de H1 fait échouer ce contrôle.
Le mélange du groupe bas/milieu doit rester inchangé.
Ils suivent aussi le chemin événement clavier → accélérateur : appui Espace,
auto-répétition, relâchement, perte du focus, arrêt M et retour du banc. Le runtime
UI vérifie les boutons et trois largeurs sans ouvrir de périphérique audio.

`VerifyCompact.py` mesure la hauteur et les variations de niveau dans les WAV,
le plein régime et la retombée. Il protège par empreinte les trois extraits
acceptés de H1, vérifie la régularité du plancher, l’ouverture progressive,
le micro coup de gaz, la taille et les empreintes de la banque.
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

L’outil écrit `Compact.pcm` et `Compact.json` dans le répertoire de sortie,
et `BlendEnergy.sx` dans son répertoire parent. Pour une reconstruction de
contrôle, utiliser par exemple `Build/YZ250-H2-Rebuild/Assets`.

Python utilise seulement sa bibliothèque standard. Il n’est pas requis à la
lecture de la démo compilée. L’ancien `Prepare.py` prépare uniquement les assets
historiques du banc à grains ; il ne reconstruit pas la banque compacte.
