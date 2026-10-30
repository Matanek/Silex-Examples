# Tester un pneu souple

Une roue motorisée roule sur un sol plat et franchit une petite marche. Sa
carcasse déformable porte une jante dynamique : augmenter la charge permet
d’observer son écrasement, puis changer le gonflage modifie sa réponse.

Depuis la racine `SilexProject/`, avec le compilateur et les packages du workspace :

```sh
silex run Silex-Examples/Sources/Physics3D/SoftTire/Main.sx --release
```

Utiliser la version Release pour l’essai interactif. La version Debug sert aux
vérifications et son coût de simulation est beaucoup plus élevé.

| Commande | Action |
| --- | --- |
| Z / S maintenu | Moteur avant / arrière |
| Espace maintenu | Freiner la jante |
| C | Alterner la charge de jante : 20 / 50 kg |
| P | Alterner le gonflage : normal / souple / ferme |
| O | Activer ou retirer la marche |
| R | Recommencer avec les réglages sélectionnés |
| Souris | Orienter la caméra et régler sa distance |
| Échap | Quitter |

Le HUD compact reste à gauche ; la caméra suit la roue. Les repères jaunes
sur la jante et la carcasse permettent de distinguer leur rotation. Les
changements de charge, de gonflage et d’obstacle ne réinitialisent pas la roue.

## Ce que le banc démontre

La carcasse est un tore fermé de 192 sommets, avec contraintes d’étirement,
de cisaillement et de flexion, gonflé par pression. Ses contacts avec la jante
et le sol transmettent les efforts dans les deux sens. Le moteur applique
uniquement un couple à la jante ; aucune translation n’est imposée au pneu.

La jante ne peut pas entrer directement en collision avec le sol ou la marche.
Un guide mécanique bloque le déplacement latéral et le basculement, tout en
laissant libres la montée, l’avance et la rotation de roue. Il ne fournit pas
de portance verticale. Sans carcasse, la jante tombe à travers le sol : ce cas
témoin fait partie des vérifications.

Le gonflage emploie les coefficients 500, 1500 et 3000 du solveur. Ce ne sont
pas des pressions étalonnées en bars. La masse de jante s’ajoute à celle de
la carcasse ; ce réglage n’est pas la masse totale d’un véhicule.

## Vérifier sans fenêtre

Compiler depuis la même racine, puis passer les options à l’exécutable :

```sh
silex compile Silex-Examples/Sources/Physics3D/SoftTire/Main.sx --backend native --release -o /private/tmp/silex-soft-tire-demo
/private/tmp/silex-soft-tire-demo --check
```

`--check` vérifie la portance, la charge, le gonflage, le guidage sans appui
vertical, la transmission du couple et le franchissement, puis les commandes,
le remplacement explicite de la roue et les limites du HUD. Il ne crée aucune
fenêtre. `--controls-check` reprend uniquement cette dernière partie ; `--bench`
mesure une seconde simulée sans rendu. `--smoke` ouvre une fenêtre de test,
fait avancer la roue et se ferme après cinq secondes simulées.

Ce prototype expérimental qualifie une roue guidée contre des corps rigides.
Un monster truck complet demandera encore l’assemblage des roues au véhicule
et la qualification des charges, des virages et des vitesses visés. Les
contacts souple/souple et l’auto-collision restent à implémenter.
