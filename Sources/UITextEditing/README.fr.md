# Historique et navigation de texte

La galerie compose un champ court, une ligne longue et un texte multiligne.
Elle utilise les bindings, identités et viewports de GFX.UI sans gestionnaire
applicatif d’historique.

Depuis la racine du workspace ou du groupe de Spec :

```sh
silex run Silex-Examples/Sources/UITextEditing/Main.sx --release
```

Cliquez un champ et tapez plusieurs caractères. Cmd/Ctrl+Z annule la frappe
contiguë ; Maj+Cmd/Ctrl+Z ou Ctrl+Y la rétablit. Déplacez le caret avant de taper
à nouveau pour commencer une autre unité. Sélectionnez du texte avant de le
remplacer, puis annulez : la sélection est restaurée avec sa direction.

Option/Ctrl+flèches parcourt les mots ; ajouter Maj les sélectionne.
Option/Ctrl+Retour arrière ou Suppr efface jusqu’à la frontière correspondante.
Les accents combinés et emoji restent entiers. Ponctuation et espaces Unicode
suivent le parcours décrit dans [GFX.UI](../../../Packages/GFX.UI/Docs/FR/Text-Editing.md).

F2 ou le bouton de thème conserve l’historique. F3 ou « Valeurs initiales » impose
les valeurs d’origine : les historiques dont la valeur change sont réinitialisés.
La ligne longue et le texte multiligne révèlent le caret après édition, navigation
et undo/redo. Redimensionnez la fenêtre pour vérifier les mêmes gestes.

Le binaire accepte `--cpu-check` : il exerce historique, mots, thèmes et tailles
900/480/200/1 sans ouvrir de fenêtre. Les tests Debug/Release qualifient ce mode ;
l’essai graphique reste distinct. IME, tactile et sélection pointeur maintenue
hors champ ne sont pas démontrés ici.
