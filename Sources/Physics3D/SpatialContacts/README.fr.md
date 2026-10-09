# Abaisser une charge jusqu’au plan puis la relever

La sphère or de 2 kg est portée par deux charnières perpendiculaires.
Le bras bleu reste tenu. Cet essai manuel sert à vérifier que le plan,
l’arrêt de la descente et la libération du contact se comprennent visuellement.
Les bilans mécaniques sont déjà qualifiés par les tests du package Physics.

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/SpatialContacts/Main.sx --release
```

La scène démarre en pause, sans changement automatique de cible.

- **Abaisser jusqu’au plan** reprend la simulation et fait descendre la charge.
  Au premier contact, la commande freine le moteur et retient l’angle atteint.
  Le message **CONTACT ATTEINT** confirme cet arrêt. Le petit repère vert est
  affiché au point de contact mesuré tant que le contact existe.
- **Lever la charge** reprend la simulation et remonte la sphère. Le message
  passe à **CHARGE LIBRE** et le repère vert disparaît.
- **Freiner** interrompt le déplacement et retient l’angle courant.
- **Espace** ou **Pause/Reprendre** arrête/reprend la simulation.
- **R** ou **Remettre à zéro** revient à la pose horizontale en pause.
  **Échap** ferme la fenêtre.

Le numéro de commande confirme immédiatement l’action ; les angles et l’état
se mettent à jour dix fois par seconde. Le déplacement prend quelques secondes.
La caméra est fixe. Le plan physique infini est à Y=1,58 m ; la plaque affichée
en représente la zone utile. Rayon de sphère 0,15 m, déport 0,8 m, masses
2/2 kg, inerties isotropes 0,4/0,2 kg·m², capacités moteur 60/40 N·m.
Seule la sphère heurte le plan, sans friction ni restitution.

L’arrêt au premier contact fait partie de la commande : elle ne maintient pas
une cible inaccessible en poussant indéfiniment. Le guide `SpatialContacts3D`
de Physics documente la qualification bornée avec Jolt ; cette scène ajoute
l’interaction et le rendu, sans revendiquer une qualification du contact forcé
prolongé ou d’une chaîne arbitraire.

Contrôle sans fenêtre et smoke graphique automatique :

```sh
silex compile Silex-Examples/Sources/Physics3D/SpatialContacts/Main.sx --release -o .silex/spatial-contacts
.silex/spatial-contacts --controls-check
.silex/spatial-contacts --smoke
```

Le contrôle synthétise de vrais clics et événements clavier, puis vérifie
l’arrêt au contact, sa tenue, le relèvement, les poses affichées, le freinage,
la pause et le reset. Le smoke suit deux passages au contact et se ferme seul.
