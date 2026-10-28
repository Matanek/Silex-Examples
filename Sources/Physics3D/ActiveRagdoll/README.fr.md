# L’atelier du pantin : premiers pas physiques

Un personnage mécanique à treize corps marche et tourne sur un sol quadrillé.
Les moteurs du tronc et des jambes visent les positions d’une marche ; les contacts
des pieds déplacent réellement le corps. Le rendu suit les corps physiques.

Depuis la racine du workspace ou du groupe Worktree de la Spec :

```sh
silex run Silex-Examples/Sources/Physics3D/ActiveRagdoll/Main.sx --release
```

- **ZQSD maintenus** : choisir une direction par rapport à la caméra ; le
  personnage tourne puis marche dans cette direction.
- **P**, ou **Pousser** : appliquer une impulsion au torse, sans changer la pose.
- **F** : relâcher/réactiver les moteurs et l’assistance d’équilibre.
- **R** : détruire et recréer le personnage. C’est la seule remise à zéro.
- **Échap** : fermer la fenêtre.

La caméra suit doucement le personnage. Le HUD reste sur la gauche et indique
les appuis chargés, la vitesse et le couple d’assistance. Les membres non voisins
peuvent se heurter ; hanches, genoux, chevilles, épaules et coudes ont des limites.
Les bras restent ballants : aucun moteur de pose ne commande les épaules et les
coudes. Les écrous et yeux sont des décorations attachées aux volumes physiques.
La silhouette reprend les références fournies : tête facettée mauve, capot et
mâchoire gris, yeux et mains en écrous clairs, gilet orange, taille en tige et
pieds clairs.

## Équilibre et marche

La trajectoire d’un pied distingue le retour levé et la poussée au sol. Le pied
parcourt 60 cm entre les extrémités avant et arrière de sa trajectoire cible,
avec un retour levé de 19 cm. Une cinématique inverse à deux segments calcule
les cibles de hanche et de genou.
Les moteurs articulaires ont des couples bornés ; aucune pose n’est imposée
pendant le déplacement.

L’équilibre est assisté par un moteur angulaire extérieur sur le bassin, borné
à 350 N·m par axe et actif avec un contact au sol. Les trois translations restent
libres :
aucun moteur ne soulève ni ne transporte le bassin. En mode passif, cette
assistance et les moteurs articulaires sont désactivés. En mode actif, une chute
déclenche une recherche d’appui alternée des jambes, puis leur extension lorsque
le bassin se redresse. Le personnage reprend la marche après stabilisation ;
il peut aussi faire des pas correctifs lorsque le centre de masse prédit dépasse
l’appui des pieds. F permet donc de le laisser tomber puis de le réactiver ;
aucun reset n’est nécessaire au relevage. R reste une recréation explicite.
Le couple extérieur aide réellement ce redressement : ce contrôleur n’est pas
un modèle d’équilibre humain autonome.

La simulation utilise un pas fixe à 120 Hz, 24 tours de vitesse et 32 passes de
position. Les géométries de rendu et le sol texturé sont créés une seule fois ;
les transformations sont interpolées entre deux pas physiques.

## Vérifier sans fenêtre

```sh
silex test Silex-Examples/Sources/Physics3D/ActiveRagdoll/Main.sx
silex test Silex-Examples/Sources/Physics3D/ActiveRagdoll/Qualification.sx
silex compile Silex-Examples/Sources/Physics3D/ActiveRagdoll/Main.sx --release -o .silex/active-ragdoll
.silex/active-ragdoll --controls-check
.silex/active-ragdoll --physics-check
```

Le contrôle de scène vérifie les touches logiques et les boutons du HUD,
l’impulsion, le mode passif, le reset, le cadrage et les transformations des
maillages, sans initialiser de fenêtre. Le contrôle physique couvre repos,
marche, virage, arrêt, efforts bornés, chute passive, relevage depuis quatre
directions, nouvelle marche, poussée en mode actif et destruction à 60/120 Hz. Les bras ne produisent aucun couple moteur.
Un contre-témoin sans friction vérifie que les moteurs internes et l’assistance
angulaire ne déplacent pas horizontalement le centre de masse total.

C’est le premier parcours d’une scène évolutive. La saisie, les charges, les
coups avec objets, l’escalade, les cordes et l’entrée dans les véhicules ne sont
pas encore présents. Cette scène ne remplace pas la qualification indépendante
du contrôleur capsule, ni une comparaison universelle de trajectoires avec Jolt.

Inspiration visuelle et principe du ragdoll actif :
[MetallCore999](https://www.youtube.com/@metallcore9993) et son
[exemple Unity](https://github.com/metallcore999/Projects). Le personnage et
la logique Silex sont propres à cette démo.
