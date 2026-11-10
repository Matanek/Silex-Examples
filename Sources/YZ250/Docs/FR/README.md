# Piloter la YZ250 avec une petite banque de sons

Depuis la racine `SilexProject/` :

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

La fenêtre **YZ250 · ralenti / retombée · H5 · ESPACE = gaz** utilise environ
**1,25 Mio** de PCM16 stéréo. Le ralenti et la fermeture des gaz proviennent du
début proche de **2018_Yamaha_YZ_250x.mp3** ; les attaques et le palier G gardent
la référence YZ250/FMF précédente.
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
**Montée longue · ×4** est le réglage initial d’inertie : à la charge par défaut,
il faut environ quatre secondes de pleins gaz pour parcourir 95 % de la plage.
**Réponse vive · ×1** garde une réaction brève ; ×4 permet une montée prolongée.
Le curseur permet ×1 à ×10. L’inertie allonge uniquement l’accélération.
La retombée utilise une constante de 0,62 s : environ 1,86 s pour parcourir
95 % du retour au régime de base, après fermeture des gaz. Le statut affiche
**retombée / claquements** pendant cette texture distincte. Ce réglage ne simule pas une boîte de vitesses
et n’ajoute aucun changement de rapport automatique.

Le **régime de base** vaut **1 800** dans l’échelle de commande, réglable de
1 800 à 3 500. À 1 800, la nouvelle prise de ralenti conserve son tempo natif.
Cette valeur n’est pas une mesure de ses tr/min au compte-tours.
Les onze exports utilisent le réglage de base initial.

**G seul · palier** conserve uniquement la prise de l’essai G, au-dessus de
6 000 tr/min une fois le régime stabilisé. La charge y règle le niveau sonore,
sans mélange avec d’autres timbres. Elle continue de ralentir la montée en
mode accélérateur. **Prises initiales · comparer** désactive G et les nouvelles
textures de ralenti et de retombée. Le régime et la phase restent continus.

Le volume ne change pas la réponse du moteur.

## Ce qui conserve le caractère de la référence

La nouvelle prise de ralenti utilise **4,06–4,70 s** du fichier YZ250X : la fin
au ralenti identifiée dans les 4,7 premières secondes. Le démarrage autour de
1 s et la partie où la moto s’éloigne sont exclus. Le PCM garde son temps natif,
avec un raccord de boucle de 20 ms et un gain fixe. Trois bandes passantes
préparées hors ligne évitent le repliement pendant la transposition. Son lecteur
suit progressivement la commande de régime et s’efface sur les premiers
1 600 tr/min au-dessus de la base, pour rejoindre les attaques existantes.

La retombée utilise **3,64–4,00 s**, à la fermeture du dernier coup de gaz proche.
La préparation suit la seconde partielle pour corriger la hauteur interne,
sans recaler les formes d’explosion entre elles. La prise conserve 32 cycles
avec leurs claquements. Fermer les gaz sous charge déclenche ce chemin même
quand la texture de charge devient nulle ; il s’efface progressivement à
l’approche du ralenti et lors d’une réouverture. Le niveau n’est pas multiplié
par l’ouverture des gaz. Allonger seulement les tr/min tout en coupant le son
à la fermeture ne suffirait pas à reproduire une décélération.

Le programme lit douze courtes boucles issues du PCM réel du fichier **2023
YZ250 + FMF Full Exhaust PURE SOUND.mp3**. Chaque segment stocke **32 tours** avec leurs explosions, leur bruit et leur
texture mécanique. Le plancher utilise seize tours plus réguliers, répétés deux
fois. Les trois étages chargés supérieurs assemblent deux passages de seize
tours pris pendant des montées franches. Ces boucles ne sont pas
réduites à un cycle ou reconstruites à partir de quelques harmoniques.

La préparation hors ligne corrige la hauteur à l’intérieur de chaque extrait.
Elle suit la phase de la fondamentale autour du chemin de hauteur estimé,
écarte l’intervalle où cette phase devient ambiguë, puis rééchantillonne le PCM
selon les tours du moteur. Quatre tours supplémentaires servent au raccord de
boucle. Un filtrage limite les fréquences susceptibles de se replier lors de la
transposition aux régimes voisins.

