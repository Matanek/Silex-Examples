# Franchir un tremplin avec le profil cross

Le profil de test inspiré du cross se conduit librement : châssis, suspensions, roue avant braquée et
rayons colorés suivent leurs états physiques. Les repères verts indiquent les
appuis. Le sol utilise la texture `World3D/Assets/DarkGrid.png` : les petites
cases mesurent un mètre et restent ancrées au monde pendant les déplacements.
La caméra suit la moto depuis l’arrière, avec une position et un cap amortis.
Elle garde l’horizon droit pendant les virages, les cabrages et les sauts ; après
une chute, son cap se stabilise. R et B la replacent immédiatement au départ.

Les mesures et les cinq boutons sont regroupés dans un panneau compact à gauche.
Le centre et le haut de la scène restent dégagés pour repérer le tremplin.

Depuis la racine du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release
```

- Maintenir **Z** : couple normal demandé à 40 % ; relâcher : frein moteur.
- Maintenir **W** : plein gaz demandé, pour lever la roue avant.
- Maintenir **S** : freinage débrayé, prioritaire sur Z et W.
- Maintenir **Q / D** : tourner à gauche/droite depuis la vue arrière ; relâcher : recentrer progressivement.
- Les lettres suivent les caractères du clavier : **ZQSD** sur AZERTY.
- **A** : activer/couper le pilote automatique de roulis.
- **L** : activer/couper la limite de braquage liée à la vitesse.
- **P** : impulsion physique de roulis de 150 N·m·s.
- **B** : comparer rampe et plan, en repartant du départ.
- **R** : recréer au départ en conservant le terrain et les choix A et L.
- Maintenir **Espace** : frein arrière seul ; relâcher pour reprendre l’adhérence. **Échap** : quitter.

La scène démarre face à un tremplin orange de 16°, à environ 12 m. Attendre les appuis,
puis maintenir Z tout droit : la moto monte, quitte les deux appuis et atterrit
sur le plan. Les suspensions se détendent en vol puis reprennent la charge.
L’interface distingue le vol sans appui de la roue arrière et affiche la
réception. B remet au départ sur le plan, puis rétablit la rampe à l’appui
suivant ; cette comparaison conserve les choix A/L. B et R relâchent les commandes tenues.

Pour essayer la roue arrière sur le plat, appuyer sur B, attendre les appuis,
puis maintenir Z : la roue avant se soulève sous le couple et le transfert de
charge. W demande davantage de gaz dès le départ. Le cabrage reste autorisé
à basse et moyenne vitesse ; le pilote réduit progressivement sa marge entre
29 et 50 km/h pour retrouver l’appui avant quand la vitesse augmente. Relâcher
les gaz et freiner repose la roue. Aucun saut, pose ou élan de cabrage n’est
imposé. L’affichage indique les gaz réellement appliqués et la compression
avant/arrière en centimètres, mesurée depuis la détente maximale.

A coupe le correcteur de roulis et les aides qui coordonnent les virages avec le moteur. Sans lui, cette moto n’a ni pilote
simulé ni commande manuelle d’inclinaison : elle est instable en virage.
Ce mode sert à comparer l’effet de l’équilibre automatique. Pour comparer au
repos, essayer R puis P, et répéter après A et R. L retire la limite de
braquage, tandis que l’entrée progressive reste active.

Après une chute (inclinaison du châssis d’environ 73°), les gaz et le pilote
se coupent jusqu’à R. Le corps continue sa chute physique ; le correcteur ne
se réactive pas pendant les rebonds. A choisit alors le mode au prochain R,
indiqué par le bouton. Les cinq boutons font les mêmes actions ponctuelles.
La perte de focus, B et R relâchent Z/W/S, le braquage et le frein arrière.
La conduite libre n’a plus de commande de pause.

Le profil conserve 100 kg et une inertie isotrope de 100 kg·m². Le moteur
idéal fournit jusqu’à 180 N·m ; la transmission manuelle 3×3,42 entraîne la roue
arrière. Les roues de 30 cm sont placées à +1,25 m et −0,75 m du châssis,
ce qui déplace la répartition de charge vers l’arrière. Les ressorts et amortisseurs sont réglés
à 2500 N/m et 350 N·s/m. Le débattement est de 70 cm (longueurs 0,2–0,9 m),
avec des attaches 10 cm au-dessus du centre du châssis. L’enfoncement au repos
est d’environ 14 cm à l’avant et 26 cm à l’arrière ; sous accélération, l’arrière
atteint environ 40 cm de compression. La réception utilise presque toute la
course avant que la moto reprenne son assiette. Simulation à 120 Hz, direction progressive avec saturation douce selon la vitesse.
Le pilote autorise jusqu’à 0,95 rad (54°) de roulis, avec un correcteur moins
raide et un amortissement proche du critique. Le braquage tient compte du
carrossage et garde une transition progressive à grande vitesse. Sous assistance,
le pilote limite le cabrage en virage, allège la transmission pendant une
inversion et réserve de l’adhérence latérale en limitant le couple arrière.
Les grands virages et inversions Z/W sont vérifiés à 60/120 Hz, puis à dix
changements de direction par seconde, sans chute ni glisse arrière excessive.
Le départ Z de 0 à 40 km/h prend environ 1,87–1,89 s dans cette recette, contre
2,25 s avec le candidat précédent. Le cabrage est moins haut avec Z pour
accélérer plus vite ; W conserve un cabrage plus marqué.
L’amortissement moteur est de 1,5 s⁻¹. Sous les gaz, le pilote compense les
pertes internes pour conserver la réponse de couple du profil cross ; au lever
des gaz, cette compensation cesse. Le HUD affiche les gaz réellement appliqués. Le frein arrière atteint 260 N·m avec
une montée de commande en 0,20 s et une libération en 0,08 s.
Les pneus utilisent une adhérence combinée : freinage et virage partagent le
même budget d’efforts, avec un coefficient effectif de 1,4 sur ce sol. Les contacts utilisent des rayons sur un plan et une rampe fixe de
8 × 0,4 × 9 m, centrée en (0 ; 1,0514218 ; 16,5) m et inclinée de −0,28 rad
autour de X. Le bord de sortie atteint 2,49 m. Les pneus ne sont pas des corps rigides séparés. Ce profil n’est pas calibré sur une moto réelle.

Pour essayer la glisse, B passe sur le plat : accélérer avec Z, relâcher les
gaz, tenir Q ou D puis maintenir brièvement Espace. L’arrière peut se bloquer
et déborder ; relâcher Espace permet à la roue de reprendre son roulement.
Un freinage prolongé ou une manœuvre excessive peut toujours faire chuter la
moto. La dérive provient des contacts et des efforts de pneus ; aucun lacet
ni pose de glisse ne sont imposés. Le frein arrière reste indépendant de S
et peut être combiné aux gaz.

## Vérification sans fenêtre

```sh
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Model.sx --nocache
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Handling.sx --nocache
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --nocache
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/ChaseCamera.sx --nocache
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Ground.sx --nocache
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --controls-check
```

`--view-check` vérifie le cadrage des neuf recettes avec le suivi arrière,
l’horizon, la pause et le reset, sans fenêtre. Les tests de sol vérifient que
les mêmes points du monde gardent leur phase de texture après recentrage.

`--oracle-check` émet les 17 292 états de six recettes de 16 s à 60/120 Hz :
départ/freinage, inversions miroirs, roue arrière, récupération puis accident,
et chute sans pilote. Ils utilisent le même profil et les mêmes commandes
que le témoin `MotorcycleHandling` de Silex-Benchmarks. Les contrôles physiques
ajoutent des virages tenus trois secondes puis dix changements de direction
par seconde. `--ramp-check` émet en plus 5 764 états de comparaison plan/rampe,
identiques au témoin `MotorcycleRamp`. Celui-ci vérifie le vol balistique,
les contacts sur la boîte finie et la réception à 60/120 Hz. La qualification
porte sur cette approche droite avec Z, pas sur tout terrain ou toute manœuvre.
Le mode interactif ne rejoue aucune de ces séquences.

`--cross-check` émet 8 646 états du profil cross : Z tenu depuis le départ,
tremplin et reprise de Z vers 16 km/h. Le témoin `MotorcycleCross` conserve les budgets du châssis sur toute
la réception et vérifie gaz, mémoire de pente, gravité et rotors indépendamment.
Le parcours conserve un envol physique suivi de la reprise des appuis et du freinage.
Le pilote mémorise la pente des appuis chargés pendant le vol ; il module les
gaz, sans imposer de couple de tangage aérien ni de pose. Les deux témoins
précédents gardent leurs réglages route et servent de régressions, tandis que
la conduite libre utilise le profil cross avec les nouveaux réglages d’inclinaison,
de frein moteur et d’adhérence combinée. Ces réglages sont contrôlés par
`Handling.sx` : virages miroirs Z/W à 60/120 Hz, inversions soutenues puis rapides,
accélération, décélération, frein arrière sélectif,
budget d’efforts et reprise d’adhérence. Les témoins historiques conservent
leur ancien profil ; leur parité Jolt ne qualifie pas l’adhérence combinée. W est vérifié par
les tests consommateurs de levée, compression, freinage et reprise des appuis ;
sa parité Jolt point par point sur une roue arrière prolongée reste non qualifiée.

`--smoke` ouvre une fenêtre « TEST AUTOMATIQUE », joue les neuf recettes
(les six historiques, la rampe route, le tremplin cross puis le frein arrière en virage), vérifie cadrage, transforms réels, roues, appuis, pause et recréation, puis se
ferme avec son marqueur final. Une fermeture anticipée ne valide pas ce contrôle.
Après accident, la preuve vise la coupure persistante et l’absence de rotation
entretenue : moins de 2 cm et 0,05 rad de variation sur les deux dernières
secondes. Elle ne promet pas une vitesse angulaire exactement nulle au contact.
