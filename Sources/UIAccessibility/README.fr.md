# Inspecter et actionner une session UI sur macOS

Cette démonstration interactive présente un champ **Nom**, le bouton **Valider**
ainsi que des cases à cocher, un groupe **Profil**, un curseur **Volume** et
leurs lignes de retour. La session se passe directement à Viewer : aucun
câblage d’accessibilité supplémentaire dans l’application.

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

Les tests sans fenêtre couvrent ces actions et le refus des actions désactivées.
Ils ne qualifient pas le parcours VoiceOver des nouveaux contrôles ni les ponts
Linux/Windows.

Le mode `--cpu-check` vérifie le modèle et les actions sémantiques sans fenêtre.
Il ne vérifie ni l’arbre attaché à la vraie fenêtre, ni VoiceOver.
