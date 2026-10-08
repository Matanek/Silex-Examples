# Produire des sons sans banque

Cette démonstration joue huit recettes de `GFX.Audio`, du bip au moteur à
régime variable et à la partition MIDI. Tous les échantillons sont calculés en
Silex. `Score.mid` contient 218 octets de commandes musicales ; aucun son ni
banque d’instruments n’est embarqué.

[English version](README.md).

## Écouter et choisir une recette

Depuis la racine `SilexProject/`, avec la toolchain et les packages locaux de la
Spec jusqu’à leur livraison :

```sh
silex compile Silex-Examples/Sources/ProceduralAudio/Main.sx --release -o .silex/procedural-audio
.silex/procedural-audio --case laser
.silex/procedural-audio --case midi
.silex/procedural-audio
```

Dans la Spec, utiliser sa racine `Worktree/` à la place. La démo demande
Silex 0.47.1 au minimum et les corrections locales de la Spec. `--help` affiche
les noms ; sans `--case`, les recettes jouent dans l’ordre du tableau. La sortie
audible utilise le périphérique par défaut. La durée et le nom sont affichés.

| Nom | Durée | Composition et paramètres à explorer |
| --- | ---: | --- |
| `beep` | 0,295 s | Sinusoïde 660 Hz ; attaque 5 ms, relâchement 120 ms. |
| `impact` | 0,260 s | Grave 65 Hz et bruit blanc filtré à 1 200 Hz ; graine 42. |
| `laser` | 0,750 s | Fréquence de 2 900 à 100 Hz sur 500 ms, enveloppe ADSR. |
| `explosion` | 1,250 s | Bruit blanc filtré à 450 Hz et grave 48 Hz ; graine 1985. |
| `engine` | 5,100 s | Fondamentale et harmonique modulées, bruit rose, quatre changements de régime lissés. |
| `retro` | 0,500 s | Onde carrée 440 Hz, bitcrusher 8 bits, maintien pendant six frames. |
| `melody` | 2,500 s | Instrument polyphonique, accord et quatre notes à 120 BPM, fin et relâchement inclus. |
| `midi` | 4,600 s | Deux pistes, trois bindings explicites, changement de tempo, sustain, panoramique et écho. |

Les premières recettes sont mono ; le MIDI est stéréo. Le niveau est conservé,
sans normalisation. Commencer avec un volume d’écoute modéré. `retro` est un
son court à texture rétro, pas l’émulation d’une puce particulière.

## Modifier les sons

[Recipes.sx](Recipes.sx) assemble les sources et les traitements. Changer une
fréquence en hertz, un gain linéaire ou les durées d’enveloppe change directement
le rendu. Toutes les recettes utilisent 48 000 frames par seconde : 240 frames
valent 5 ms. Le bitcrusher maintient une valeur pendant six frames, soit une
fréquence effective de 8 000 Hz. Les graines de bruit assurent la reproductibilité.

[Envelope.sx](Envelope.sx) et [Engine.sx](Engine.sx) sont des générateurs propres
à l’application qui implémentent `Synthesis.Generator`. Le premier déclenche le
relâchement à une frame précise ; le second segmente le rendu aux changements
de régime et utilise `Control` pour lisser hauteur et gain. On peut remplacer
ces compositions, développer ses propres générateurs et traitements, ou
fournir ses instruments aux bindings MIDI, sans appeler de boundary native.

La mélodie directe place ses notes tous les 24 000 frames : leur cadence ne
dépend pas d’un timer ou de la boucle de l’application. Le MIDI utilise les
changements de tempo de sa partition. Les contrôleurs de gain et panoramique
sont lissés sur 240 frames pour éviter les sauts audibles ; le réglage est
optionnel dans `MIDI.Synthesizer`. Aucune humanisation aléatoire n’est appliquée.
Ces recettes ne promettent pas un orchestre réaliste ni un hôte VST.

## Vérifier sans sortie audio

```sh
.silex/procedural-audio --check
.silex/procedural-audio --check --case engine
```

`--check` n’ouvre aucun périphérique. Pour chaque recette, il vérifie durée,
valeurs finies, marge sous la saturation, début et fin, puis compare les PCM
après reset avec des blocs de 480 et 257 frames. Il compare aussi le flux avec
le rendu complet, même lorsque sa capacité de 127 frames force des écritures
partielles. Les compteurs doivent montrer toutes les frames consommées et
aucune frame jetée. La dernière demi-seconde de la mélodie et la dernière
seconde du MIDI laissent finir relâchements et écho.

[Playback.sx](Playback.sx) prépare les sons courts avec `Audio.create` et fournit
les plus longs par `Synthesis.StreamProducer`. Cette vérification mesure la
cohérence du rendu ; l’écoute reste nécessaire pour juger le timbre et les
artefacts. Elle ne mesure ni les allocations ni le budget de temps d’un bloc.
