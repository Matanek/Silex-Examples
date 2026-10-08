# Charnière avec charge hors du plan

Depuis la racine du workspace (ou celle du groupe Worktree de la Spec) :

```sh
silex run Silex-Examples/Sources/Physics3D/LoadedHinge/Main.sx --release
```

La scène démarre en pause. Le bras bleu pivote autour du support blanc ;
l’attache verte porte la charge jaune de 2 kg, décalée d’un mètre en profondeur.
La gravité et le sol font partie de la simulation.

- **Vers la droite**, puis **Vers la gauche** : le bras et la charge se
  déplacent nettement ensemble. Chaque bouton fixe une direction et reprend
  la simulation. Le message confirme la commande.
- **Lâcher le bras** : le moteur est retiré ; la gravité fait osciller le bras.
- **Charge derrière/devant le bras** : reconstruit la charge de l’autre côté
  du plan et remet la scène en pause. Choisir ensuite une direction.
- **Espace** ou le bouton **Pause/Reprendre** : arrête ou reprend les poses.
- **R** ou **Remettre à zéro** : revient à la pose verticale, en pause, en
  conservant le côté de la charge. **Échap** ferme la fenêtre.

L’angle, le couple moteur et les résidus affichés viennent des contraintes
physiques. Le moteur de cette vue vise ±0,65 rad avec un plafond de 40 N·m
pour rendre l’action visible sous gravité ; le témoin comparatif Jolt utilise
une vitesse et un plafond plus faible de 0,2 N·m. La caméra est fixe.

Contrôle sans fenêtre et smoke natif explicitement automatique :

```sh
silex compile Silex-Examples/Sources/Physics3D/LoadedHinge/Main.sx --release -o .silex/loaded-hinge
.silex/loaded-hinge --controls-check
.silex/loaded-hinge --smoke
```

Le contrôle synthétise de vrais événements UI et clavier, puis vérifie les
mutations, les déplacements et les poses rendues. Le smoke automatique
exerce les deux cibles, pause/reprise, le déport opposé et le lâcher, puis
ferme la fenêtre. Le lancement normal ne change aucune cible automatiquement.

La comparaison avec Jolt porte sur l’assemblage après convergence ; les
corrections initiales diffèrent. Cette scène ne qualifie pas une chaîne
quelconque ni une masse ou une commande arbitraires.
