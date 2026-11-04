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
et la perte de focus les ferment. Espace reste réservé aux gaz après un clic
sur un bouton ; Entrée active le contrôle focalisé. Couper le contact n’attend pas l’arrêt moteur.
Le passage Libre/Route est possible dès le contact coupé, sans attendre le
ralentissement ; il réinitialise le banc. Changer de profil moteur exige encore
la rotation et le véhicule arrêtés. Les réglages
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

## Boîte de vitesses optionnelle

Cocher **Mode Route · boîte de vitesses** après avoir coupé le contact. La boîte
commence en automatique. **A** bascule auto/manuelle ; **↑ / ↓** ou les boutons
+/− demandent un rapport, **N** le point mort, **S** maintenu freine. Le cadran
montre mode, rapport et vitesse, ainsi que les refus de rétrogradage pour surrégime.
Le contact peut être coupé en roulant. Une demande refusée ne s’engage pas plus tard
sans commande nouvelle ; après N en roulant, + permet d’atteindre un rapport sûr.

Décocher Route revient au banc libre dès le contact coupé, même si le moteur ou
le véhicule ralentissent encore ; le nouveau contexte repart à l’arrêt. Le régime
de maintien et la charge ne sont affichés qu’en mode libre, où ils ont un effet. La transmission
et sa télémétrie viennent de `GFX.Audio.Engines`, pas d’un calcul privé de la démo.

Les boutons indiquent l’action suivante : **Démarrer** ou **Arrêter**, **Passer
en manuel** ou **Passer en automatique**. Le libellé de la case Route utilise
la couleur claire du panneau.

En Route, ouvrir **Régler la démultiplication** pour préparer le rapport de pont
et chaque rapport de boîte. Une valeur numérique plus élevée raccourcit le
rapport ; à vitesse identique, le moteur tourne plus vite. Les rapports doivent
décroître de la première à la dernière. **Appliquer la démultiplication** ne
prend effet que moteur et véhicule arrêtés ; les gestes sur ces sliders ne
modifient pas la simulation avant l’application. **Rapports d’origine** rétablit
la boîte du profil. Changer de profil retrouve aussi ses valeurs d’origine.
La démo conserve le nombre de rapports du profil ; l’API permet des boîtes
personnalisées de 1 à 12 rapports. Préparer une banque v2 pour ce parcours.

Les rapports d’origine sont conservés par défaut. Un rapport plus long ne
garantit pas une accélération plus forte : couple moteur et traînée du véhicule
interviennent aussi.
