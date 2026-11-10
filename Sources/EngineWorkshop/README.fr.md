# Façonner une signature sonore de véhicule

Choisir un véhicule, démarrer et maintenir **Espace** pour donner des gaz.
**M** ou le bouton bascule le contact. L’atelier utilise le générateur procédural
par pièces de GFX.Audio ; aucune banque d’enregistrements n’est nécessaire.

Depuis la racine `SilexProject/`, utiliser le package local puis construire :

```sh
silex link Packages/GFX.Audio --workspace Silex-Examples
silex compile Silex-Examples/Sources/EngineWorkshop/Main.sx --release -o Build/EngineWorkshop
Build/EngineWorkshop
```

## Choisir un véhicule

Le menu propose 17 profils :

- citadines essence 1,0 L trois cylindres, essence 1,4 L quatre cylindres et turbodiesel 1,6 L ;
- sportives I4 turbo 2,0 L, flat-six 3,2 L, V8 cross-plane 5,0 L, V10 5,2 L et V12 6,0 L ;
- motocross 125, 250 et 500 cm³ deux temps ; 250 et 500 cm³ quatre temps ;
- motos de course 1 000 cm³ quatre cylindres en ligne et V4 à allumages groupés ;
- custom et chopper bicylindres 1 200 et 1 800 cm³ à intervalles 315°/405°.

Les mentions GTI, 911, Mustang, R8, Ferrari et Harley sont des inspirations
sonores, pas des reproductions certifiées de modèles commerciaux. Les profils
et leur synthèse appartiennent à `GFX.Audio.Synthesis.EngineVehicles`.

## Entendre les réglages

La **cylindrée totale** se règle directement en cm³, sur une échelle logarithmique
50..12 000 ; elle conserve les proportions alésage/course et le rapport de
compression. Ce réglage ne représente pas le volume d’une chambre. Les limites
de dimensions du générateur restent applicables : un assemblage incompatible
est refusé avec un message et le son précédent est conservé.

**Échappement** ouvre ou assourdit le profil en combinant absorption et nombre
de chicanes. Zéro conserve son échappement d’origine. **Combustion** change
l’attaque ; **Admission** combine son niveau et son absorption ; **Mécanique**
règle son niveau ; **Fonctionnement** fait varier les combustions et légèrement
la rotation. Les changements attendent 120 ms sans mouvement, puis sont fondus
sur 50 ms. Modifier B pendant l’écoute de A revient à B.

L’accélérateur commande le régime cible ; l’effort le réduit et renforce le son
en charge. Le temps de réponse est propre au profil et réglable. Déplier
**Imposer le régime du banc** permet de fixer le régime indépendamment des gaz,
pour comparer un moteur à régime constant. L’indication de régime donne les
tr/min réels du banc ; le curseur du banc parcourt le ralenti jusqu’à la limite
du profil. Le volume d’écoute reste indépendant du timbre.

**Essai 8 secondes** joue ralenti, montée en régime, effort et relâchement.
L’essai conserve le moteur en marche. Une action sur les commandes du banc
interrompt l’essai ; une perte de focus relâche Espace.

**Mémoriser les réglages dans A** conserve la définition sonore B courante.
**Basculer A / B** compare les timbres au même régime et au même effort, sans
changer le temps de réponse. Les niveaux ne sont pas égalisés automatiquement.
Choisir une voie seule aide à localiser une différence ; le turbo reste muet
sur les profils qui n’en possèdent pas. Les dimensions de ligne et la compression
restent disponibles sous **Réglages avancés**.

## Exporter et vérifier

```sh
Build/EngineWorkshop --list
Build/EngineWorkshop --render Build/Cross250.wav --profile cross-250-2t
Build/EngineWorkshop --render Build/Vehicles.wav --catalogue
Build/EngineWorkshop --check
Build/EngineWorkshop --trace-audio
```

Chaque profil exporté dure 10 s : le même essai que dans l’interface, puis arrêt
et queue avec fondu final. `--catalogue` concatène les 17 essais dans l’ordre du
menu (170 s) et affiche les repères en secondes. Sans `--profile`, le rendu
choisit `city-i3`. L’export conserve le volume initial et les différences de
niveau ; il ne normalise pas les profils.

`--check` vérifie les 17 assemblages, cylindrées, échappements, comparaisons,
cycles d’essai, arrêts, refus, dessins à trois largeurs, curseur logarithmique
et sélection/démarrage au clavier sans fenêtre ni périphérique audio.
`--trace-audio` rapporte à la fermeture les observations de file vide et le plus
grand intervalle de mise à jour. La file reste bornée : blocs de 480 frames,
capacité de 4 800 à 48 kHz, soit au plus 110 ms préparés/en file hors périphérique.

Le modèle est acoustique et stylisé : chicanes filtrantes et résonance de détente
2T simplifiées, sans simulation des cônes, du balayage, de la puissance ou d’une
transmission routière. La qualité et la reconnaissance des profils restent à
qualifier par l’écoute. La [bibliothèque moteur validée](../EngineLibrary/README.fr.md)
reste un parcours distinct. `Measure.sx` conserve sa mesure du générateur V8
historique ; elle ne mesure pas le catalogue complet.
