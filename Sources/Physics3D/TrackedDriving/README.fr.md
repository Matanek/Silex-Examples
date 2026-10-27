# Franchir une rampe avec deux chenilles et une boîte automatique

Conduire en continu et observer les trois rapports avant et arrière, les
interruptions de couple et l’engagement de l’embrayage. Les six suspensions,
les rayons bleus/orange et les repères verts suivent les états physiques.
Le panneau donne rapport, régime, embrayage et vitesses des deux bandes.

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release
```

- Maintenir **Z/S** : avancer/reculer. Une inversion freine avant d’entraîner
  les bandes dans l’autre sens ; elle ne remet pas au départ.
- Maintenir **Q/D** ou **←/→** : tourner. Sans gaz à très faible vitesse,
  les bandes tournent en sens opposés pour pivoter.
- Maintenir **Espace** : frein. Au relâchement des gaz, le véhicule roule sur
  son élan ; un frein léger le maintient presque à l’arrêt.
- **B/F** : ajouter la rampe/revenir au plat à la pose courante ; retirer un
  appui peut naturellement faire retomber le châssis.
- **M** : activer/couper le pilote du cycle depuis l’état courant. Une touche
  de conduite reprend la main. La boîte automatique fonctionne aussi en conduite
  manuelle : le pilote et la transmission sont deux choses distinctes.
- **P** : pause/reprise ; **R seul** : retour au départ sur le terrain choisi,
  avec la même boîte ; **Échap** : quitter.

Les cinq boutons concernent terrain, pilote, pause et reset. Les relâchements
et la perte de focus libèrent la conduite. B/F et M conservent la pause ; R
reprend la simulation. Les commandes conservent identité, pose, vitesses et
horloge ; la conduite continue après seize secondes. Aucune pose/vitesse de
châssis ou rotation de roue n’est imposée par les commandes.

## Voir les rapports changer

La fenêtre démarre devant la rampe. **F**, puis **R**, permettent de comparer
le même départ sur plat ; **B**, puis **R**, rétablissent la rampe. Maintenir Z pour voir 1/2/3 et l’embrayage
s’ouvrir puis se refermer. Freiner ensuite pour observer les rétrogradages
et le point mort. S entraîne les mêmes passages en marche arrière.
La conduite au clavier module couple et différence des bandes avec la vitesse,
avec une cible d’environ 9 m/s pour rester maniable ; moteur et suspensions sont
les mêmes que dans le témoin qualifié.

Pour voir le cycle qualifié sans moduler les gaz, activer **M**, puis **R**
pour repartir explicitement du départ : 2 s de stabilisation, 4 s à 80 % de gaz et
10 s de freinage à 4 %, puis maintien au repos. Il ne redémarre pas tout seul.
Le panneau distingue « Pilote » et « boîte auto » ; R seul recrée le véhicule.
La caméra suit le châssis et la grille indique des mètres. Sur rampe, le
pilote monte, quitte les six appuis pendant environ 0.39 s puis réceptionne
avant de freiner jusqu’au repos. Le panneau indique le vol puis la reprise
des appuis ; les repères verts disparaissent pendant le vol.

## Modèle et qualification

100 kg, inerties 100 kg·m², six roues de 30 cm, suspensions 10000 N/m et 1000 N·s/m,
bandes d’inertie 2 kg·m², moteur 15 N·m et différentiel 6. La boîte utilise
2/1.4/1 et −2/−1.4/−1, seuils 1800/1200 RPM, changement 0.5 s, engagement 0.3 s,
latence 0.5 s. Le frein modéré vaut 60 N·m par bande. Les bandes sont un couplage
idéal, sans maillons articulés ; les contacts sont six rayons.

Le témoin autonome `TrackedAutomaticRun.py` de Silex-Benchmarks qualifie sur
plan les passages avant/arrière et l’interdiction de monter un rapport sans
appui ou avec bandes opposées. La scène reproduit exactement les deux cas
avant/arrière. Les huit recettes manuelles historiques, dont le franchissement
de rampe, restent dans les tests avec leurs témoins inchangés.

`TrackedAutomaticRampRun.py` compare en plus plat et rampe avec la boîte
automatique à 60/120 Hz, Native Debug/Release. La scène reproduit exactement
ces deux parcours de 16 s : boîte de 8 × 0.4 × 6.03 m inclinée de 0.1 rad,
montée, vol, réception et retour au repos. Les séquences de rapports et
l’embrayage restent qualifiés pendant ce parcours. Être déjà en troisième
pendant le vol ne prouve pas l’interdiction de monter un rapport sans appui ;
celle-ci garde ses témoins indépendants sur plan.

La rectitude prolongée à haute vitesse, les terrains généraux, le freinage
extrême et les contacts de chenille à maillons ne sont pas prouvés par ces recettes.

## Vérifier

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --controls-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --automatic-physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --automatic-ramp-physics-check
```