Les trois extraits chargés du bas et du milieu restent conservés à l’identique.
La préparation sélectionne séparément un plancher plus régulier et des passages
hauts de texture montante, en privilégiant la même accélération de référence.

La banque couvre six régimes estimés et deux textures : retombée et montée en
régime. Les boucles voisines sont mélangées progressivement sur une phase moteur
commune. Leur position reste continue même quand leur volume est nul. Cette
phase commune évite les variations de hauteur internes qui rendaient le
précédent mode C instable.

Entre les étages supérieurs, le mélange compense la perte d’énergie provoquée
par la superposition de boucles peu corrélées. `BlendEnergy.sx` contient leur
covariance stéréo mesurée hors ligne. Le gain dépend des poids de mélange,
jamais du niveau audio instantané : ce n’est pas un compresseur. Le groupe
bas/milieu conserve son mélange H1 pour préserver l’attaque acceptée.

La banque initiale reste inchangée. Une prise supplémentaire applique le recalage
de l’essai G à la seule prise chargée à 6 000 tr/min. La corrélation des douze premiers
ordres détermine un décalage limité à un quart de tour par cycle ; des fenêtres
de deux tours superposées appliquent ce déplacement au PCM stéréo complet.
Cela conserve le bruit et les explosions enregistrés. Le recalage agit sur le
placement des explosions, indépendamment du niveau et du raccord de boucle.
Le mélange pilotable reste à valider à l’écoute.

Après 0,35 s de stabilité au-dessus de 6 000 tr/min, une transition progressive
introduit G seul. Les montées gardent les prises initiales ; les autres prises
ne sont pas superposées à G au palier. Les déplacements de phrases aléatoires
sont désactivés pour préserver le timbre isolé. Les 32 cycles conservent leurs
différences enregistrées, mais la boucle reste répétitive : ce point n’est pas
résolu par ce prototype. Au-delà de 7 200 tr/min, une vue filtrée de la même prise
est introduite progressivement, entièrement à 7 500, pour éviter le repliement
jusqu’à 10 500 tr/min. À 7 000 tr/min, G garde sa bande passante initiale.

`PeakBounds.sx` contient une enveloppe conservatrice des crêtes des mélanges initiaux.
La prise G utilise la crête maximale de ses deux bandes passantes.
G, les mélanges initiaux, le ralenti et la retombée sont bornés séparément
avant leurs transitions convexes.
Le gain respecte un plafond de 0,98 pour toutes les phases de lecture, y compris
les poids résiduels pendant les transitions. La protection
utilise les crêtes des données et les poids de mélange, pas le niveau instantané
du signal : les pics ne sont pas coupés par un écrêteur.

Un worker dédié alimente maintenant le flux audio, indépendamment du rendu de l’interface.
Le petit tampon de 2 048 frames, environ 46 ms, reste inchangé pour conserver
la réactivité des commandes. Les commandes partagées et les blocs de rendu sont
protégés par `mutex` ; l’attente du périphérique se fait hors de cette section.
L’arrêt de la fenêtre demande la fin du worker puis attend sa terminaison.

Le compteur **Réserve audio** indique les observations d’une file d’entrée vide.
Le mixer peut encore avoir du son déjà préparé : ce compteur ne prouve donc pas
une coupure audible. Le test de sortie réelle ci-dessous vérifie le PCM émis.
Le contrôle du régime et de la charge reste calculé sur l’horloge audio.
La réponse aux gaz est simplifiée, sans identification de couple ni d’inertie.
Une forte charge allonge la montée ; elle ne réduit pas la consigne de plein
régime. La texture suit l’ouverture des gaz et leur évolution. Le son reste
stéréo, sans normalisation automatique ni compresseur.

## Taille et limites

