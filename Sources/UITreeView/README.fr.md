# Explorer une hiérarchie avec TreeView

La galerie compare 50 000 feuilles dans vingt dossiers et une branche de
200 niveaux. Les flèches ouvrent ou referment les branches ; cliquer une ligne
sélectionne sa clé. La feuille 1000 est un champ éditable.

Depuis la racine SilexProject :

```sh
silex run Silex-Examples/Sources/UITreeView/Main.sx --release
```

Essayer Haut/Bas, Gauche/Droite, Début/Fin et Page précédente/suivante après Tab
ou un clic. La sélection garde ses clés quand les branches se replient ; le
curseur rejoint un ancêtre visible. La case active la sélection multiple,
avec Maj+Haut/Bas pour étendre une plage.

Les boutons filtrent les dossiers, inversent leurs enfants, retirent/réajoutent
la feuille 1000, ouvrent/replient les branches et vident/restaurent l’arbre.
« 200 niveaux » révèle la dernière ligne ; l’indentation est plafonnée pour
préserver le libellé. « Clair / sombre » conserve ouverture et navigation.
Le compteur montre les descriptions de lignes construites, pas des FPS.
La molette est lissée ; les champs et l’arbre isolent leur scroll débordant.

L’index des données est construit au remplacement de source. Seules les lignes
nécessaires au viewport deviennent des vues. Les états applicatifs conservent
la valeur éditée même si sa ligne sort du viewport ; un éditeur retiré perd le
focus. Le modèle `Hierarchy` conserve l’instant des paramètres utilisé par ses
callbacks, selon les règles de durée de vie de Silex.

Sur le binaire compilé, `--cpu-check` vérifie sans fenêtre les grands arbres,
le scroll, le repli, les mutations, les tailles étroites et l’absence de nouvelles
descriptions au repos. Les tests du vrai exemple ajoutent les événements clavier
GFX et le changement de thème. Un marqueur `UITreeView CPU : OK` et un code 0
confirment ce parcours ; ils ne remplacent pas l’essai visuel utilisateur.