`--controls-check` vérifie touches tenues, relâchement/focus, virages, freinage,
marche arrière, pause, pilote et cinq boutons dans les deux profils, avec
conservation des états et R séparé. `--physics-check` conserve les recettes
manuelles ; `--automatic-physics-check` vérifie 1/2/3/2/1/point mort, embrayage,
repos et conservation du profil lors du reset à 60/120 Hz.

`--oracle-check` émet 8 652 états historiques ; `--ramp-check`, 5 044 états plat/rampe ;
`--automatic-check`, 5 764 états avant/arrière identiques au benchmark qualifié.
`--smoke` joue les huit recettes manuelles avec cadrage, roues, appuis et rampe.
`--live-smoke` joue 18 s de commandes continues automatiques, terrain, pilote,
pause et reprise manuelle sans reset. Une fermeture anticipée ne valide pas
ces contrôles ; les fenêtres « TEST AUTOMATIQUE » se ferment à leur fin.

`--automatic-ramp-check` émet 5 764 états plat/rampe, byte-identiques au nouveau
témoin qualifié. `--automatic-ramp-physics-check` vérifie montée, vol,
réception et repos contre le plat à 60/120 Hz, puis le reset explicite.
`--automatic-smoke` joue ces deux parcours dans la fenêtre native avec boîte
automatique, roues, marqueurs d’appui, caméra et pause finale contrôlés.
Le passage au second terrain recrée explicitement le véhicule dans ce test ;
les commandes interactives B/F et M continuent à conserver le véhicule.


## Observer l'entraînement par une plateforme

Pour ouvrir le mode plateforme depuis la même racine :

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --platform
```

Cliquer sur **Déplacer lat. (B)** ou **Déplacer long. (F)** : la plateforme
bleue se déplace immédiatement à 2 m/s pendant 2 s, puis s'arrête.
**Déplacer (M)** relance le dernier axe ; pendant le mouvement, ce bouton devient
**Arrêter (M)**. Chaque déplacement part de l'état courant, sans reset.
Le châssis reste dynamique ; le contact entraîne le véhicule, sans lui imposer
une pose ou une vitesse. Le panneau compare vitesses du véhicule et du support,
avec appuis, rapport au point mort, régime et rotation des bandes.

- **B/F** : lancer un déplacement latéral/longitudinal, y compris après un arrêt.
- **G** : serrer/libérer le frein de maintien. L'effet apparaît pendant le
  mouvement ; le bouton indique l'état du frein même à l'arrêt.
- **M** : démarrer/arrêter le déplacement. Après les 2 s, un clic le relance.
- **Espace** : serrer le frein tant que la touche reste tenue, sans couper M.
- **ZQSD** : reprendre la conduite ; cette reprise arrête le déplacement du
  support. Le frein de maintien G reste appliqué jusqu'à sa libération.
- **P** : pause/reprise. **R seul** replace véhicule et support au départ,
  conserve axe/frein et reprend la simulation. **Échap** quitte.

Pour comparer les deux freins depuis le même départ : **R**, attendre les appuis,
puis **F** ; refaire **R**, **G**, attendre les appuis, puis **F**. Le reset est
une aide à la comparaison ; les boutons de déplacement fonctionnent sans lui.

Freins serrés, le véhicule suit presque le support à 2 m/s. Libres en
longitudinal, les roues roulent : le véhicule avance à environ 0.615 m/s,
la plateforme va plus vite et les bandes tournent dans l'autre sens relatif.
Le véhicule s'arrête vers 1.23 m, contre environ 4 m avec les freins serrés.
Les traits de grille restent des repères du monde ; le seul support physique
est la boîte bleue de 8 × 0.4 × 12 m. En conduite libre, on peut en sortir ;
R rétablit alors le départ.

`TrackedPlatformRun.py` qualifie les quatre recettes de 6 s à 60/120 Hz,
Native Debug/Release. `--platform-check` émet les 4 328 états identiques au
benchmark, `--platform-physics-check` vérifie entraînement/roulement/repos et
reset, `--platform-controls-check` vérifie commandes et boutons sans reset
implicite et le redémarrage après un parcours. `--platform-click-smoke` exerce
les clics dans la fenêtre native, avec départ immédiat, arrêt, relance et frein.
`--platform-smoke` joue les quatre cas dans la fenêtre native,
avec plateforme, châssis, roues, appuis, cadrage et pause contrôlés.
Cette qualification porte sur la translation horizontale, au point mort et
sans gaz ; conduite libre, support rotatif ou dynamique et terrains généraux
ne sont pas prouvés par ces quatre recettes.

## Conduite longue avec un profil de précision explicite

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long
```

