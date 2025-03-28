import os

# Définition de la classe Joueur
class Joueur:
    def __init__(self, pseudo, type_personnage, mot_de_passe):
        self.pseudo = pseudo
        self.type_personnage = type_personnage
        self.mot_de_passe = mot_de_passe
        self.attaque = type_personnage.attaque
        self.sante = type_personnage.sante
        self.defense = type_personnage.defense
        self.xp = 0
        self.niveau = 1

    def mettre_a_jour_statistiques(self, nouvelle_attaque, nouvelle_sante, nouvelle_defense):
        self.attaque = nouvelle_attaque
        self.sante = nouvelle_sante
        self.defense = nouvelle_defense

    def monter_de_niveau(self):
        self.niveau += 1
        print("Niveau supérieur ! Vous êtes maintenant niveau " + str(self.niveau))
        self.sauvegarder_dans_fichier()

    def calculer_niveau(self):
        return self.niveau * 100
    
    def gagner_xp(self, quantite):
        self.xp += quantite
        while self.xp >= self.calculer_niveau():
            self.monter_de_niveau()
        self.sauvegarder_dans_fichier()

    def sauvegarder_dans_fichier(self):
        with open("joueurs.txt", "r") as fichier:
            lignes = fichier.readlines()

        with open("joueurs.txt", "w") as fichier:
            for ligne in lignes:
                if self.pseudo in ligne:
                    ligne = f"{self.pseudo} {self.mot_de_passe} {self.type_personnage.nom} {self.attaque} {self.sante} {self.defense} {self.niveau} {self.xp}\n"
                fichier.write(ligne)

# Définition de la classe TypePersonnage
class TypePersonnage:
    def __init__(self, nom, attaque, sante, defense):
        self.nom = nom
        self.attaque = attaque
        self.sante = sante
        self.defense = defense

# Définition des types de personnages
fee = TypePersonnage("Fée", 100, 1150, 100)
magicien = TypePersonnage("Magicien", 275, 900, 175)
elfe = TypePersonnage("Elfe", 200, 1000, 150)
gobelin = TypePersonnage("Gobelin", 125, 1000, 225)
valkyrie = TypePersonnage("Valkyrie", 250, 850, 250)

# Fonction de création de joueur
def creer_joueur():
    while True:
        pseudo = input("Entrez votre pseudo : ")
        mot_de_passe = input("Entrez votre mot de passe : ")

        utilisateur_existe = False
        if os.path.exists("joueurs.txt"):
            with open("joueurs.txt", "r") as fichier:
                for ligne in fichier:
                    if pseudo in ligne:
                        print("Ce pseudo est déjà pris. Veuillez en choisir un autre.")
                        utilisateur_existe = True
                        break

        if not utilisateur_existe:
            while True:
                print("Choisissez votre type de personnage :")
                print("1. Fée\n2. Magicien\n3. Elfe\n4. Gobelin\n5. Valkyrie")
                choix = input()
                if choix == "1":
                    joueur = Joueur(pseudo, fee, mot_de_passe)
                elif choix == "2":
                    joueur = Joueur(pseudo, magicien, mot_de_passe)
                elif choix == "3":
                    joueur = Joueur(pseudo, elfe, mot_de_passe)
                elif choix == "4":
                    joueur = Joueur(pseudo, gobelin, mot_de_passe)
                elif choix == "5":
                    joueur = Joueur(pseudo, valkyrie, mot_de_passe)
                break
            
            if not os.path.exists("joueurs.txt"):
                with open("joueurs.txt", "w") as f:
                    f.write("Pseudo MotDePasse TypePersonnage Attaque Santé Défense Niveau XP\n")

            with open("joueurs.txt", "a") as f:
                f.write(f"{joueur.pseudo} {joueur.mot_de_passe} {joueur.type_personnage.nom} {joueur.attaque} {joueur.sante} {joueur.defense} {joueur.niveau} {joueur.xp}\n")
                print("Joueur créé avec succès !")
                break

# Connexion
def connexion():
    while True:
        pseudo = input("Entrez votre pseudo : ")
        mot_de_passe = input("Entrez votre mot de passe : ")
        joueur_trouve = False
        utilisateur = None

        with open("joueurs.txt", "r") as fichier:
            for ligne in fichier:
                champs = ligne.split()
                if len(champs) == 8:
                    pseudo_enregistre, mdp_enregistre = champs[0], champs[1]
                    if pseudo == pseudo_enregistre and mot_de_passe == mdp_enregistre:
                        joueur_trouve = True
                        type_perso = TypePersonnage(champs[2], int(champs[3]), int(champs[4]), int(champs[5]))
                        utilisateur = Joueur(pseudo_enregistre, type_perso, mdp_enregistre)

        if not joueur_trouve:
            print("Pseudo ou mot de passe incorrect. Veuillez réessayer.")
        else:
            return utilisateur

# Fonction d'exploration
def explorer_region(joueur):
    regions = {
        "0": "Retour au menu principal",
        "1": "Caverne Cristalline",
        "2": "Jardins Scintillants",
        "3": "Forêt des Fées",
        "4": "Montagnes Mystiques",
        "5": "Marais des Secrets"
    }

    while True:
        print("\nCarte :")
        for cle, valeur in regions.items():
            print(f"{cle}. {valeur}")
        choix = input("Sélectionnez un lieu à explorer : ")

        if choix == "0":
            break
        elif choix in regions:
            print(f"Vous explorez {regions[choix]}...")
        else:
            print("Choix invalide. Veuillez sélectionner une option valide.")

# Programme principal
if __name__ == "__main__":
    while True:
        print("1. Créer un joueur\n2. Se connecter\n3. Quitter")
        choix = input("Sélectionnez une option : ")
        if choix == "1":
            creer_joueur()
        elif choix == "2":
            joueur = connexion()
            explorer_region(joueur)
        elif choix == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez sélectionner une option valide.")
