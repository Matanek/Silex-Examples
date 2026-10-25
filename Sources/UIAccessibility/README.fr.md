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