Le mode long utilise 48 itérations de vitesse et 4 de position à 120 Hz, pour un
trajet 20 s : réception 2 s, accélération 8 s et freinage 10 s. Appuyer sur **M** ou
« Pilote ON/OFF » pour lancer le cycle depuis la position courante. Il atteint
environ 90 km/h et parcourt 176 m sur le plan. **R seul** remet au départ.
**ZQSD**, **Espace** et **P** conservent conduite continue, frein et pause ; une
commande de conduite reprend la main sur le pilote. Le terrain du test est plat.

Le HUD 300 × 400 reste à gauche ; caméra et grille suivent le véhicule. Les
positions, roues, suspensions et rapports viennent de la simulation. Les
commandes ordinaires ne recréent pas le véhicule et ne remettent pas l’horloge
à zéro. M relance le programme, sans replacer le véhicule ; R permet de refaire
le témoin exact depuis le repos. Les autres modes gardent leurs profils.

Le témoin autonome avant/arrière à 60/120 Hz contient 7204 états identiques au
sous-ensemble chargé de TrackedAutomaticLong. Son profil 48/4 est qualifié ;
le trajet long au profil 12/4 conserve son échec de parité d’environ 7,04 cm pour
un budget 5 cm. Cette scène ne résout pas ce cas 12/4 et ne modifie pas le SDK.
Elle ne qualifie pas les virages à grande vitesse ni les terrains arbitraires.

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long-physics-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long-controls-check
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --long-smoke
```

Le smoke ouvre « TEST AUTOMATIQUE », lance un cycle complet 20 s par un vrai clic,
vérifie les poses rendues, la grille et la caméra suivies, puis se ferme seul.
Les contrôles sans fenêtre vérifient aussi l’encre du HUD, les clics, la pause,
la reprise manuelle et R. Le profil de précision augmente les itérations ;
aucune mesure ou promesse de FPS n’est fournie par ce parcours.

### Sens de direction dans le repère du véhicule

En marche avant et en pivot, **Q / flèche gauche** oriente l’avant vers la
gauche du véhicule ; **D / flèche droite** l’oriente vers sa droite. Ce repère
suit le véhicule lorsqu’il change de cap. Les vitesses G/D affichées suivent
la même convention. Cette association corrige les commandes interactives ;
le parcours automatique rectiligne et les témoins physiques sont conservés.

Le contrôle sans fenêtre inclut les touches logiques AZERTY et les flèches,
en déplacement et en pivot, avec deux caps initiaux :

```sh
silex run Silex-Examples/Sources/Physics3D/TrackedDriving/Main.sx --release -- --steering-check
```
