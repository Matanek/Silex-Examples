# Suivre une pose et relâcher les membres

Au départ, les deux mannequins sont suspendus par leur torse fixe. Le bleu
maintient une pose neutre. L’or démarre sans moteurs : ses membres retombent
et oscillent sous gravité. P applique une impulsion de 6 N·s sur l’avant-bras. M ou une cible active le maintien motorisé ; M le relâche ensuite.
T recrée les deux mannequins avec un torse mobile et un sol physique ; T à
nouveau revient à la suspension. Les limites anatomiques et collisions internes
non voisines restent actives.

Depuis la racine du workspace ou du groupe de Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/RagdollDrive/Main.sx --release
```

Utiliser les boutons ou les touches :

- **1 / 2 / 0** : pose ouverte, repliée ou neutre pour l’or ;
- **3** : demander des coudes et genoux au-delà de leurs butées ;
- **P** : impulsion sur l’avant-bras or ;
- **B** : lancer un bloc rouge vers ce bras et observer son choc physique ;
- **M** : arrêter ses moteurs, puis les reprendre vers la cible choisie ;
- **T** : choisir suspension ou sol et recréer les deux mannequins ;
- **Espace** : mettre en pause ou reprendre ;
- **R** : recréer les assemblages ; **Échap** : quitter.

La demande **3** conserve les épaules et hanches de la cible ouverte, mais
demande −2,8 rad aux coudes et 2,8 rad aux genoux. Leurs limites restent
−2,35 et 2,4 rad : les articulations bornent le geste et les contacts peuvent
le bloquer avant la butée. Le panneau indique quatre demandes hors limites
quand leurs moteurs sont actifs. Une cible excessive ne force aucun membre.

Le bloc vole puis transmet son choc par contact : B ne change aucune pose
ou vitesse du mannequin lors du tir. Le compteur d’impacts augmente seulement
après un contact mesuré avec l’or. Un seul bloc est actif ; un nouveau tir
le remplace, et il disparaît après environ trois secondes. R et T le retirent.
B reprend la simulation après une pause ; Espace fige aussi le projectile.

Le changement de cible conserve les poses et vitesses ; seuls les moteurs
orientent progressivement les membres. Une nouvelle cible reprend les moteurs.
R et le changement de mode sont les seuls placements immédiats des mannequins.
Le torse fixe permet
l’observation des articulations sans chute de l’ensemble : il ne démontre ni
l’équilibre debout ni une commande de déplacement mondial. Dans le mode sol,
les moteurs agissent sur des membres en contact et les torses restent entièrement
mobiles : une cible n’est pas une pose imposée, et le contact peut empêcher
son suivi exact. R recrée le mode courant. Le parcours voisin
[RagdollFall](../RagdollFall/README.fr.md) conserve la chute libre et les impacts.

La simulation utilise 120 Hz et 32 passes de correction, avec interpolation au
rendu. Les moteurs ont un budget de 120 N·m par axe, une raideur de 400 N·m/rad
et un amortissement de 8 N·m·s/rad pour l’or, 40 pour le bleu.
Le maintien de l’or laisse une réaction oscillante à l’impulsion au lieu de
l’amortir presque immédiatement. Leurs cibles changent aux commandes ; la
mesure et l’interface sont actualisées à 10 Hz ou après une action effective.
Les observations géométriques détaillées sont réservées aux tests et au smoke.

Sur le binaire compilé, `--projectile-check` qualifie sans fenêtre le tir,
le contact et la réaction à 60/120 Hz dans les deux supports, avec moteurs
actifs ou libres. Ce parcours compare aussi un mannequin témoin sans bloc.

Les options `--physics-check` et `--controls-check` valident le modèle et les
commandes sans fenêtre ; `--smoke` parcourt les changements de cible, impulsion,
arrêt, reprise, pause, reset, puis deux vols/impacts de bloc dans les deux
modes, avec rendu interpolé et visibilité vérifiés dans une fenêtre qui se ferme
automatiquement.
Sur le binaire compilé, `--floor` démarre directement l’interactif au sol,
et `--limits` sélectionne la demande excessive sans placer les membres.
`--limits-check` isole sa recette sans fenêtre ; `--physics-check` l’inclut
avec les parcours précédents. Le smoke contrôle cette demande puis les tirs
de bloc dans les deux modes.
Un smoke terminé exige son marqueur final, pas seulement un code de sortie nul.
La cadence qu’il affiche constitue un échantillon local, sans comparaison FPS.
