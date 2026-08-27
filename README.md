# Silex Examples

`Silex-Examples` rassemble les démonstrations visuelles que l'on veut pouvoir
retrouver et lancer sans parcourir les dépôts de chaque package. Ce dépôt est
un catalogue d'applications autonomes : les exemples techniques et les preuves
d'API restent auprès de leur package propriétaire.

## Parcours

- [`Showcases/`](Showcases/) : galeries visuelles et tours de fonctionnalités ;
- [`Applications/`](Applications/) : petites applications complètes ;
- [`Interactive/`](Interactive/) : simulations et scènes orientées jeu.

Un showcase privilégie la variété et l'impact visuel d'une capacité. Une
application accomplit une tâche cohérente que l'utilisateur pourrait reprendre
comme point de départ. Une expérience interactive met en avant une boucle de
simulation, des contrôles ou un comportement proche d'un jeu.

Les thèmes techniques forment le second niveau de l'arborescence. Chaque
parcours possède son propre `Package.json` et ne dépend donc pas des packages
utilisés seulement par un autre parcours.

## Préparer les packages publiés

```sh
silex install GFX --suite
silex install GFX.Physics
silex install GFX.UI --suite
silex install GFX.WebView
silex install Plot
```

## Lancer une démonstration

Depuis la racine du dépôt :

```sh
silex run Showcases/Canvas/ShapeGallery.sx
silex run Applications/Terminal/QuickStart.sx
silex run Interactive/Physics2D/RotatingContainer.sx
silex run Interactive/Scene2D/Boids.sx
silex run Interactive/Scene3D/World.sx
silex run Showcases/Charts/Gallery.sx
```

La galerie Plot présente plusieurs pages successives. Fermer la fenêtre
courante ouvre la page suivante.

## Règle de synchronisation

Une démonstration promue ici devient une application appartenant à ce dépôt.
Elle peut diverger de l'exemple de package dont elle est issue. Les sources ne
sont pas recopiées automatiquement et aucune modification de ce dépôt ne doit
être répercutée aveuglément vers un package.

Le fichier [`CATALOG.md`](CATALOG.md) conserve la provenance de la sélection et
les autres candidats visuels repérés pendant l'inventaire.
