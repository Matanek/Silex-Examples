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
