# Témoin sonore engine-sim

[English](README.md)

Cet outil de développement fait tourner le Chevrolet 454 original hors de son
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

Les adaptations conservent les valeurs et équations d'origine : includes
portables, constantes inline, valeurs de mélange par défaut explicites,
identifiant de template, include de type complet, correction d'un nom dans
`RingBuffer::overwrite`, chemins Piranha via `std::filesystem` et retrait d'un
include graphique inutilisé. Les calculs de gaz et de contraintes restent ceux
d'engine-sim. Le build n'inclut pas Delta Studio, Discord ou leur application.

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

Le runtime utilise la simulation à 10 kHz, huit sous-étapes de gaz et la synthèse
à 44,1 kHz. Le calcul complet reste assumé pour ce témoin unique. Le client interactif
utilise une file bornée et du polling sans attente ; le rendu hors ligne reste
synchrone. Les allocations, la latence et le coût de plusieurs véhicules en jeu ne
sont pas qualifiés par ce banc. Aucune portabilité Linux/Windows n'est annoncée
pour cet outil de développement macOS.

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
