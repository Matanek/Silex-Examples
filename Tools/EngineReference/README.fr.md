# Témoin sonore engine-sim

[English](README.md)

Cet outil de développement fait tourner plusieurs profils engine-sim hors de son
interface Windows. Il sert de témoin au banc d'écoute Silex. Le calcul thermique
complet reste extérieur à GFX.Audio. Une version allégée destinée au jeu devra
être confrontée à ce témoin avant de revendiquer le même caractère sonore.

## Construire sur macOS ARM64

Prérequis : Xcode avec Clang/Flex, CMake, Python 3.12+ et Bison 3.2+.
Bison peut être compilé dans un dossier local ; aucune installation globale
n'est requise par l'outil. La génération d'un lecteur Piranha demande sa version
récente, celle livrée sous `/usr/bin/bison` est trop ancienne sur l'hôte testé.

Depuis la racine du workspace ou du groupe de Spec, préparer un clone de travail
public, sans télécharger les dépendances graphiques Windows :

```sh
git clone --filter=blob:none https://github.com/ange-yaghi/engine-sim.git Build/EngineReference-Upstream
git -C Build/EngineReference-Upstream switch --detach 85f7c3b959a908ed5232ede4f1a4ac7eafe6b630
git -C Build/EngineReference-Upstream submodule update --init dependencies/submodules/simple-2d-constraint-solver dependencies/submodules/piranha dependencies/submodules/csv-io
python3 Silex-Examples/Tools/EngineReference/Build.py \
  --source Build/EngineReference-Upstream --output Build/EngineReference \
  --bison /chemin/vers/bison
```

Le clone doit posséder la révision `85f7c3b959a908ed5232ede4f1a4ac7eafe6b630`
et les sous-modules indiqués dans `Build.py`. Si la branche distante avance,
placer ce clone dédié à cette révision avant de préparer les sous-modules.
Le script archive ces commits, indépendamment de modifications locales du clone.
Il adapte uniquement sa copie générée dans `Build/EngineReference/Source`,
construit le helper et prépare son runtime. `Provenance.json` conserve les
révisions, l'empreinte du binaire et celle de la réponse impulsionnelle.
Ne pas placer de sources manuscrites dans ce dossier de génération.

Les adaptations de portabilité du chemin quatre temps conservent les valeurs et équations d’origine : includes
portables, constantes inline, valeurs de mélange par défaut explicites,
identifiant de template, include de type complet, correction d'un nom dans
`RingBuffer::overwrite`, chemins Piranha via `std::filesystem` et retrait d'un
include graphique inutilisé. Les profils originaux conservent leurs calculs de gaz et de contraintes. Le build n'inclut pas Delta Studio, Discord ou leur application.

La somme FIR peut être vectorisée par réassociation des additions, uniquement
pour `convolution_filter.cpp`. `--scalar-fir` prépare le témoin scalaire strict.
Le seuil de comparaison est un écart maximal de 32 unités PCM16 et un RMS
d'écart inférieur à 0,0001 de pleine échelle, avec régime identique. Ce seuil
contrôle l'adaptation numérique ; il ne prouve pas le réalisme perceptif.

## Exécuter et vérifier

La [démo](../../Sources/EngineAudio/README.fr.md) utilise `--reference`.
Le helper seul propose aussi deux rendus déterministes hors ligne :

```sh
cd Build/EngineReference/Runtime
../RenderReference Profile454.mr Impulse.pcm Witness full
../RenderReference Profile454.mr Impulse.pcm Base base
```

Chaque rendu écrit 14 secondes mono 44,1 kHz, le régime et les commandes dans un
CSV, puis une trace float32 à 10 kHz : régime, angle du cycle et les deux
pressions d'échappement. `full` conserve les réglages audio initiaux du profil.
`base` désactive convolution, dérivée, jitter et bruit d'écoulement : c'est un
étage de diagnostic défini, pas une identification des réglages du passage
4:48–5:00 de la vidéo.

Depuis la racine de travail, après le rendu de la démo :

```sh
python3 Silex-Examples/Tools/EngineReference/Verify.py \
  --binary Build/EngineReference/RenderReference \
  --runtime Build/EngineReference/Runtime \
  --bridge-wave Build/EngineReference/Bridge.wav \
  --report Build/EngineReference/Verification.json
```

Le contrôle vérifie les paquets, deux rendus identiques, les étapes mécaniques,
les bornes et le silence final, le rejet des requêtes invalides et la copie PCM
vers Silex avec son gain. `--scalar-binary /chemin/RenderReference` compare aussi
la somme vectorisée au contrôle scalaire. Le protocole privé `serve` reçoit une
ligne par bloc : nombre de frames mono (1–960), contact (0/1), pédale, texture,
convolution, régime de banc, charge. Il répond par quatre uint32 little-endian
(magic `0x34563845`, frames, régime × 1 000, état de démarrage), puis le PCM16 mono.
Le client Silex fournit sa copie stéréo au flux GFX.Audio.

