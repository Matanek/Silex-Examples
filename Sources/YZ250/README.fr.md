# Comparer la prise KTM 250 SX et le mix E/G

Depuis la racine `SilexProject/` :

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

- **Prise originale** lit le coup de gaz enregistré entre 17,85 et 19,55 s.
- **Mix E/G intégral** lit l'extrait H, avec la matière de E jusqu'à 1,08 s
  puis le maintien de G. Les deux boutons utilisent le même volume.
- **Ralenti** démarre la boucle issue de 6,39–7,31 s de la prise.
- **Espace** ouvre les gaz. Le début de l'accélération reprend 12,92–14,81 s
  de la prise à vitesse d'origine, puis rejoint la montée de H. Maintenir
  Espace prolonge le palier. Relâcher pendant l'ouverture revient au ralenti,
  et relâcher après le raccord rejoint la retombée à une cadence voisine.
- **M** arrête le son. Quitter la fenêtre relâche les gaz.

Le maintien en direct répète environ 0,19 s du haut régime. Le mode KTM
utilise 1,12 Mio de PCM stéréo embarqué. La prise permet de piloter les coups
de gaz à l'écoute ; le banc Yamaha reste disponible pour imposer un régime
ou régler la charge avec `Build/YZ250-KTM --yz250`. [Guide du banc Yamaha](Docs/FR/README.md).

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --release -o Build/YZ250-KTM
Build/YZ250-KTM --ktm-check
```

Ce contrôle compare la sortie du générateur aux deux extraits embarqués et
à l'ouverture enregistrée entre les raccords, échantillon par échantillon.
Il vérifie aussi le relâchement, le maintien et la réouverture.
`PrepareKtm.py` empaquette les WAV `A-Source.wav`,
`H-Mix-E-G.wav` et `Decoded.wav` du dossier de comparaison. Les empreintes et
fenêtres sont dans [Assets/Ktm.json](Assets/Ktm.json).
