# Franchir un tremplin avec le profil cross

Le profil de test inspiré du cross se conduit librement : châssis, suspensions, roue avant braquée et
rayons colorés suivent leurs états physiques. Les repères verts indiquent les
appuis ; la grille donne l’échelle en mètres et la caméra suit le châssis.

Depuis la racine du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release
```

- Maintenir **Z** : gaz normaux, à 40 % ; relâcher : roue libre.
- Maintenir **W** : plein gaz demandé, pour lever la roue avant.
- Maintenir **S** : freinage débrayé, prioritaire sur Z et W.
- Maintenir **← / →** : braquer ; relâcher : recentrer progressivement.
- **A** : activer/couper le pilote automatique de roulis.
- **L** : activer/couper la limite de braquage liée à la vitesse.
- **P** : impulsion physique de roulis de 150 N·m·s.
- **B** : comparer rampe et plan, en repartant du départ.
- **R** : recréer au départ en conservant le terrain et les choix A et L.
- **Espace** : suspendre/reprendre ; **Échap** : quitter.

La scène démarre face à un tremplin orange de 16°, à environ 12 m. Attendre les appuis,
puis maintenir Z tout droit : la moto monte, quitte les deux appuis et atterrit
sur le plan. Les suspensions se détendent en vol puis reprennent la charge.
L’interface distingue le vol sans appui de la roue arrière et affiche la
réception. B remet au départ sur le plan, puis rétablit la rampe à l’appui
suivant ; cette comparaison conserve les choix A/L. B et R reprennent une
simulation suspendue et relâchent les commandes tenues.

Pour une roue arrière, repartir avec R, attendre les appuis puis maintenir W.
La puissance et le transfert de charge soulèvent réellement la roue avant.
Le gaz se module selon le tangage relatif à la pente et sa vitesse pour limiter le retournement
arrière ; aucune pose ni impulsion de cabrage n’est imposée. Relâcher W et
freiner repose la roue. Z permet une conduite plus modérée.

A coupe seulement le correcteur de roulis. Sans lui, cette moto n’a ni pilote
simulé ni commande manuelle d’inclinaison : elle est instable en virage.
Ce mode sert à comparer l’effet de l’équilibre automatique. Pour comparer au
repos, essayer R puis P, et répéter après A et R. L retire la limite de
braquage, tandis que l’entrée progressive reste active.

Après une chute (inclinaison du châssis d’environ 73°), les gaz et le pilote
se coupent jusqu’à R. Le corps continue sa chute physique ; le correcteur ne
se réactive pas pendant les rebonds. A choisit alors le mode au prochain R,
indiqué par le bouton. Les six boutons font les mêmes actions ponctuelles.
La perte de focus, la pause, B et R relâchent Z/W/S et le braquage. P demandé
pendant la pause attend la reprise ; R l’annule.

Le profil conserve 100 kg et une inertie isotrope de 100 kg·m². Le moteur
idéal fournit jusqu’à 120 N·m (+50 %) ; la transmission manuelle 3×3,42 entraîne la roue
arrière. Les roues de 30 cm sont placées à +1,25 m et −0,75 m du châssis,
ce qui déplace la répartition de charge vers l’arrière. Les ressorts et amortisseurs sont réglés
à 5000 N/m et 500 N·s/m, moitié des valeurs route. Le débattement passe de
40 à 70 cm (longueurs 0,2–0,9 m). Les attaches sont remontées de 20 cm
pour garder le centre de masse bas avec ces suspensions plus longues. Simulation à 120 Hz, entrée de direction bornée
avant lissage, inversion complète en 0,3 s. Le pilote vise au plus 0,5 rad
de roulis. Les contacts utilisent des rayons sur un plan et une rampe fixe de
8 × 0,4 × 9 m, centrée en (0 ; 1,0514218 ; 16,5) m et inclinée de −0,28 rad
autour de X. Le bord de sortie atteint 2,49 m. Les pneus ne sont pas des corps rigides séparés. Ce profil n’est pas calibré sur une moto réelle.

## Vérification sans fenêtre

```sh
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Model.sx --nocache
silex test Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --nocache
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --physics-check
silex run Silex-Examples/Sources/Physics3D/MotorcycleDriving/Main.sx --release -- --controls-check
```

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

`--cross-check` émet 5 764 états du profil cross, comparant plan et nouveau
tremplin. Le témoin `MotorcycleCross` conserve les budgets du châssis sur toute
la réception et vérifie gaz, mémoire de pente, gravité et rotors indépendamment.
Le châssis culmine vers 4,02 m et reste environ 1,08 s sans appui dans ce parcours.
Le pilote mémorise la pente des appuis chargés pendant le vol ; il module les
gaz, sans imposer de couple de tangage aérien ni de pose. Les deux témoins
précédents gardent leurs réglages route et servent de régressions, tandis que
la conduite libre démarre directement avec le profil cross.

`--smoke` ouvre une fenêtre « TEST AUTOMATIQUE », joue les huit recettes
(les six historiques, la rampe route puis le tremplin cross), vérifie cadrage, transforms réels, roues, appuis, pause et recréation, puis se
ferme avec son marqueur final. Une fermeture anticipée ne valide pas ce contrôle.
Après accident, la preuve vise la coupure persistante et l’absence de rotation
entretenue : moins de 2 cm et 0,05 rad de variation sur les deux dernières
secondes. Elle ne promet pas une vitesse angulaire exactement nulle au contact.