Le runtime utilise la fréquence de simulation de chaque profil (10 à 40 kHz), huit sous-étapes de gaz et la synthèse
à 44,1 kHz. Le calcul complet reste assumé pour ce témoin unique. Le client interactif
utilise une file bornée et du polling sans attente ; le rendu hors ligne reste
synchrone. Les allocations, la latence et le coût de plusieurs véhicules en jeu ne
sont pas qualifiés par ce banc. Aucune portabilité Linux/Windows n'est annoncée
pour cet outil de développement macOS.

## Catalogue, transmission et deux temps

`Profiles.json` est la source unique des noms et réglages de véhicule. Silex
l’incorpore avec JSON ; Build.py projette les paramètres natifs, prépare les
scripts d’entrée et les impulsions PCM, puis conserve le catalogue et ses
empreintes dans `Provenance.json`. Les deux fichiers sous `Profiles/` dérivent
du mono TRX520 (MIT) et portent des adaptations de démonstration. Les références
à certaines IR `new/` du dépôt sont absentes au pin ; le catalogue choisit les
IR disponibles smooth_39, archive/test_engine_14 et test_engine_15. Ces choix
ne constituent pas une reproduction exacte des réglages de la vidéo.

Le mode privé `drive` ajoute trois champs après la commande `serve` : mode
(1 auto, 2 manuel), rapport demandé (0=N, puis 1..n), frein (0..1). Son en-tête
contient huit uint32 little-endian : magic `0x36563845`, frames, régime × 1 000,
démarrage, rapport, km/h × 1 000, flags (bit 0 passage, bit 1 refus surrégime),
compteur de passages. Le PCM16 mono suit cet en-tête de 32 octets. L’argument
optionnel final du helper est l’index du catalogue, par défaut 0 pour le 454.

`Drive.cpp` commande la transmission et le véhicule du simulateur, avec un
frein sur le corps représentant l’énergie de translation, une pression
d’embrayage progressive et une protection fondée sur le régime couplé prévu.
Le rapport change l’inertie réfléchie en conservant la vitesse du véhicule.
Le choix de véhicule ou Banc/Route nécessite moteur coupé et véhicule immobile.
Le transfert audio reste borné à quatre requêtes et un flux de cinq blocs.

`TwoStroke.py` applique uniquement à la copie générée une période d’allumage
configurable et une branche de gaz pour le mono 2T : ouvertures autour du point
mort bas, échappement avant transfert, puis compression et combustion à chaque
tour. Le réservoir de transfert à pression prescrite simplifie le carter-pompe.
Cette approximation n’est pas une simulation thermodynamique validée d’un 2T.
Les valeurs par défaut gardent le chemin quatre temps, contrôlé contre le
binaire 454 accepté. `CycleCheck` vérifie vingt étincelles contre dix sur vingt
tours de vilebrequin, en exécutant le module d’allumage adapté.

```sh
ctest --test-dir Build/EngineReference/CMake --output-on-failure
python3 Silex-Examples/Tools/EngineReference/FleetVerify.py \
  --binary Build/EngineReference/RenderReference \
  --runtime Build/EngineReference/Runtime \
  --report Build/EngineReference/Fleet-Native.json
```

Ce scénario vérifie les huit démarrages, passages auto, freinages et arrêts,
puis rapport manuel sûr, refus d’un rétrogradage dangereux, point mort,
continuité de vitesse et redépart. L’écoute et la qualification en jeu restent
nécessaires. Le build remplace le binaire par renommage d’un fichier neuf pour
préserver la cohérence des pages signées sur macOS pendant une reconstruction.

Les réponses cross sont préparées hors ligne : shelf de présence à 2 kHz,
corps grave du 4T à 250 Hz et queue amortie à 60/45 ms. Le canal audio passe
à 6 kHz pour ces deux profils, contre 1 900 Hz conservés pour les originaux.
Le 2T utilise une capture immédiate des crêtes, sans plancher d’atténuation,
pour préserver les transitoires avant conversion PCM16. Ces choix sont calibrés
sur les caractéristiques larges des prises fournies et demandent une écoute ;
les enregistrements utilisateur ne sont pas copiés dans les sources du package.

## Provenance

[engine-sim](https://github.com/ange-yaghi/engine-sim/tree/85f7c3b959a908ed5232ede4f1a4ac7eafe6b630),
copyright 2022 AngeTheGreat (Ange Yaghi), est accompagné de sa
[licence MIT](LICENSE.engine-sim), également copiée près du runtime généré.
Profil `assets/engines/chevrolet/engine_03_for_e1.mr`, réponse
`assets/sound-library/smooth/smooth_39.wav`. Le build utilise les sous-modules
[SCS](https://github.com/ange-yaghi/simple-2d-constraint-solver),
[Piranha](https://github.com/ange-yaghi/piranha) et
[csv-io](https://github.com/ange-yaghi/csv-io) aux commits verrouillés. Leurs
sources sont récupérées séparément ; elles ne sont pas incluses dans ce dépôt.
Les sources du moteur et l'audio de la vidéo ne sont pas copiés dans le package
GFX.Audio.
