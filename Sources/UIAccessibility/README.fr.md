# Inspecter et actionner une session UI sur macOS

Cette démonstration interactive présente un champ **Nom**, le bouton **Valider**
ainsi que des cases à cocher, un groupe **Profil**, un curseur **Volume** et un
panneau **Fichiers** avec un petit arbre. Des lignes affichent leurs valeurs.
La session se passe directement à Viewer : aucun câblage d’accessibilité
supplémentaire dans l’application.

Le bouton **Masquer les contours des cases et radios** permet de comparer le
contour par défaut et `FocusAppearance.none()`. Il agit sur les deux cases et
sur le groupe ; le slider conserve son réglage de focus habituel. La navigation
et l’activation restent disponibles. Le thème sombre fournit des libellés
clairs sur le fond du Viewer, et la page défile si la fenêtre est trop petite.

Depuis la racine du workspace, avec la toolchain de développement qui prend en
charge les méthodes de protocole avec corps :

```sh
silex run Silex-Examples/Sources/UIAccessibility/Main.sx --debug
```

Dans l’inspecteur d’accessibilité macOS, retrouver **Nom** avec son rôle de champ
et sa valeur **Ada**, puis **Valider** avec son rôle de bouton. Modifier le champ
ou actionner le bouton depuis l’outil doit changer les mêmes lignes de retour
que la souris ou le clavier. Avec VoiceOver, vérifier la lecture du nom et de
la valeur, le déplacement du focus, la saisie et l’activation. Déplacer ou
redimensionner la fenêtre permet de contrôler la géométrie exposée.

Le parcours bouton/champ a été confirmé avec l’inspecteur et VoiceOver. Pour
qualifier les nouveaux contrôles :

1. Activer **Notifications** : son état coché et le retour affiché changent.
2. Choisir **Énergique** dans **Profil** : une seule option est cochée ;
   **Indisponible** reste désactivée.
3. Ajuster **Volume** : valeur initiale 12, minimum 10, maximum 20 ; les actions
   d’incrément/décrément changent le même état que le glissement à la souris.
4. Cocher **Verrouiller le volume** : le curseur devient désactivé et refuse
   les modifications ; décocher rétablit son utilisation.
5. Réactiver **Notifications**, puis revenir au groupe et au curseur : les
   références restent utilisables après les réévaluations de l’interface.

Le panneau **Fichiers** contient **Documents** (deux enfants) et **Images**.
Déplier Documents, sélectionner Notes, puis replier et rouvrir le panneau permet
de comparer l’état visible et la source sémantique. Un client d’accessibilité peut aussi
modifier les attributs sélectionné/déplié lorsque les actions sont annoncées.
Le champ **Nom** référence son titre visible, qui le référence en retour.

Les tests sans fenêtre couvrent ces actions et le refus des actions désactivées.
Ils ne qualifient pas le parcours VoiceOver des nouveaux contrôles ni les ponts
Linux/Windows.

Le mode `--cpu-check` vérifie le modèle et les actions sémantiques sans fenêtre.
Il ne vérifie ni l’arbre attaché à la vraie fenêtre, ni VoiceOver.

## Inspecter une sélection Unicode

Le champ **Message Unicode** contient `Aé👩‍💻中Z` puis une deuxième ligne.
Sélectionner l’accent combiné, l’emoji ou plusieurs lignes permet de comparer
le surlignage et les propriétés de sélection exposées au système. Les index
natifs comptent des unités UTF-16 ; le toolkit conserve des graphèmes entiers.
Une saisie remplace la sélection et Cmd+Z restaure le texte sur macOS.

Le mode CPU vérifie cette édition et son annulation par les événements de
la session, après sélection par la source sémantique. Les tests AppKit séparés
vérifient la conversion native ; ce mode ne remplace pas l’inspection en fenêtre.

## Contrôler le placement de la présentation

Le mode `--placed` place une page adaptable avec une marge pour son décalage.
Son origine utilise `position:Math.Vec2(24.0, 16.0)` et `anchor:Math.Vec2(0.05)`. Dans une fenêtre de
780 × 820, son origine est donc à (63, 57) unités logiques ; le redimensionnement
la déplace avec l’ancre et adapte sa taille à la place disponible. Les éléments
restent décrits dans le repère du dessin.

Lancer le binaire avec `--placed`, cliquer dans Nom et Message Unicode puis
sélectionner du texte et faire défiler la page à la molette. Les cibles de souris
et le surlignage doivent suivre le contenu décalé. Dans l’inspecteur, le rectangle
d’un champ doit coïncider avec le contrôle, avant et après déplacement ou
redimensionnement de la fenêtre. Si une méthode de saisie affiche des candidats,
leur zone doit rester près du caret.