`Assets/Compact.pcm` contient douze segments de 64 Kio ; `Assets/Registered.pcm`
contient G seul et sa vue filtrée, deux segments de 64 Kio. `Assets/LowSpeed.pcm`
ajoute **393 652 octets** de ralenti et de retombée. Le total vaut
**1 311 156 octets**. Ce sont les seules données audio embarquées. Le chargement
les décode une fois en float32 : environ 2,50 Mio en mémoire. Les anciens assets
`Reference.pcm` et `Grains.bin` restent des données historiques de préparation ;
ils ne sont plus embarqués ni lus par la démo H5.

La référence FMF couvre des tr/min acoustiquement estimés à **3 660–10 500**.
La démo accepte **1 800–10 500** comme échelle indicative de commande. Le ralenti
YZ250X est réellement enregistré, mais ne possède pas de mesure au compte-tours :
sa conservation au tempo natif prime sur une hauteur déduite du numéro affiché.
Les textures de charge restent des indices de montée/retombée, sans mesure de
couple. Ces deux courts enregistrements ne
couvrent pas toutes les situations ; des répétitions et des différences de timbre
entre boucles restent à juger à l’écoute. La YZ250X 2018 et la YZ250/FMF 2023
ont des prises et échappements différents : leur raccord reste une limite du
prototype. Celui-ci attend une validation humaine
avant toute généralisation.

`Assets/Compact.json` donne les empreintes de l’original et du PCM, les fenêtres
retenues, l’intervalle de phase exploitable, les niveaux et la taille de la banque.
Les archives sont uniquement lues par la préparation.

