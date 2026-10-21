# Monter, freiner et glisser sur une pente

Cette démo place une voiture de 100 kg sur une pente de 11,5°. Attendre sa
réception, puis appuyer sur **Z** : le moteur entraîne les quatre roues et la
voiture monte. **F** relâche les gaz et serre les freins ; la voiture ralentit
puis reste sur la pente. **X** libère à la fois les gaz et les freins.
Ces commandes restent actives après le relâchement de la touche.

**G** recrée le véhicule sans adhérence. La suspension porte toujours la
caisse, mais le véhicule glisse vers le bas, même avec les freins serrés.
Z fait tourner les roues sans arrêter cette glissade. Refaire G pour comparer
avec l’adhérence active. Le bouton indique toujours le choix courant.

Depuis la racine du workspace ou du groupe de Spec contenant cet exemple :

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleHill/Main.sx --release
```

## Commandes

| Touche | Action |
| --- | --- |
| Z | Gaz à 80 % dans le sens de la montée, freins libérés. |
| X | Roue libre : gaz et freins relâchés. |
| F | Gaz relâchés, quatre freins serrés. |
| G | Alterner avec/sans adhérence et recréer. |
| I | Inverser la pente et le rapport de boîte pour monter dans l’autre sens. |
| M | Comparer les suspensions souple et ferme. |
| T | Parcourir cylindre de 40 cm, rayon, sphère, puis cylindre. |
| R | Recréer au point de départ, freins serrés. |
| Espace | Suspendre ou reprendre la simulation. |
| Échap | Fermer la fenêtre. |

Les boutons reproduisent ces actions. G, I, M, T et R recréent le véhicule et
le sol, conservent les autres choix, serrent les freins et reprennent la
simulation. Attendre la réception avant Z. Une commande de conduite reprend
également une simulation suspendue. Les répétitions clavier sont ignorées.

La bande jaune indique l’avant de la caisse. I utilise la marche arrière pour
monter la pente opposée ; le sens positif des mesures reste la montée. La
caméra suit la voiture et le quadrillage métrique montre son déplacement.
Les barres cyan révèlent la rotation physique des roues, les traits blancs
suivent les longueurs des suspensions et les repères verts signalent les appuis.
Le panneau affiche vitesse, déplacement depuis l’origine, appuis, efforts,
hauteur normale au sol, régime et rapport.

## Réglages et périmètre

Le départ utilise des suspensions souples et des contacts cylindriques de
40 cm de largeur. Chaque roue a un rayon de 30 cm. Les rayons recherchent le
contact sur leur axe ; les sphères ont un rayon de recherche de 30 cm.
Le preset souple utilise 1 200 N/m et 160 N·s/m par roue, le ferme
10 000 N/m et 1 000 N·s/m. Leurs détentes maximales respectives de 77,985 et
60 cm compensent la différence de compression statique.

Un moteur de 40 N·m entraîne les quatre roues via une boîte manuelle à rapport
+1 ou −1 et deux différentiels de rapport 3, répartissant chacun la moitié du
couple. Les pneus utilisent ici un coefficient de friction constant de 1 ou 0,
sans résistance au roulement. Cette recette permet une comparaison Coulomb
bornée avec Jolt ; elle ne qualifie pas les courbes variables, d’autres terrains
ou un modèle complet de conduite. Le plan physique possède la même normale
que la route visible. Toutes les poses et réactions proviennent de la simulation.

La simulation avance à 120 Hz. Le rendu interpole poses, débattements et angles
de roues. Les meshes sont partagés et créés au démarrage ; la grille se recentre
par tranches de cinq mètres. Le panneau change sur commande ou au plus à 10 Hz.
Les repères de contact proviennent du début du pas physique et peuvent être
légèrement décalés de la pose interpolée pendant une réception.

L’exemple [VehicleSuspension](../VehicleSuspension/README.fr.md) reste disponible
pour les virages, l’anti-roulis, les obstacles et le basculement.

## Vérifications

Depuis la même racine :

```sh
silex test Silex-Examples/Sources/Physics3D/VehicleHill/Model.sx
silex compile Silex-Examples/Sources/Physics3D/VehicleHill/Main.sx --release -o .silex/vehicle-hill
.silex/vehicle-hill --physics-check
.silex/vehicle-hill --controls-check
.silex/vehicle-hill --smoke
```

Le contrôle physique couvre 48 configurations à 60/120 Hz : deux pentes,
trois détecteurs, deux suspensions et adhérence active/nulle. Il contrôle la
montée, le freinage, les appuis, la hauteur et le poids normal moyens ainsi que
la glissade sous gravité. Il vérifie aussi la recréation et les anciens handles.
Le contrôle des commandes exerce touches logiques, majuscules, fallback physique,
répétitions, vrais clics, pause et conservation des choix, sans fenêtre.

Le parcours **TEST AUTOMATIQUE** exécute quatre essais de huit secondes
physiques : souple adhérent, souple sans adhérence, pente opposée adhérente,
puis ferme. Il vérifie les transforms rendus de la caisse et des roues, la
route, le cadrage, la pause et la recréation. Attendre sa fermeture normale.
L’essai interactif sert à apprécier la lisibilité de la pente et la sensation
de montée, de freinage et de glissade.
