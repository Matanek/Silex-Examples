# Comparer la prise KTM 250 SX et le mix E/G

Depuis la racine `SilexProject/` :

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

- **Prise originale** lit le coup de gaz enregistré entre 17,85 et 19,55 s.
- **Mix E/G intégral** lit l'extrait H, avec la matière de E jusqu'à 1,08 s
  puis le maintien de G. Les deux boutons utilisent le même volume.
- **Espace** ouvre les gaz. Le mode piloté rejoint la montée de H, prolonge
  son palier tant que la touche est enfoncée, puis rejoint sa retombée.
  Relâcher Espace plus tôt rejoint la descente à une cadence voisine.
  Le ralenti provient de 6,39–7,31 s de la même prise.
- **M** arrête le son. Quitter la fenêtre relâche les gaz.

Le maintien en direct répète environ 0,19 s du haut régime. Le mode KTM
utilise 826 Kio de PCM stéréo embarqué. La prise permet de piloter les coups
de gaz à l'écoute ; le banc Yamaha reste disponible pour imposer un régime
ou régler la charge avec `Build/YZ250-KTM --yz250`. [Guide du banc Yamaha](Docs/FR/README.md).

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --release -o Build/YZ250-KTM
Build/YZ250-KTM --ktm-check
```

Ce contrôle compare la sortie du générateur aux deux extraits embarqués,
échantillon par échantillon, et vérifie la montée, le relâchement, le maintien
et la réouverture. `PrepareKtm.py` empaquette les WAV `A-Source.wav`,
`H-Mix-E-G.wav` et `Decoded.wav` du dossier de comparaison. Les empreintes et
fenêtres sont dans [Assets/Ktm.json](Assets/Ktm.json).
