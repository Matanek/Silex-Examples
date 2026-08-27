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
silex install HTML
silex install Plot
```

## Lancer une démonstration

Les fichiers directs se lancent depuis la racine du dépôt :

```sh
silex run Sources/AnalogClock.sx
silex run Sources/ApplicationWindow.sx
silex run Sources/DirectWindowInputLoop.sx
silex run Sources/DedicatedSystemTerminal.sx
silex run Sources/ComposedSystemTerminal.sx
silex run Sources/ApplicationCommandConsole.sx
silex run Sources/GeneratedHTMLWebView.sx
silex run Sources/BoidsSimulation.sx
silex run Sources/PlotGallery.sx
```

Les démonstrations multi-fichiers se lancent elles aussi depuis la racine :

```sh
silex run Sources/FallingBodies/Main.sx
silex run Sources/RotatingPhysicsContainer/Main.sx
silex run Sources/ShapeGallery2D/Main.sx
```

Leurs imports `Module.*` sont explicitement relatifs au dossier de chaque
source. Le manifeste déclare `"sources": "Sources"`, donc ce dossier physique
n'apparaît pas dans les noms de modules : `Sources/FallingBodies/Model.sx`
devient `FallingBodies.Model` et reste accessible par
`Package.FallingBodies.Model`. Il est également possible de se placer dans le
dossier d'une démonstration et de lancer `silex run Main.sx` : le manifeste
parent et ses dépendances restent actifs.

La galerie Plot présente plusieurs pages successives. Fermer la fenêtre
courante ouvre la page suivante.

Les exemples terminal forment une progression intentionnelle :
`DedicatedSystemTerminal.sx` possède une fenêtre dédiée et son cycle de vie,
`ComposedSystemTerminal.sx` intègre le shell dans une interface plus large, et
`ApplicationCommandConsole.sx` expose des commandes définies par l'application
sans donner accès au shell du système.

Les deux exemples WebView illustrent également deux approches différentes :
`EmbeddedWebView/Main.sx` embarque des fichiers web, tandis que
`GeneratedHTMLWebView.sx` construit et sérialise son document avec le package
`HTML` avant de l'afficher.

## Règle de synchronisation

Une démonstration promue ici devient une application appartenant à ce dépôt.
Elle peut diverger de l'exemple de package dont elle est issue. Les sources ne
sont pas recopiées automatiquement et aucune modification de ce dépôt ne doit
être répercutée aveuglément vers un package.

Le fichier [`CATALOG.md`](CATALOG.md) conserve la provenance de la sélection et
les autres candidats visuels repérés pendant l'inventaire.
