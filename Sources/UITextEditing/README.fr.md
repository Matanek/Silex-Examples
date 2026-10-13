# Édition de texte et composition IME

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

Cliquez dans la ligne longue, glissez au-delà du bord gauche ou droit et gardez
le bouton appuyé sans bouger : texte et sélection continuent d’avancer.
Dans le texte multiligne, essayez aussi le haut, le bas et une diagonale, en
restant dans la fenêtre. Relâchez pour arrêter, remplacez la sélection puis
annulez pour retrouver le texte et la sélection.

Le binaire accepte `--cpu-check` : il exerce historique, mots, thèmes, sélection
maintenue, événements de composition IME et tailles 900/480/200/1 sans ouvrir
de fenêtre. Les tests Debug/Release qualifient ce mode ; l’essai IME natif reste
distinct. Les gestes tactiles sont décrits ci-dessous.

La police de repli embarquée affiche les idéogrammes et les emojis de la galerie,
ces derniers en monochrome. Les raccourcis alphabétiques suivent la disposition
logique du clavier, notamment Cmd+Z sur AZERTY. Le mode CPU vérifie aussi
l’absence de glyphes manquants dans le dessin réel et le trajet des événements.

Pour essayer l’IME réel sur macOS, activez une source de saisie japonaise ou
chinoise du système, cliquez un champ puis composez un mot. Le provisoire est
souligné ; le compteur de notifications ne change pas encore. Choisissez un
candidat et validez : le compteur augmente une fois et Cmd+Z annule tout le mot.
Composez à nouveau puis appuyez sur Échap : la valeur précédente et le focus
restent. Essayez aussi le texte multiligne et un champ défilé ; la fenêtre de
candidats doit suivre le caret visible. F2 conserve une composition en cours ;
changer de champ ou imposer une autre valeur avec F3 l’annule.

Pour essayer les poignées sur desktop, démarrez le binaire avec `--touch-simulation`
ou utilisez `F4`. Le libellé SIMULATION TACTILE confirme le mode : un clic place
le caret, un maintien sélectionne le mot, puis les bulles déplacent les
extrémités. Faire glisser le corps du champ défile ; maintenir une poignée hors
du bord prolonge la sélection. Échap annule le geste simulé. Les notifications
restent inchangées jusqu’à l’édition ; Cmd+Z conserve son rôle habituel.
Les événements `finger_*` d’un écran tactile sont également transmis, mais la
simulation souris et les tests CPU ne constituent pas une preuve matérielle.

La case « Défilement lissé », cochée au départ, applique le même suivi de molette
à la page et aux champs. « Transférer le scroll à la page » est décochée : la
molette ou le glissement restent dans le champ lorsqu’il atteint une limite.
Cocher la case autorise le transfert. Un champ sans débordement laisse passer
le geste. Comparer les deux options avec un geste lent, rapide puis inversé ;
les notifications et la sélection restent inchangées. Le contrôle CPU de la
vraie galerie couvre les mouvements intermédiaires, la limite et le transfert.
