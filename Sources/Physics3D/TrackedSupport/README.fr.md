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

## Observer le transport par un support tournant

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation
```

Trois supports cinématiques à pivot fixe comparent les deux sens de rotation
et un contrôle immobile. Le véhicule démarre à un mètre du pivot rouge ; sa
position et son orientation évoluent par les contacts des roues. La grille
reste fixe dans le monde. Le panneau affiche les vitesses angulaires autour de Y.

- **1 / 2 / 3** : rotation +Y, rotation −Y ou support immobile.
- **Z / Lancer** : imposer +0.25 / −0.25 rad/s aux deux supports mobiles.
- **S / Arrêter** : arrêter les supports sans déplacer les véhicules.
- **G** : serrer/libérer les chenilles ; **P** : pause ; **R seul** : départ.

Attendre la réception, lancer avec les freins serrés, puis comparer les deux
sens. Le véhicule est entraîné en rotation. Arrêter avec S, repartir avec R,
libérer G puis relancer : les bandes roulent et le mouvement relatif devient
visible. Les trois simulations avancent ensemble ; changer de vue ne réinitialise
rien. Lancer plusieurs fois fixe la même vitesse, sans l'accumuler.

Le témoin fixe quatre cas de six secondes à 60/120 Hz : immobile, rotations
opposées freinées et rotation +Y avec bandes libres. Le support tourne entre
2 et 4 secondes puis s'arrête. Les 4328 états de la scène sont identiques au
benchmark `TrackedRotatingPlatformRun.py` qualifié face à Jolt. Le mode conserve
12 itérations de vitesse. La rotation d'un support dynamique de masse finie et
la conduite générale sur terrain mobile restent hors de cette qualification.

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation-controls-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation-physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation-witness
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --rotation-smoke
```

## Observer un support qui avance tout en tournant

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --combined
```

Les trois vues comparent maintenant un support qui avance en +Z et tourne
autour de +Y, son miroir −Z/−Y et un contrôle immobile. Le repère rouge suit
le centre réel du support ; la grille reste fixe dans le monde.

- **Z / Lancer** fixe simultanément ±2 m/s et±0.25 rad/s sur les deux supports.
- **S / Arrêter** fixe leurs deux vitesses à zéro, sans replacer les véhicules.
- **1 / 2 / 3** change seulement de vue ; **G** bloque/libère les bandes.
- **P** pause/reprise ; **R seul** replace les expériences ; **Échap** quitte.

Attendre la réception, puis lancer avec les freins serrés : le véhicule est
transporté et tourne par ses contacts. Arrêter, repartir avec R, libérer G et
relancer pour voir les bandes rouler et le mouvement relatif apparaître.
Le panneau gauche de 300×400 affiche quatre lignes complètes : vitesse Z en m/s
puis rotation Y en rad/s, véhicule/support. Le HUD laisse le reste de la vue
disponible. Les commandes agissent immédiatement et les trois mondes gardent
leurs identités et horloges. RépéterZ ne cumule pas les vitesses.

Le témoin fixe les mêmes quatre cas de 6 s à 60/120 Hz que le benchmark combiné :
le support avance et tourne entre 2 s et 4 s, puis s’arrête. Dans le cas libre,
les freins sont serrés explicitement à 4 s pour tester le repos final. Les 4328
états sont identiques au témoin autonome. Le profil reste 12/4, sans animation
imposée du châssis. La vitesse transmise combine la translation du support
et sa rotation autour de son centre.

Le support reste une surface finie. En utilisation libre prolongée, le véhicule
peut quitter la plateforme ; R ramène l’expérience au départ. Cette preuve
ne couvre pas un support de masse finie tournant librement, le terrain
arbitraire ou une conduite générale sur plusieurs supports.

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --combined-controls-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --combined-physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --combined-witness
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --hud-check
silex run Silex-Examples/Sources/Physics3D/TrackedSupport/Main.sx --release -- --combined-smoke
```

Les contrôles couvrent les vrais clics, la vitesse au point, les bandes libres
ou verrouillées, la pause et R seul au départ. Le texte du HUD est mesuré dans
les vraies commandes Canvas des neuf vues en mouvement. Le smoke combiné
annonce « TEST AUTOMATIQUE », compare les trois vues, libère puis resserre
les freins avant l’arrêt final et se ferme seul. Il ne constitue pas une
mesure comparative de FPS.
