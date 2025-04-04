# OpenPyWorld
# RPG en Python – Projet de Développement d'un Jeu RPG en Programmation Orientée Objet

Ce projet est réalisé dans le cadre d’un projet d’étude de l'EPSI par Simon Godard et Maxime Mansiet. Il s’agit d’un jeu de rôle (RPG) développé en Python en utilisant la programmation orientée objet. Le jeu propose une aventure interactive dans le Royaume d'Eldoria, avec des animations, des combats, un système d'inventaire et de progression du personnage.

---

## Table des Matières

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Installation et Pré-requis](#installation-et-prérequis)
- [Utilisation](#utilisation)
  - [Lancement du Jeu](#lancement-du-jeu)
  - [Création et Connexion d'un Joueur](#création-et-connexion-dun-joueur)
  - [Exploration et Combat](#exploration-et-combat)
- [Structure du Projet](#structure-du-projet)
- [Animations et Effets Visuels](#animations-et-effets-visuels)
- [Crédits](#crédits)

---

## Présentation

Ce jeu RPG vous plonge dans une aventure dans le Royaume d'Eldoria. Le joueur incarne un personnage choisi parmi plusieurs types (Fée, Magicien, Elfe, Gobelin, Valkyrie) et doit explorer diverses zones – de la Montagne de l'Enfer au Château de Wamp – en affrontant des ennemis, en collectant des objets et en progressant grâce à l'accumulation d'XP et au système de niveaux.

---

## Fonctionnalités

- **Interface Console Améliorée :** Utilisation de la bibliothèque [Rich](https://github.com/willmcgugan/rich) pour des animations, des affichages colorés et une expérience utilisateur enrichie.
- **Animations :** Animations de transitions, d’XP gain et d’affichage d’ASCII art animé.
- **Système de Combat :** Combat interactif avec gestion des attaques, parades et utilisation d’objets.
- **Progression du Joueur :** Système de niveaux, XP, et amélioration des statistiques (attaque, défense, santé).
- **Gestion d’Inventaire :** Ajout et utilisation d’objets avec effets temporaires.
- **Sauvegarde des Données :** Les informations du joueur sont enregistrées dans un fichier texte, permettant la persistance des données entre les sessions.
- **Exploration de Régions :** Diverses zones à explorer, chacune avec ses propres défis et événements interactifs.

---

## Installation et Pré-requis

Pour exécuter ce projet, vous devez disposer de Python (version 3.7 ou supérieure est recommandée) et installer les dépendances suivantes :

1. **Rich** pour l'affichage console :
   ```bash
   pip install rich
   ```
2. **bcrypt** pour le hachage des mots de passe :
   ```bash
   pip install bcrypt
   ```

Assurez-vous également que tous les fichiers du projet (comme `main.py`, `animation.py`, `menu.py`, `map.py`, `player.py`, etc.) se trouvent dans le même répertoire ou que les chemins d'importation soient correctement configurés.

---

## Utilisation

### Lancement du Jeu

Pour démarrer le jeu, exécutez simplement le fichier `main.py` :

```bash
python main.py
```

Au lancement, le jeu affiche une animation d’ASCII art (avec un dégradé de couleurs) qui introduit l’univers du RPG.

### Création et Connexion d'un Joueur

- **Créer un Joueur :**  
  Sélectionnez l’option « Créer un joueur » dans le menu principal. Vous serez invité à entrer un nom d’utilisateur, un mot de passe et à choisir le type de personnage.
  
- **Connexion :**  
  Pour vous connecter, choisissez l’option « Connexion » et entrez vos identifiants. Après une connexion réussie, une animation violette vous confirmera la réussite.

### Exploration et Combat

Une fois connecté, vous accéderez au menu d’exploration. Vous pouvez :
- **Explorer des zones** (Montagne de l'Enfer, Vaisseau Amiral, Parc MCD, Forêt MariaDB, Château de Wamp) en naviguant sur la carte.
- **Affronter des ennemis** lors de combats interactifs.
- **Utiliser votre inventaire** pour améliorer vos statistiques ou bénéficier d’effets pendant les combats.
- **Gérer votre compte** pour modifier votre nom d’utilisateur ou votre mot de passe.

Les actions en jeu sont choisies via des menus interactifs et des invites de commande.

---

## Structure du Projet

Le projet est organisé en plusieurs fichiers pour une meilleure modularité :

- **main.py :** Point d’entrée du jeu qui gère le menu principal, les animations d’introduction et la navigation vers les différentes fonctionnalités.
- **animation.py :** Contient toutes les fonctions d’animation (affichage d’ASCII art animé, transitions d’écran, animation de gain d’XP, etc.).
- **menu.py :** Gère la création, la connexion des joueurs et l’affichage du classement.
- **map.py :** Contient la définition de la carte du royaume et la logique d’exploration des différentes zones.
- **player.py et character.py :** Définissent les classes du joueur et les types de personnages.
- **enemy.py :** Contient la classe des ennemis et la logique de combat.

---

## Animations et Effets Visuels

Le projet utilise la bibliothèque Rich pour animer l’interface :
- **Animation de démarrage :** Un dégradé de couleurs pour l’affichage de l’ASCII art du jeu.
- **Animation de combat :** Animation d’attaque affichant des symboles (⚔️, 🔥, 💥, ✨) pour représenter l’action.
- **Animation de gain d’XP :** Progression animée pour montrer l’accumulation d’expérience.
- **Transitions d’écran :** Effets de transition (barres de progression, etc.) lors du passage entre les écrans du jeu.

Ces animations améliorent l’immersion et rendent l’expérience utilisateur plus dynamique.

---

## Crédits

Ce projet a été développé par **Simon Godard** et **Maxime Mansiet** dans le cadre de leurs études en informatique.  
Pour toute question ou suggestion, n’hésitez pas à contacter les auteurs du projet.
