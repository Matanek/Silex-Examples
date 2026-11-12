# AudioEngineSimulator

## Presets d’EngineWorkshop

La fenêtre principale réunit les neuf presets d’EngineWorkshop, la coupe de
profil et la vue des cylindres de dessus. Les pistons des deux vues sont
animés à partir du régime du moteur. La clé, le compte-tours et la pédale
sont regroupés à côté des vues, ou en dessous dans une fenêtre étroite.

Cliquer sur la clé ou appuyer sur **M** pour mettre ou couper le contact.
Maintenir **Espace** pour donner plein gaz ou doser l’ouverture avec le
curseur **Accélérateur**. Le bouton **Essai 8 secondes** rejoue le scénario
d’EngineWorkshop. Couper le contact et attendre l’arrêt pour changer de moteur.

`--check-references` vérifie les vues et les commandes et compare le son,
le régime et le démarreur des neuf presets à ceux d’EngineWorkshop.
`--render-reference <id> <wav>` exporte le même essai en WAV stéréo à 44,1 kHz.

## Simulateur de pièces

Lancer le binaire avec `--procedural` pour configurer les pièces et les équipements.

La fenêtre s’ouvre sur un V8 4T générique. À gauche, choisir une disposition
en ligne ou en V, le nombre de cylindres, puis la cylindrée totale au curseur.
La plage dépend du nombre de cylindres et va de 50 cm³ pour un monocylindre
à 48 L pour un V16. Le nouveau moteur attend la remise du contact. Les
pistons, les bielles et le compte-tours suivent le simulateur qui produit le son.
Cliquer sur la clé ou appuyer sur **M** pour la tourner de 11 h à 13 h et
mettre le contact. Maintenir **Espace** pour enfoncer la pédale. Cliquer
sur le bouton compact ou appuyer sur **T** pour choisir **Hard** (0,15 s) ou
**Soft** (1 s). La jauge suit l’enfoncement. Le remplissage du moteur suit
la pédale avec un court retard. Relâcher Espace ramène la pédale au repos
en 0,3 s et augmente le frein moteur. Rétrécir la fenêtre
pour voir les deux panneaux se réagencer en conservant leurs proportions.
La vue de dessus se trouve sous la coupe. La clé, le compte-tours et
la pédale sont regroupés à droite et passent sous les vues en format étroit.

Sous la configuration du moteur, **Mixage** règle l’aspiration et la
combustion de 0 à 100 % pendant la lecture. Les niveaux initiaux sont
20 % et 100 %. Pour isoler une piste, ramener l’autre à 0 %. Les niveaux
restent en place quand on change de moteur.

Le panneau **Échappement** permet de changer de silencieux et de montage
pendant que le moteur tourne. **Tube libre** réduit l’absorption et retire
les chicanes. **Chicanes** amortit davantage la sortie. **Commune** regroupe
les cylindres, **Deux longueurs** envoie les impulsions dans des conduits
de longueurs différentes et **Une dominante** atténue la seconde sortie.
**Origine** rappelle les paramètres
de l’assemblage pour la ligne concernée.

**Réglages techniques** ouvre l’éditeur de mécanique, de phases d’allumage
et d’échappement. Pour affecter un cylindre, saisir le numéro de sortie à
partir de 1. Avec zéro sortie configurée, la sortie 1 utilise une résonance
commune. Les nombres acceptent la virgule ou le point. **Appliquer** revient
au banc et une modification du moteur demande de remettre le contact.
Dans **Mécanique**, **Rupteur (tr/min)** fixe le seuil et **Coupure (ms)**
règle le délai de reprise après le dépassement. Le compte-tours adapte
son échelle au seuil choisi.

**Chevrolet 454** charge les valeurs d’un V8 7,44 L, consultables dans l’éditeur.
Pour le reconstruire, partir de **En V** et **8 cylindres** puis saisir les
valeurs du [preset](EngineConfig.sx). Changer la disposition, le nombre de
cylindres ou la cylindrée au curseur repart des valeurs génériques.

Les assemblages utilisent un modèle 4T à allumage commandé et des calages
génériques. La cylindrée marine sert à explorer des tailles de moteur.

Depuis la racine du workspace où `GFX.Audio` fournit `EngineSimulation` :

```sh
mkdir -p Build
silex compile Silex-Examples/Sources/AudioEngineSimulator/Main.sx --debug -o Build/AudioEngineSimulator-Window
Build/AudioEngineSimulator-Window
```

## Export hors ligne

`--render-454 <préfixe>` produit le mix et les trois pistes du preset,
avec un ralenti à 850 tr/min, une montée jusqu’à 2 600 tr/min, un palier
et une retombée. La trace CSV indique le régime et les commandes.

L’export rend un monocylindre 4T et une variante à deux cylindres déphasés
de 180°.

```sh
mkdir -p Build/AudioEngineSimulator-Audio
Build/AudioEngineSimulator-Window --render Build/AudioEngineSimulator-Audio/moteur
```

Dans les pistes `mono` et `bi`, le démarreur s’enclenche à 0,25 s et le
contact est mis à 0,95 s. Les gaz montent à partir de 2,20 s, se ferment à
4,70 s et le contact est coupé à 5,30 s. Le banc laisse la charge appliquée
pendant le ralentissement. Écouter le mix puis le frottement, l’aspiration et
la combustion isolés.

Les exports `frottement-reference` et `frottement-double` rejouent deux
secondes à 1 500 tr/min, allumage coupé. Seul le coefficient de frottement
passe de 0,08 à 0,16. Les WAV sont mono à 48 kHz et gardent les niveaux du
rendu. Les CSV consignent les commandes et l’état de chaque cylindre toutes
les 240 frames audio, avec la frame exacte du dernier allumage.
