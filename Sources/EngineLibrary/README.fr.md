# Moteurs validés via GFX.Audio

Cette démo consomme `GFX.Audio.Engines`. Le package possède le simulateur, les
profils, les réponses d’échappement, l’aspiration et les traitements de sortie.
La démo possède uniquement les entrées, le compte-tours et l’alimentation du flux.
Le banc `EngineAudio` reste autonome pour les comparaisons.

Préparer une bibliothèque avec les outils de GFX.Audio, puis depuis la racine du
workspace ou du groupe de Spec :

```sh
silex compile Silex-Examples/Sources/EngineLibrary/Main.sx --debug -o Build/EngineLibrary-Demo
Build/EngineLibrary-Demo /chemin/absolu/vers/EngineLibrary
```

**M** démarre ou coupe le moteur ; **Espace** maintenu donne des gaz. Le relâchement
et la perte de focus les ferment. Couper le contact n’attend pas l’arrêt moteur.
Changer de moteur exige le contact coupé et la rotation arrêtée. Les réglages
sont ceux du premier banc : maintien, charge, échappement, texture, ambiance et
volume. L’admission n’apparaît que pour le 450 4T qui fournit le débit d’aspiration.

Le son conserve le simulateur complet de référence, à 44,1 kHz stéréo. La lecture
reprend ses cinq blocs en file et au plus quatre calculs demandés en avance,
soit environ 98 ms hors sortie du périphérique. L’interface reçoit les blocs
prêts ; elle n’attend pas la simulation. La fermeture libère flux et moteur.
Aucun chemin sonore privé de la démo ou générateur par pièces n’est utilisé.

Contrôles sans fenêtre ni sortie sonore :

```sh
silex compile Silex-Examples/Sources/EngineLibrary/Check.sx --debug -o Build/EngineLibrary-Demo-Check
Build/EngineLibrary-Demo-Check /chemin/absolu/vers/EngineLibrary
silex compile Silex-Examples/Sources/EngineAudio/PackageParity.sx --release -o Build/EngineLibrary-Parity
Build/EngineLibrary-Parity /chemin/absolu/vers/EngineLibrary
```

Le comparateur emploie l’ancien banc comme oracle indépendant, avec son runtime
habituel sous `Build/EngineReference`. Il exige le PCM et le régime identiques
sur les huit profils et les changements de commandes. Ce runtime n’est pas une
dépendance de la nouvelle démo : seul le comparateur historique le nécessite.
La [documentation du package](../../../Packages/GFX.Audio/Docs/FR/Engines.md)
précise déploiement, API et limites de qualification.

La commande UI ci-dessus emploie Debug pour le contrôle local sous la garde de
4 Gio. Le simulateur reste construit en Release. La compilation Release complète
de la fenêtre dépasse cette garde sur le compilateur courant et reste à qualifier.
