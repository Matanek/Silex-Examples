# Observer le premier freinage d’une charnière

Depuis la racine `SilexProject/` ou le groupe `Worktree/` de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/HingeImpact/Main.sx --release
```

La scène commence en pause. Cliquer **Vers le repère haut**, attendre l’arrêt,
puis **Vers le repère bas**. La pointe rouge passe entre les deux repères verts.
En **Rotation libre**, le bouton donne une vitesse de ±1 rad/s puis laisse
l’axe sans moteur. **Avec moteur** sélectionne une commande de position ;
cliquer ensuite un sens pour rejoindre la butée et inverser le mouvement.
Choisir un mode met en pause ; la commande de sens reprend la simulation.

La lecture est ralentie à ×0,25, avec une physique à 120 Hz. Le panneau conserve
la vitesse avant/après le premier freinage de chaque commande et son angle,
puis affiche l’état et le couple actuels. Les limites valent ±0,3 rad (±17,2°).
Le moteur demande ±0,8 rad, cible effective bornée aux limites, avec 10 N·m,
raideur 1,6 et amortissement 0,08. La rotation positive suit la règle de la main
droite ; les boutons désignent le repère vert haut ou bas de la vue initiale.

**Espace** et le bouton Pause suspendent/reprennent. **R** et Remettre à zéro
recréent la scène au centre, en rotation libre et en pause. **Échap** ferme.
Les répétitions automatiques des touches sont ignorées. Aucun T, M ou I caché.

Les repères verts visualisent la limite de charnière ; ce ne sont pas des
contacts. Le solveur peut freiner avant l’angle limite, selon la distance
restante sur un pas. On vérifie l’impulsion et le mouvement ; on ne promet
pas une vitesse transitoire identique à celle de Jolt.

Pour les contrôles sans fenêtre, compiler l’exemple et passer `--controls-check`
à l’exécutable. `--smoke` ouvre une fenêtre automatique, vérifie les deux modes,
les inversions, pause/reprise, bilan d’impulsion et poses affichées, puis ferme.