Le mode CPU vérifie aussi que la page et le champ restent dans la fenêtre sur
quatre dispositions successives, et que le titre est visible au démarrage.
Il ne prouve pas cette correspondance dans une vraie fenêtre.

## Inspecter les dimensions des collections

En bas de page, **Équipe** contient trois lignes et deux colonnes : **Personne**
et **Domaine**. L’inspecteur doit montrer ces dimensions sur le tableau, un
index sur chaque ligne, et les plages de ligne/colonne de longueur 1 sur ses
cellules. Les index commencent à 0. Cliquer une ligne actualise **Personne
sélectionnée** ; la sélection native utilise le même état.

Dans **Fichiers**, Documents et Images ont un niveau natif 0. Après dépliage,
Notes et Rapport ont un niveau 1. Leur position de ligne dans le modèle se
distingue de leur ordre parmi les enfants de Documents.

Les tests CPU vérifient les données et la sélection du tableau. Les tests
AppKit du package GFX vérifient les propriétés natives et leur lecture paresseuse
sur 50 000 lignes. La navigation complète des collections avec un lecteur
d’écran reste à qualifier.

Le tableau affiche un séparateur continu entre ses deux colonnes. La dernière
occupe l’espace disponible (`stretch_last_column:true`), sans fausse colonne
vide à droite. Les poignées se révèlent au survol ou au focus ; la séparation
reste visible dans les lignes. Le mode CPU vérifie les mêmes données et actions.

L’option `full_height_resize:true` est activée dans Équipe. Survoler puis glisser
le séparateur entre Personne et Domaine depuis une ligne, ou l’espace vide sous
les lignes, redimensionne la première colonne sans sélectionner de ligne.
La poignée et sa mise en évidence couvrent le corps ; la même poignée reste
accessible dans l’en-tête et au clavier. La valeur par défaut du toolkit reste
false pour conserver le choix d’une poignée limitée à l’en-tête.

L’inspecteur peut maintenant demander les lignes par `AXRows`, sans inclure
les en-têtes ni les conteneurs, et une cellule du tableau par ses coordonnées.
Les mêmes identités servent à la hiérarchie et à ces accès indexés. Le mode CPU
vérifie cette relation sur Équipe ; les tests AppKit vérifient sa traduction
native sans fenêtre. Ces preuves ne remplacent pas un parcours lecteur d’écran.

## Profil CPU des gestes

Le libellé du volume utilise directement `Text(volume, format:...)` : déplacer
le slider actualise ce texte sans reconstruire tout le formulaire. Les actions,
le verrouillage et la source accessible conservent les mêmes états.

[InteractionProfile.sx](InteractionProfile.sx) rejoue les gestes du slider et
d’une colonne sur ce même modèle, sans fenêtre. Il distingue entrées, dessin,
préparation Canvas et notifications accessibles, avec et sans observation de
l’arbre complet. Ses mesures concernent le CPU ; elles ne mesurent ni le GPU,
ni la présentation, ni les FPS de la fenêtre.

Le profil accepte `--bursts` pour comparer un et huit mouvements par dessin,
avec les requêtes de cible IME effectuées par l’hôte. Cette variante complète
le profil à une position par dessin ; les compteurs de layouts sont éprouvés
séparément dans les tests du toolkit.

`PresenterProfile.sx` rejoue séparément slider et défilement, avec et sans
observation de l’arbre accessible. Il chronomètre les entrées, la synchronisation
accessible avant dessin, le dessin, le remplacement du Canvas Scene2D et la
synchronisation après dessin, dans l’ordre de Viewer. Ce profil reste CPU et
n’ouvre ni fenêtre ni device GPU.

## Tracer la fenêtre réelle

La démo affiche les FPS dans le titre, en mode normal comme avec `--placed`,
avec ou sans trace. La moyenne de la boucle de rendu est actualisée au plus
deux fois par seconde ; elle inclut le temps réel des ralentissements longs.

L’option `--trace-drag` conserve en mémoire les 4 096 derniers passages dans la
boucle et écrit un CSV sur stdout après la fermeture de la fenêtre. Redirigez
stdout vers un fichier lors du lancement du binaire. Déplacez le slider puis
le séparateur, et fermez la fenêtre pour obtenir la trace.

`interval_ms` mesure le temps réel entre deux updates ; `delta_ms` est le delta
transmis par Viewer, borné à 100 ms par l’application. La trace compte les
événements et mesure handle, update, drawing et les requêtes IME. Le reste de
l’intervalle inclut rendu, accessibilité native, attente et ordonnancement ; il
ne représente pas un temps GPU isolé. La trace est optionnelle et ne change pas
la session utilisée par défaut.
