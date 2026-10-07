# Sept articulations 3D en manuel

Depuis la racine du workspace, avec le candidat Physics local disponible :

```sh
silex run Silex-Examples/Sources/Physics3D/Articulations/Main.sx --release
```

La fenêtre démarre en pause. Précédente / Suivante choisit un mécanisme et
remet sa pose à zéro. Son bouton d’action démarre ou inverse le mouvement,
affiche un compteur et reprend même depuis la pause. Espace et le bouton
Pause / Reprendre partagent le même traitement. R et Remettre à zéro restaurent
le mécanisme sélectionné en pause. Échap ferme ; la répétition clavier est ignorée.

| Mécanisme | Action visible |
|---|---|
| Cône | Une barre pivote vers l’une des deux limites vertes. |
| Swing / twist | La barre change d’inclinaison et de rotation sur son axe. |
| Six degrés | La barre se déplace à gauche/droite et tourne sur son axe. |
| Engrenage | Deux rotors guidés tournent en sens opposés avec un rapport 2:1. |
| Crémaillère | Un pignon guidé entraîne une barre horizontale. |
| Poulie | Les masses guidées montent et descendent en conservant le câble. |
| Chemin | Un chariot orienté suit une boucle Hermite et inverse son sens. |

Le doré désigne le corps commandé, le bleu le second corps. Le vert montre
limites, guides, câble ou chemin. Les mesures donnent course, angle, longueur
du câble ou erreur de phase. Les commandes sont exclusivement manuelles.

Cette démonstration ciblée utilise une gravité nulle et des collisions
filtrées. Des charnières et glissières retiennent les axes de l’engrenage,
de la crémaillère et des masses de la poulie. Elle ne qualifie pas les chaînes
spatiales chargées, le contact des dents ou une machine complète. Physics
simule à 120 Hz ; Scene3D affiche les poses interpolées. Les pools visuels
sont alloués au démarrage puis réutilisés. Deux poses de corps sont interpolées par frame ; au plus 24 dents décoratives
suivent ces mêmes poses pour l’engrenage ou la crémaillère. Les mesures sont rafraîchies à
10 Hz et le dessin UI seulement lorsqu’un état change.

Le binaire accepte `--controls-check` sans fenêtre : événements de clics et
de touches, mutations, mouvements, pause et remise à zéro des sept familles.
`--smoke` ouvre un scénario automatique explicitement nommé, sans boutons,
vérifie limites, poses affichées, pause et inversion, puis ferme à la fin.
La lisibilité visuelle et les entrées clavier natives se vérifient séparément
dans le mode manuel par défaut.