## Vérifier et exporter

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --debug -o Build/YZ250-H5
Build/YZ250-H5 --check
Build/YZ250-H5 --render Build/YZ250-H5
python3 Silex-Examples/Sources/YZ250/VerifyCompact.py Build/YZ250-H5
```

Les onze WAV stéréo PCM16 utilisent un gain commun de 0,7 :

| Suffixe | Contenu |
| --- | --- |
| `Fixed-4500`, `Fixed-7000`, `Fixed-9500` | 8 s à régime fixe, texture de charge 0,7 |
| `Load-Low`, `Load-High` | 8 s à 7 000 tr/min, charge 0 puis 1 |
| `Throttle` | 12 s : deux coups de gaz, montée et maintien à fond, retombée puis gaz partiels |
| `Idle` | 8 s au régime de base de 1 800 tr/min, charge nulle |
| `Micro` | 4 s avec une ouverture des gaz de 80 ms |
| `Progressive` | 12 s : ouverture progressive des gaz sur 4 s, maintien puis relâchement |
| `Long` | 20 s : pleins gaz à inertie ×4, maintien puis relâchement |
| `Nearby` | 10 s à inertie ×4 : ralenti, petit coup de gaz, retour, montée puis retombée |

Les neuf premiers scénarios utilisent l’inertie ×1 ; `Long` et `Nearby`
utilisent le réglage ×4 proposé par défaut dans l’interface.

Chaque export possède un CSV de régime, de phase, de charge acoustique, de gaz
et de poids du chemin de retombée (`coast`).
Les paliers de l’interface restent continus sans limite de durée.

Pour juger le timbre, écouter un seul état à la fois : commencer par `Idle`,
puis la fermeture des gaz entre 7,15 et 8,00 s dans `Throttle`. `Nearby` sert
ensuite à juger les raccords ; il n’est pas une comparaison de timbres isolés.

Les contrôles couvrent 27 points régime/charge, la cadence, la sortie finie sans
saturation, le freinage par la charge sans plafond artificiel, le maintien et le
relâchement, l’indépendance des blocs, l’arrêt et les entrées invalides.
Ils mesurent aussi l’énergie réellement rendue aux étages supérieurs et à leurs
points intermédiaires : le creux d’environ 3 dB de H1 fait échouer ce contrôle.
Le mélange du groupe bas/milieu conserve son réglage. Le contrôle inclut le cas
7980 tr/min / pleine charge qui dépassait la limite audio, puis 6 000 blocs de
changements de régime, charge et inertie avec un plafond strict de 0,98.
Ils suivent aussi le chemin événement clavier → accélérateur : appui Espace,
auto-répétition, relâchement, perte du focus, arrêt M et retour du banc. Le runtime
UI vérifie les boutons et trois largeurs sans ouvrir de périphérique audio.

`VerifyCompact.py` mesure la hauteur et les variations de niveau dans les WAV,
le plein régime et la retombée. Il protège par empreinte les trois extraits
acceptés de H1, vérifie la régularité du plancher, l’ouverture progressive,
le micro coup de gaz, la taille et les empreintes de la banque et de l’enveloppe
de crête et du recalage. Il contrôle l’amélioration de la cohérence des formes
de pression dans la prise de l’essai G. À 7 000 tr/min, il compare directement
la forme d’onde rendue à G isolé, à trois charges, pour protéger son timbre.
Le ralenti rendu est aussi comparé au PCM natif. `--coast-check` vérifie qu’une
fermeture coupe les gaz sans supprimer la rotation ni les claquements, puis
que le moteur rejoint le ralenti et réagit à une réouverture. Il teste aussi
l’indépendance aux découpages de buffers pendant toute la retombée.
Le résultat est écrit dans `*-Verification.json`. Ces mesures ne remplacent pas
la validation du caractère sonore. `--check` reproduit aussi, avec un mixer
hors ligne, l’assèchement de l’ancienne alimentation par l’interface : un blocage
de 120 ms dépasse son avance de 46 ms.

Pour vérifier la sortie audio réelle avec l’interface, sans capture d’écran :

```sh
Build/YZ250-H5 --live-check Build/YZ250-H5-Live
python3 Silex-Examples/Sources/YZ250/VerifyLive.py Build/YZ250-H5-Live
```

Ce test automatique dure huit secondes et bloque volontairement le thread de
l’interface six fois pendant 120 ms. Il enregistre la sortie du mixer dans
`*.f32le` avec son format dans `*.json`. Il exige zéro perte de capture et
rapporte les observations de file vide. `VerifyLive.py` contrôle aussi le PCM
réellement capturé,
sans intervalle silencieux de 5 ms ni effondrement du niveau sur 10 ms hors du
démarrage et de l’arrêt. Il produit `*-Verification.json`.
Ce contrôle exige un périphérique audio et exerce le worker, les commandes et
sa terminaison ; les tests `--check` restent utilisables sans périphérique.

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
contrôle, utiliser par exemple `Build/YZ250-H5-Rebuild/Assets`.

Après une nouvelle préparation de la banque, régénérer son enveloppe et les
cycles recalés :

```sh
python3 Silex-Examples/Sources/YZ250/PrepareBounds.py \
  Silex-Examples/Sources/YZ250/Assets/Compact.pcm \
  Silex-Examples/Sources/YZ250
python3 Silex-Examples/Sources/YZ250/PrepareRegistered.py \
  Silex-Examples/Sources/YZ250/Assets/Compact.pcm \
  Silex-Examples/Sources/YZ250
```

`PeakBounds.json` lie les paramètres au PCM par empreinte. Les données de crête
ajoutent environ 17 Kio de nombres au programme. `Assets/Registered.json`
conserve l’empreinte des deux banques, les paramètres et les décalages par cycle ;
`RegisteredData.sx` contient puissance et crête du PCM recalé.

Après décodage de la nouvelle référence en WAV PCM16 stéréo 44,1 kHz :

```sh
python3 Silex-Examples/Sources/YZ250/PrepareLowSpeed.py \
  Build/YZ250X-Source.wav \
  .archives/EngineSounds/2018_Yamaha_YZ_250x.mp3 \
  Silex-Examples/Sources/YZ250
```

`Assets/LowSpeed.json` conserve les empreintes, fenêtres proches, niveaux et
chemin de hauteur ; `LowSpeedData.sx` contient les bornes de lecture et de crête.
Python utilise seulement sa bibliothèque standard. Il n’est pas requis à la
lecture de la démo compilée. L’ancien `Prepare.py` prépare uniquement les assets
historiques du banc à grains ; il ne reconstruit pas la banque compacte.
