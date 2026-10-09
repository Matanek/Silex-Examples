# Play and control a MIDI score

The score keeps its tempo changes. Choose a customized retro timbre or an
integrated sine instrument. The Audio plugin feeds playback on the application
thread; the example contains no sample or stream pumping loop.

From the SilexProject root (or the Spec Worktree group root):

```sh
silex compile Silex-Examples/Sources/MIDIPlayer/Main.sx --release -o .silex/midi-player
.silex/midi-player
```

Focus the window, then Space pauses/resumes, S stops, R replays, and Escape quits.
A finished playback stays available for replay. Append `--sine` to choose the
integrated instrument. Simple mode merges all channel notes and reports ignored
programs/controllers; it does not recreate the score's original orchestration.

```sh
.silex/midi-player --standalone
.silex/midi-player --standalone --sine
SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=dummy .silex/midi-player --check
```

Standalone mode deliberately blocks in `player.wait()`, which owns feeding.
The headless check exercises the actual plugin and pause/resume/stop controls.
Audio and the player are prepared during application setup; the plugin preserves
the provided Audio instance. Keep instrument/effect state exclusive to one player.
The player stores a bounded PCM queue rather than the complete song. See the
[GFX.Audio guide](https://github.com/Matanek/Silex-Lib-GFX.Audio/blob/main/Docs/EN/MusicPlayer.md)
for tails, errors, advanced routing, and buffer capacity.

[Lire en français](README.fr.md).

Add `--piano` to play the score with the built-in procedural piano:

```sh
.silex/midi-player --piano
.silex/midi-player --standalone --piano
```
