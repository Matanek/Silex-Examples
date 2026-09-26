# Platformer2D — Pixel Trail

Un petit parcours en pixel art : déplacer le personnage vert, sauter les deux
fossés, explorer les plateformes et atteindre le drapeau. Les dix pièces sont
optionnelles. Une chute ramène au départ en conservant les pièces ; `R`
recommence entièrement la partie.

Depuis la racine du workspace `SilexProject/`, avec ses packages locaux liés :

```sh
silex run Silex-Examples/Sources/Platformer2D/Main.sx
```

- Flèches gauche/droite ou touches physiques Q/D sur AZERTY, A/D sur QWERTY.
- Espace : sauter ; relâcher tôt pour réduire la hauteur.
- R : recommencer ; Échap : quitter.

La fenêtre fixe de 960 × 540 affiche des pixels agrandis trois fois, avec une
caméra qui suit le personnage. Les atlas PNG sont intégrés à la compilation ;
le binaire fonctionne indépendamment de son dossier de lancement.

## Ce que l'exemple utilise

- `Nodes.TileMap2D` pour les couches solides et décoratives.
- `Scene2D.TilePatch` pour répéter neuf tuiles sans étirer les coins.
- `Physics.TileMapCollider2D` pour fusionner les cellules en rectangles et
  produire un seul corps par carte. Le Node l'active par `collision_enabled`.
- `Nodes.CharacterBody2D` pour les déplacements et les contacts à 120 Hz.
- `Nodes.Sprite2D`, `Camera2D` et `Canvas2D` pour les animations, la caméra et le HUD.

La gravité, le contrôle du personnage, la tolérance au bord des plateformes et
la courte mémorisation du bouton de saut sont des règles de jeu dans `Player.sx`.
Les pièces et le drapeau utilisent des tests de proximité, sans corps physiques.
Le rendu de terrain, sa préparation retenue, son culling, ses instances GPU et
les collisions fusionnées appartiennent aux packages, accessibles aussi en ECS.

## Tuiles Kenney employées

L'atlas terrain contient 20 colonnes, avec des cellules de 18 × 18 pixels.
Les indices sont ceux du fichier packed, à partir de zéro :

| Motif | Haut | Centre | Bas |
| --- | --- | --- | --- |
| Terre/herbe | 21, 22, 23 | 121, 122, 123 | 141, 142, 143 |
| Panneau vert contigu 3 × 3 | 17, 18, 19 | 37, 38, 39 | 57, 58, 59 |

Les pièces alternent 151/152 ; le drapeau 111/112 avec un pied 109.
Le personnage utilise les deux premières cellules de 24 × 24 de l'atlas de
personnages. Les lignes de la grille montent dans le monde ; `TilePatch`
place donc les morceaux supérieurs sur la ligne la plus élevée.

Assets : Kenney, **Pixel Platformer 1.2**, CC0. Le pack original et sa licence
sont conservés dans `../../Assets/KenneyPixelPlatformer/`.

## Vérifier

Toujours depuis la racine du workspace :

```sh
silex test Silex-Examples/Sources/Platformer2D/Tests/Gameplay.sx
silex compile Silex-Examples/Sources/Platformer2D/Main.sx -o /tmp/silex-platformer2d
/tmp/silex-platformer2d --verify
```

Le test de gameplay parcourt le niveau à pas fixe et vérifie l'arrivée. Le mode
`--verify` exécute douze frames dans une fenêtre masquée, vérifie le nombre de
corps et les bornes de dessins/instances, puis quitte. Il ne remplace pas une
vérification visuelle et manuelle du contrôle du personnage.

Cette première tranche n'inclut pas de pentes, de plateformes à sens unique,
d'ennemis ou de sons. L'édition d'une cellule reconstruit actuellement les
collisions de toute sa carte ; les très grands niveaux éditables demanderont
une invalidation par zones. Les différentes couches conservent leur ordre de
dessin : une couche visible non vide produit un dessin de terrain instancié.
