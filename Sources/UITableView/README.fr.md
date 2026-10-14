# Tableaux de données

La galerie montre 50 000 lignes à clés stables, tri, largeurs, sélection et édition.
Depuis la racine du workspace ou du groupe de Spec :

```sh
silex run Silex-Examples/Sources/UITableView/Main.sx --release
```

- Cliquer un en-tête alterne croissant, décroissant et ordre initial ; Groupe et Score montrent des valeurs égales avec tri stable.
- Glisser le bord droit d’un en-tête change sa largeur. Tab rejoint aussi les poignées ; Gauche/Droite, Maj et Début/Fin règlent leur largeur.
- Sélectionner puis trier : la même clé reste sélectionnée et sa nouvelle position est révélée.
- Essayer filtre, retrait/ajout 100 et état vide, puis restaurer 50 000 lignes. La sélection absente reste applicative.
- « Révéler 100 » rejoint la cellule Nom éditable. Le thème conserve l’édition et les largeurs.
- Réduire la fenêtre pour vérifier le rail horizontal : en-têtes et cellules restent alignés, rail vertical accessible à droite.
- Le scroll est lissé et isolé aux limites. Le toolkit permet aussi le transfert ; la galerie conserve l’isolation souhaitée.

Les compteurs décrivent le travail réalisé, sans mesure de FPS. Le chemin CPU
vérifie les grandes collections, tri, largeurs, filtrage, clavier et petits viewports :

```sh
silex run Silex-Examples/Sources/UITableView/Main.sx --release -- --cpu-check
```

Ce chemin ne crée aucune fenêtre. Les gestes normalisés disposent de preuves CPU
séparées ; aucun nouveau matériel tactile n’est qualifié ici.
