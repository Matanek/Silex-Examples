# Silex Examples

`Silex-Examples` rassemble les démonstrations visuelles que l'on veut pouvoir
retrouver et lancer sans parcourir les dépôts de chaque package. Ce dépôt est
un catalogue d'applications autonomes : les exemples techniques et les preuves
d'API restent auprès de leur package propriétaire.

## Organisation

Toutes les démonstrations vivent sous [`Sources/`](Sources/). Elles ne sont ni
classées par package, ni rangées dans une catégorie subjective comme
« showcase », « application » ou « interactif ». Leur nom exprime directement
ce qu'elles montrent.

Une démonstration autonome et compacte reste un fichier direct :

```text
Sources/AnalogClock.sx
Sources/BoidsSimulation.sx
```

Une démonstration volumineuse ou composée de plusieurs fichiers reçoit un
dossier et un point d'entrée `Main.sx` :

```text
Sources/FallingBodies/Main.sx
Sources/EmbeddedWebView/Main.sx
Sources/EmbeddedWebView/Web/...
```

Un unique [`Package.json`](Package.json) décrit le graphe nécessaire au
catalogue complet.

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
silex run Sources/AnalogClock.sx
silex run Sources/TerminalWindow.sx
silex run Sources/FallingBodies/Main.sx
silex run Sources/BoidsSimulation.sx
silex run Sources/World3D/Main.sx
silex run Sources/PlotGallery.sx
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
