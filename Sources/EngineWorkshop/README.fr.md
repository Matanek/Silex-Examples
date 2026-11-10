# Écouter et adapter les moteurs de référence

Pour qualifier un cross depuis l’enregistrement YZ250 fourni, utiliser le
[prototype d’écoute YZ250](../YZ250/README.fr.md). Ce prototype est isolé du
catalogue ci-dessous et conserve les parcours 454 et cross 500 4T.

EngineWorkshop utilise `GFX.Audio.Engines.Vehicles` et le simulateur thermique
d’EngineLibrary. Le Chevrolet 454 est le profil initial : sa définition,
ses réponses d’échappement et son
traitement sont conservés. Le générateur simplifié par impulsions n’est plus
utilisé dans cette démo.

Les citadines essence portent maintenant le libellé **extérieur feutré** et le
diesel **voix TDI hybride**. Ces mentions et le titre « citadines et TDI hybride »
identifient la version avec les corrections de timbre. Le diesel ajoute de
courtes excitations tirées de la référence audio TDI ; leur cadence suit le
régime simulé. Il ne rejoue pas le montage entier et son modèle enregistré
n’est pas identifié. Le rendu extérieur des essences reste plus discret que
celui des sportives au même volume.

Depuis la racine `SilexProject/` :

```sh
silex link Packages/GFX.Audio --workspace Silex-Examples
silex compile Silex-Examples/Sources/EngineWorkshop/Main.sx --debug -o Build/EngineWorkshop
Build/EngineWorkshop
```

Le simulateur embarqué reste construit en Release. Debug concerne ici le
programme Silex de l’interface, comme pour EngineLibrary. La banque native
est actuellement disponible sur macOS ARM64.

## Choisir et écouter

**M** ou le bouton démarre/coupe le contact. **Espace** maintenu donne des gaz,
y compris après un clic sur un bouton ; Entrée active le contrôle focalisé.
La perte de focus relâche Espace. Le régime affiché provient du simulateur.
Le curseur d’accélérateur fournit une pédale continue et la charge sollicite
le banc. À 800 tr/min, le maintien laisse le ralenti libre ; au-dessus, il
maintient la rotation gaz relâchés selon le comportement du banc de référence.

La pédale des customs 1 200/1 800, du V8 américain et de la citadine I4 répartit
la faible ouverture utile à vide sur les premiers 90 % du curseur. Les derniers
10 % rejoignent l’ouverture totale ; **Espace** donne toujours les pleins gaz.
Cela permet de doser la montée avant le limiteur sans imposer un régime ni
changer la mécanique. La commande du 454 et de la cross 500 4T est conservée.
Ce banc tourne sans transmission routière. Cette correction de commande ne
qualifie pas le timbre des profils.

Le menu contient 18 entrées :

- Chevrolet 454 d’origine ; citadines essence trois/quatre cylindres et diesel prototype ;
- sportives I4, flat-six, V8 sur base GM LS, V10 sur base LFA et V12 sur base Ferrari 412 T2 ;
- motocross 125/250/500 deux temps et 250/500 quatre temps ;
- motos de course I4 sur base Hayabusa et V4 à allumages groupés ;
- custom/chopper 1 200/1 800 sur base Harley.

Changer de profil ou appliquer une cylindrée demande contact coupé et rotation
arrêtée. La cylindrée concerne le moteur complet, en cm³ ; elle modifie ses
dimensions et chambres, avec adaptation mécanique des monos. La référence
454 conserve sa géométrie ; choisir le V8 américain pour une cylindrée modifiable.
Un refus conserve le moteur en place. Le détail des modèles et de leurs limites
appartient au [guide Vehicles](../../../Packages/GFX.Audio/Docs/FR/Vehicles.md).

## Comparer les traitements

**Texture** agit sur le souffle et les variations du synthétiseur natif.
**Échappement** mélange signal brut et réponse filtrée : 100 % conserve la
réponse de référence. Ce réglage ne simule pas des chicanes. **Ambiance** ajoute
le traitement spatial existant ; le volume reste indépendant. L’admission est
proposée seulement pour les monos 4T qui fournissent le débit d’aspiration.

**Mémoriser B dans A** et **Basculer A / B** comparent ces réglages d’écoute sur
le même moteur en fonctionnement. Ils ne remplacent ni sa géométrie ni ses
commandes de conduite. Modifier un traitement revient à B. **Essai 8 secondes**
joue démarrage, gaz progressifs, charge et relâchement, puis laisse le contact
allumé. Une commande de conduite interrompt cet essai.

## Exporter et vérifier

```sh
Build/EngineWorkshop --list
Build/EngineWorkshop --render Build/Chevrolet454.wav
Build/EngineWorkshop --render Build/Cross250.wav --profile cross-250-2t
Build/EngineWorkshop --render Build/Vehicles.wav --catalogue
Build/EngineWorkshop --check
Build/EngineWorkshop --trace-audio
```

L’export produit les réglages initiaux du profil choisi, à 44 100 Hz stéréo.
Chaque clip dure 10 s : l’essai, puis la coupure et une queue avec fondu final.
Le catalogue concatène les 18 clips (180 s) et affiche les repères. Les niveaux
ne sont pas normalisés et l’export ne reprend pas les réglages d’une fenêtre
interactive existante.

`--check` compare le PCM du 454 à EngineLibrary sur démarrage, accélération,
charge et coupure, puis vérifie A/B, gardes de changement, clavier, curseur
logarithmique et dessins à trois largeurs, sans périphérique. Il mesure aussi
la progression du régime à 25/50/75 % sur les quatre pédales calibrées et vérifie
l’accès aux pleins gaz. Le test consommateur
GFX.Audio exerce les 18 définitions et la pédale continue. Le flux interactif
reste borné à cinq blocs de sortie et quatre calculs de 480 frames, environ
98 ms hors périphérique ; l’interface consomme les blocs prêts sans attendre
le calcul. `--trace-audio` rapporte les observations de file vide et l’intervalle
maximal entre mises à jour, pas un historique des ruptures du périphérique.

La mécanique diesel reste une approximation à allumage commandé, sans injection
ni auto-inflammation ; sa voix enregistrée ne change pas ce modèle physique.
L’I4 de sportive ne simule pas de turbo. Le 2T conserve les
lumières et le balayage simplifiés du simulateur, sans pot de détente à cônes.
Ces limites sont visibles pour les profils concernés. Les variantes demandent
une qualification à l’écoute ; la parité du 454 protège la référence sonore.
`Measure.sx` concerne toujours le prototype par pièces, pas cette chaîne native.
