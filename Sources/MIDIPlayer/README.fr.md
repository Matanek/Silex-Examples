# Jouer et contrôler une partition MIDI

La partition conserve ses changements de tempo. Choisir un timbre rétro modifié
ou l’instrument sinus intégré. Le plugin Audio alimente la lecture sur le thread
applicatif ; l’exemple ne contient aucune boucle de pompage de samples ou de flux.

Depuis la racine SilexProject (ou celle du groupe Worktree de la Spec) :

```sh
silex compile Silex-Examples/Sources/MIDIPlayer/Main.sx --release -o .silex/midi-player
.silex/midi-player
```

Dans la fenêtre, Espace suspend/reprend, S arrête, R rejoue, Échap quitte.
Une lecture terminée reste disponible pour être rejouée. Ajouter `--sine` pour
choisir l’instrument intégré. Le mode simple réunit les notes des canaux et
signale les programmes/contrôleurs ignorés ; il ne reproduit pas l’orchestration
originale de la partition.

```sh
.silex/midi-player --standalone
.silex/midi-player --standalone --sine
SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=dummy .silex/midi-player --check
```

Le mode autonome attend volontairement dans `player.wait()`, qui possède
l’alimentation. Le contrôle sans fenêtre exerce le véritable plugin et les
commandes pause/reprise/arrêt. Audio et le player sont préparés dans la
configuration de l’application ; le plugin conserve l’Audio fourni.
Garder les états des instruments/effets exclusifs à une lecture. Le player
stocke une file PCM bornée, sans matérialiser le morceau complet. Le
[guide GFX.Audio](https://github.com/Matanek/Silex-Lib-GFX.Audio/blob/main/Docs/FR/MusicPlayer.md)
précise queues, erreurs, routage avancé et capacité des buffers.

[Read in English](README.md).
