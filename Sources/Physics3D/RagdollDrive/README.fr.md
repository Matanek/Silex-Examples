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
- **P** : impulsion sur l’avant-bras or ;
- **M** : arrêter ses moteurs, puis les reprendre vers la cible choisie ;
- **T** : choisir suspension ou sol et recréer les deux mannequins ;
- **Espace** : mettre en pause ou reprendre ;
- **R** : recréer les assemblages ; **Échap** : quitter.

Le changement de cible conserve les poses et vitesses ; seuls les moteurs
orientent progressivement les membres. Une nouvelle cible reprend les moteurs.
R et le changement de mode sont les seuls placements immédiats de cette démo.
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

Les options `--physics-check` et `--controls-check` valident le modèle et les
commandes sans fenêtre ; `--smoke` parcourt les changements de cible, impulsion,
arrêt, reprise, pause, reset et les deux modes dans une fenêtre qui se ferme
automatiquement.
Sur le binaire compilé, `--floor` démarre directement l’interactif au sol.
Un smoke terminé exige son marqueur final, pas seulement un code de sortie nul.
La cadence qu’il affiche constitue un échantillon local, sans comparaison FPS.
