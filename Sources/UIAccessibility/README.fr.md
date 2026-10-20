# Inspecter et actionner une session UI sur macOS

Cette démonstration interactive présente un champ **Nom**, le bouton **Valider**
et deux lignes de retour. La session se passe directement à Viewer : aucun
câblage d’accessibilité supplémentaire dans l’application.

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

Cet essai sert à qualifier le premier parcours AppKit ; il ne déclare pas les
autres contrôles ou les ponts Linux/Windows qualifiés.

Le mode `--cpu-check` vérifie le modèle et les actions sémantiques sans fenêtre.
Il ne vérifie ni l’arbre attaché à la vraie fenêtre, ni VoiceOver.
