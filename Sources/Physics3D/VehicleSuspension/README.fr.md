# Piloter une voiture RC ou un Monster truck

La voiture démarre avec une forte accélération, quatre roues motrices, des
suspensions souples, des balayages sphériques et des flancs de pneus solides.
Le panneau de 280 × 360 pixels laisse le texte prendre sa hauteur réelle et
reste à gauche pour dégager la voiture et le terrain. Le quadrillage mesure
des mètres ; la caméra suit le déplacement et reste orientable à la souris.

Depuis `/Users/nekmata/Projects/SilexProject` :

```sh
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release
```

## Conduire

- Maintenir **Z** pour accélérer ; relâcher pour rouler sur l’élan.
- Maintenir **S** pour freiner, puis reculer après ralentissement. Depuis la
  marche arrière, Z freine avant de repartir vers l’avant.
- Maintenir **Q / D** pour tourner à gauche/droite relativement au véhicule.
  Le braquage se recentre au relâchement et diminue avec la vitesse.
  Les lettres suivent le clavier logique : ZQSD sur AZERTY.
- Maintenir **Espace** pour bloquer les roues arrière. En virage, l’arrière
  dérive sous les efforts des pneus ; relâcher pour retrouver la motricité.
  Les roues avant restent entraînées si Z est maintenu.
- **R** repart au départ avec le profil choisi et libère les commandes.
- **Échap** quitte. La perte de focus relâche les touches ; Espace ne met plus
  la simulation en pause.

## Changer de profil et essayer le terrain

**N** alterne voiture RC et Monster truck. Le rayon physique des roues passe
de 32 à 65 cm ; leur voie, leur inertie et le débattement changent également.
Les roues dessinées reprennent ces dimensions réelles. La masse reste de 100 kg,
avec les collisions continues du châssis activées et un centre de masse bas pour freiner sans faire systématiquement un tonneau.
Le moteur de 180 N·m entraîne deux différentiels et trois rapports automatiques,
avec des passages courts. Le profil RC atteint environ 33–34 km/h après une
seconde d’accélération dans les essais à 60/120 Hz ; le Monster environ 39–40.
Ces réglages sont ludiques et ne représentent pas un véhicule réel calibré.

Le terrain contient huit obstacles fixes : un petit tremplin devant le départ,
un tremplin plus haut dans son prolongement, un plan incliné latéral,
trois marches de l’autre côté, une traverse basse et une rampe plus raide.
Leurs formes et poses physiques sont aussi utilisées par le rendu. Les essais
vérifient le passage des marches avec le Monster, l’envol et la reprise des
appuis sur le parcours des rampes. Les manœuvres excessives peuvent retourner
le véhicule ; R permet de repartir.

Les boutons du panneau et leurs touches permettent aussi de comparer :

- **M** : suspension souple/ferme.
- **T** : contacts sphère, cylindre large, cylindre étroit, rayon, puis sphère.
- **A** : barres anti-roulis.
- **L** : limite d’inclinaison totale de 60° ou mode libre.

Ces changements recréent le véhicule au départ et relâchent les commandes ;
le terrain reste en place. **O** donne une impulsion de basculement, **B** un
bond, **C** une surcharge de deux secondes. **G** reste un raccourci de diagnostic
pour couper/rétablir l’adhérence en recréant le véhicule. Le moteur ne force ni pose, ni vitesse de caisse,
ni angle de dérive. Le frein arrière de 4000 N·m par roue et l’adhérence combinée
partagent réellement le budget d’efforts longitudinal/latéral.

Les flancs des roues heurtent le sol pendant un retournement, avec leur
largeur réelle, même lorsque la suspension ne peut pas porter l’appui.
Cette enveloppe latérale reste active avec chacun des quatre balayages. Sur le
dos, les roues se détendent sans attraper de faux appuis dans le sol.
Le châssis repose sur sa collision ; le défaut d’alternance comprimée/détendue
des contacts cylindriques est couvert par une régression du SDK.

## Vérifier sans fenêtre

```sh
silex test Silex-Examples/Sources/Physics3D/VehicleSuspension/DrivingChecks.sx
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/DrivingChecks.sx --release
silex run Silex-Examples/Sources/Physics3D/VehicleSuspension/Main.sx --release -- --controls-check
```

Les contrôles couvrent accélération, freinage avant inversion, blocage arrière
et dérive miroir, gros pneus sur obstacles, sauts/réceptions, roues retournées,
entrées maintenues/relâchées, focus, répétition, boutons, dimensions du rendu et
bornes du HUD et hauteur réelle de chaque texte après les actions visibles.
Les anciens témoins physiques restent disponibles avec
`--physics-check` ; ils conservent leurs configurations historiques. Le mode
`--smoke` est un test graphique automatique qui ouvre une fenêtre et se ferme
à la fin ; il reste distinct du parcours interactif.
