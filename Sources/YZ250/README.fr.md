# Comparer la prise KTM 250 SX et le mix E/G

Depuis la racine `SilexProject/` :

```sh
silex run Silex-Examples/Sources/YZ250/Main.sx
```

- **Prise originale** lit le coup de gaz enregistré entre 17,85 et 19,55 s.
- **Mix E/G intégral** lit l'extrait H, avec la matière de E jusqu'à 1,08 s
  puis le maintien de G. Les deux boutons utilisent le même volume.
- **Ralenti** démarre la boucle issue de 6,39–7,31 s de la prise.
- **Espace** donne un coup de gaz. L'ouverture dure environ 0,40 s avant
  de rejoindre H. Relâcher revient à la position du curseur.
- **Ouverture des gaz** dose l'accélération. La prise douce fournit deux
  paliers de gaz partiels. Une ouverture à 90 % ou plus laisse la montée
  se poursuivre vers H. Revenir à zéro ferme les gaz.
- **M** arrête le son. Quitter la fenêtre relâche les gaz.

Les deux ouvertures reprennent 12,92–14,81 s de la prise. Les raccords
réduisent le temps de montée en conservant la vitesse de lecture des portions.
L'ouverture douce couvre environ 1 s avant de rejoindre H si les gaz le
permettent. Les paliers de ce banc utilisent des boucles et des seuils
acoustiques. Dans un jeu, le régime et sa variation viendraient de la physique,
avec la charge pour choisir la texture. Le banc Yamaha reste accessible avec
`Build/YZ250-KTM --yz250`. [Guide du banc Yamaha](Docs/FR/README.md).

```sh
silex compile Silex-Examples/Sources/YZ250/Main.sx --release -o Build/YZ250-KTM
Build/YZ250-KTM --ktm-check
```

Ce contrôle compare la sortie aux deux extraits embarqués et vérifie le
coup de gaz, les deux paliers partiels, la retombée et la réouverture.
`PrepareKtm.py` empaquette les WAV `A-Source.wav`,
`H-Mix-E-G.wav` et `Decoded.wav` du dossier de comparaison. Les empreintes et
fenêtres sont dans [Assets/Ktm.json](Assets/Ktm.json).
