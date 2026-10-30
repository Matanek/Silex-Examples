# Tester un pneu souple

Une roue motorisée roule sur un sol plat et franchit une petite marche. Sa
carcasse déformable est retenue sur une jante dynamique par deux rangées de
talons élastiques. Le profil de départ peu gonflé et les flancs souples
accentuent l’écrasement ; augmenter la charge ou changer le gonflage modifie
réellement sa réponse.

Depuis la racine `SilexProject/`, avec le compilateur et les packages du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/SoftTire/Main.sx --backend native --release
```

Utiliser la version Release pour l’essai interactif. La version Debug sert aux
vérifications et son coût de simulation est beaucoup plus élevé.

| Commande | Action |
| --- | --- |
| Z / S maintenu | Moteur avant / arrière |
| Espace maintenu | Freiner la jante |
| C | Alterner la charge de jante : 20 / 50 kg |
| P | Alterner le gonflage : cross / très bas / ferme |
| O | Activer ou retirer la marche |
| R | Recommencer avec les réglages sélectionnés |
| Souris | Orienter la caméra et régler sa distance |
| Échap | Quitter |

Le HUD compact reste à gauche et affiche les FPS observés ; la caméra suit la roue. Les repères jaunes
sur la jante et la carcasse permettent de distinguer leur rotation. Les
changements de charge, de gonflage et d’obstacle ne réinitialisent pas la roue.

## Ce que le banc démontre

La carcasse est un tore fermé de 192 sommets, avec contraintes d’étirement,
de cisaillement et de flexion, gonflé par pression. Ses 48 liaisons de talons
échangent des impulsions opposées avec la jante au même point. Chaque sommet
reste dynamique ; aucune attache cinématique ni téléportation ne le maintient
en place. Les contacts et les liaisons transmettent les efforts dans les deux
sens. Le moteur applique uniquement un couple à la jante ; aucune translation
n’est imposée au pneu.

La jante ne peut pas entrer directement en collision avec le sol ou la marche.
Un guide mécanique bloque le déplacement latéral et le basculement, tout en
laissant libres la montée, l’avance et la rotation de roue. Il ne fournit pas
de portance verticale. Sans carcasse, la jante tombe à travers le sol : ce cas
témoin fait partie des vérifications. Un second témoin sans liaison de talon
sous poussée latérale déjante, contrairement au montage lié. Le contrôleur
reste à 120 Hz, avec quatre micro-pas de couplage contenant chacun deux
sous-pas souples : le travail souple reste de huit sous-pas par pas du contrôleur.

Le profil cross démarre à 150 ; P passe à 50 (très bas), puis à 1500 (ferme).
Ces valeurs sont des coefficients du solveur, sans étalonnage en bars. La masse de jante s’ajoute à celle de
la carcasse ; ce réglage n’est pas la masse totale d’un véhicule.

## Vérifier sans fenêtre

Compiler depuis la même racine, puis passer les options à l’exécutable :

```sh
silex compile Silex-Examples/Sources/Physics3D/SoftTire/Main.sx --backend native --release -o /private/tmp/silex-soft-tire-demo
/private/tmp/silex-soft-tire-demo --check
```

`--check` vérifie la portance, la charge, le gonflage, le guidage sans appui
vertical, la transmission du couple et le franchissement, puis les commandes,
le remplacement explicite de la roue et les limites du HUD. Le roulage prolongé
combine vingt secondes de moteur, freinage, marche arrière, changement de
gonflage et de charge, avec contrôle des talons et du contact avec l’obstacle.
Il ne crée aucune fenêtre. `--controls-check` vérifie uniquement les commandes,
le reset, le maillage et le HUD ; `--bench` mesure une seconde simulée sans rendu. `--smoke` ouvre une fenêtre de test,
fait avancer la roue et se ferme après cinq secondes simulées. `--profile` mesure
les frames pendant douze secondes murales dans une fenêtre, puis imprime FPS
moyens, intervalle maximal et temps passé dans les pas physiques.
`--profile-four` ajoute trois roues physiques indépendantes dans cette même
fenêtre, avec une seule roue affichée, pour mesurer la charge de quatre
simulations en contexte graphique. Cela ne mesure pas le rendu de quatre roues.
`--fleet-bench` mesure sans fenêtre quatre roues complètes dans quatre mondes
indépendants. Ce coût ne comprend ni rendu, ni châssis partagé : il ne constitue
pas une mesure des FPS d’un monster truck.

Ce prototype expérimental qualifie une roue guidée contre des corps rigides.
Un monster truck complet demandera encore l’assemblage des roues au véhicule
et la qualification des charges, des virages et des vitesses visés. Les
contacts souple/souple et l’auto-collision restent à implémenter.
