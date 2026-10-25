# Observer la réaction d'un support mobile

Trois expériences évoluent ensemble : une plateforme de 1000 kg, une de
200 kg et une plateforme cinématique à vitesse imposée. Choisir une vue
conserve les trois simulations. Le panneau compare leurs vitesses ; le sol
quadrillé reste attaché au monde.

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release
```

- **1 / 2 / 3** : voir 1000 kg, 200 kg ou le support cinématique.
- **Z / S** : envoyer une impulsion dans le sens +Z / −Z. Les supports
  dynamiques reçoivent ±2M N·s ; le cinématique reçoit une variation imposée
  de ±2 m/s. Cliquer agit immédiatement, sans reset.
- **G** : serrer/libérer les freins des bandes des trois véhicules.
- **P** : pause/reprise. **R seul** : retour explicite au départ. **Échap** : quitter.

Attendre la réception au repos, puis pousser en +Z. Freins serrés, le support
cinématique reste à 2 m/s. Le support de 1000 kg et son véhicule convergent
vers 1.82 m/s ; ceux de 200 kg vers 1.33 m/s. La différence vient de la réaction
du véhicule : une plateforme de masse finie ralentit lorsqu'elle l'entraîne.
Une impulsion opposée ramène la quantité de mouvement horizontale totale à zéro.

Pour comparer les bandes libres, repartir avec R, libérer G, puis pousser.
Les roues tournent et le véhicule avance moins vite que le support. Le moteur
reste au point mort, sans gaz. Les suspensions, rotations et positions sont
issues du solveur, sans animation de pose imposée.

La plateforme mesure 8 × 0.4 × 12 m et repose sur un plan sans frottement.
Le véhicule est le profil de 100 kg et six rayons des autres exemples chenillés.
Les mondes dynamiques emploient 48 itérations de vitesse ; le cinématique
conserve le défaut 12. Ce test illustre la réaction réciproque et le roulement
relatif ; les impulsions répétées, sorties de plateforme, supports rotatifs et
la conduite générale ne sont pas qualifiés par son témoin fixé.

## Vérifier

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --controls-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --witness
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --smoke
```

Le témoin reproduit les six cas autonomes de `TrackedDynamicPlatformRun.py`
dans Silex-Benchmarks à 60/120 Hz. Le test des commandes utilise de vrais clics,
conserve identités et horloges et distingue impulsion, sélection, frein,
pause et retour au départ. Le smoke natif se ferme à la fin.
