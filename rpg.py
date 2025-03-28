import os
from rich import print

ascii_art = r"""
   ___                   ____      __        __         _     _ 
  / _ \ _ __   ___ _ __ |  _ \ _   \ \      / /__  _ __| | __| |
 | | | | '_ \ / _ \ '_ \| |_) | | | \ \ /\ / / _ \| '__| |/ _` |
 | |_| | |_) |  __/ | | |  __/| |_| |\ V  V / (_) | |  | | (_| |
  \___/| .__/ \___|_| |_|_|    \__, | \_/\_/ \___/|_|  |_|\__,_|
       |_|                     |___/                            
"""

# Définit la classe Joueur
class Player:
    def __init__(self, ign, character_type, password):
        self.ign = ign
        self.character_type = character_type
        self.password = password
        self.attack = character_type.attack
        self.health = character_type.health
        self.defense = character_type.defense
        self.xp = 0
        self.level = 1

    def update_player_stats(self, new_attack, new_health, new_defense):
        self.attack = new_attack
        self.health = new_health
        self.defense = new_defense

    def is_alive(self):
        return self.health > 0

    def show_healthbar(self):
        print(
            f"[{"❤️" * self.health}{"♡" * (self.max_hp - self.health)}] {self.hp}/{self.max_hp} hp")

    def level_up(self):
        self.level += 1
        print("Niveau supérieur ! Vous êtes maintenant au niveau " + str(self.level))
        self.save_to_file() 

    def calculate_level(self):
        return self.level * 100
    
    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.calculate_level():
            self.level_up()
        self.save_to_file()
            
    def save_to_file(self):
        with open("players.txt", "r") as file:
            lines = file.readlines()

        with open("players.txt", "w") as file:
            for line in lines:
                if self.ign in line:
                    line = f"{self.ign} {self.password} {self.character_type.name} {self.attack} {self.health} {self.defense} {self.level} {self.xp}\n"
                file.write(line)

# Définit la classe TypePersonnage
class CharacterType:
    def __init__(self, name, attack, health, defense):
        self.name = name
        self.attack = attack
        self.health = health
        self.defense = defense

# Définit les différents types de personnages
fairy = CharacterType("Fée", 100, 1150, 100)
wizard = CharacterType("Magicien", 275, 900, 175)
elf = CharacterType("Elfe", 200, 1000, 150)
goblin = CharacterType("Gobelin", 125, 1000, 225)
valkyrie = CharacterType("Valkyrie", 250, 850, 250)

# Définit la fonction de création de joueur
def create_player():
    while True:
        player_name = input("Entrez votre nom d'utilisateur en jeu : ")
        password = input("Entrez votre mot de passe : ")

        user_exists = False
        if os.path.exists("players.txt"):
            with open("players.txt", "r") as file:
                for line in file:
                    if player_name in line:
                        print("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
                        user_exists = True
                        break

        if not user_exists:
            while True:
                print("Choisissez votre type de personnage : ")
                print("1. Fée\n2. Magicien\n3. Elfe\n4. Gobelin\n5. Valkyrie")
                character_type_choice = input()
                if character_type_choice == "1":
                    player = Player(player_name, fairy, password)
                elif character_type_choice == "2":
                    player = Player(player_name, wizard, password)
                elif character_type_choice == "3":
                    player = Player(player_name, elf, password)
                elif character_type_choice == "4":
                    player = Player(player_name, goblin, password)
                elif character_type_choice == "5":
                    player = Player(player_name, valkyrie, password)
                break
            
            if not os.path.exists("players.txt"):
                with open("players.txt", "w") as f:
                    f.write("NomUtilisateur MotDePasse TypePersonnage Attaque Santé Défense Niveau XP\n")

            with open("players.txt", "a") as f:
                f.write(f"{player.ign} {player.password} {player.character_type.name} {player.character_type.attack} {player.character_type.health} {player.character_type.defense} {player.level} {player.xp}\n")
                print("Utilisateur créé avec succès !")
                break

# Fonction de connexion
def login():
    while True:
        username = input("Entrez votre nom d'utilisateur : ")
        password = input("Entrez votre mot de passe : ")
        player_found = False
        user = None

        with open("players.txt", "r") as file:
            for line in file:
                fields = line.split()
                if len(fields) == 8:
                    stored_username, stored_password = fields[0], fields[1]
                    if username == stored_username and password == stored_password:
                        player_found = True
                        character_type = CharacterType(fields[2], int(fields[3]), int(fields[4]), int(fields[5]))
                        user = Player(stored_username, character_type, stored_password)

        if not player_found:
            print("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.")
        else:
            return user

def crystal_cave_exploration(player):
    print("Vous entendez un bruit inquiétant provenant du tunnel gauche de la grotte, mais une faible lueur scintille.")
    print("Le tunnel de droite est plongé dans une obscurité totale et silencieux.")
    print("1. Gauche\n2. Droite\n")
    path = input("Quel chemin souhaitez-vous emprunter ? ")
    if path == "1":
        print("Quel soulagement ! Le bruit n'était que des gouttes d'eau tombant du plafond... Mais quelle est cette lumière ?")
        print("Vous avez trouvé un cristal de santé chanceux ! +50 Santé")
        player.health += 50
        player.gain_xp(50)
    elif path == "2":
        print("Une chauve-souris maléfique attendait silencieusement dans l'obscurité. Préparez-vous à combattre !")
        print("1. Lancer un sort\n2. Tirer une flèche")
        fight = input("Nous devons vaincre la chauve-souris pour sortir d'ici vivant. Choisissez votre attaque : ")
        if fight == "1":
            print("[green]Le sort est réussi. +50 Attaque[/green]")
            player.attack += 50
            player.gain_xp(50)
        elif fight == "2":
            print("La flèche manque sa cible, et la chauve-souris montre ses crocs avant de s'envoler. -50 Santé")
            player.health -= 50
            player.gain_xp(50)

def glittering_gardens_exploration(player):
    print("Vous tombez sur un magnifique champ de fleurs et envisagez d'en cueillir une pour vous souvenir de ce paysage.")
    print("Cueillez-vous la fleur ?")
    print("1. Oui\n2. Non")
    choice = input()
    if choice == "1":
        print("Un elfe en colère arrive en courant. 'Comment osez-vous toucher à mes fleurs ?!'")
        print("Vous vous enfuyez du jardin pour éviter de créer un scandale.")
        player.health -= 50
        player.gain_xp(50)
    elif choice == "2":
        print("Autant profiter du paysage tant que vous le pouvez.")
        print("Vous restez dans le champ de fleurs, admirant les magnifiques couleurs.")
        print("Bientôt, le soleil commence à se coucher et la nuit tombe rapidement.")
        print("Un elfe à proximité vous remarque. 'Bonjour, êtes-vous perdu ?'")
        print("1. Oui\n2. Non")
        lost_choice = input()
        if lost_choice == "1":
            print("'Voici une carte pour vous aider à retrouver votre chemin. Bonne chance dans vos voyages !'")
            player.defense += 50
            player.gain_xp(50)
        elif lost_choice == "2":
            print("Vous informez l'elfe que vous admiriez simplement le champ et avez perdu la notion du temps.")
            print("L'elfe dit : 'C'est mon champ, mais cela fait longtemps que je n'ai pu partager cette vue. Prenez cette fleur et revenez bientôt.'")
            player.health += 100
            player.gain_xp(100)

def fairy_forest_exploration(player):
    pass

def mystical_mountains_exploration(player):
    pass

def swamp_of_secrets_exploration(player):
    pass

regions = {
    "0": "Retour au menu principal",
    "1": "Grotte de Cristal",
    "2": "Jardins Étincelants",
    "3": "Forêt des Fées",
    "4": "Montagnes Mystiques",
    "5": "Marais des Secrets"
}

def explore_region(player):
    while True:
        print("\nCarte :")
        for key, value in regions.items():
            print(f"{key}. {value}")
        location = input("Sélectionnez un endroit à explorer : ")

        if location == "0":
            break
        elif location == "1":
            crystal_cave_exploration(player)
        elif location == "2":
            glittering_gardens_exploration(player)
        elif location == "3":
            fairy_forest_exploration(player)
        elif location == "4":
            mystical_mountains_exploration(player)
        elif location == "5":
            swamp_of_secrets_exploration(player)
        else:
            print("Choix invalide. Veuillez sélectionner une option valide.")

if __name__ == "__main__":
    while True:
        print(ascii_art)
        print("1. Créer un nouveau joueur\n2. Connexion\n3. Quitter\n")
        choice = input("Sélectionnez une option : ")
        if choice == "1":
            create_player()
        elif choice == "2":
            player = login()
            explore_region(player)
        elif choice == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez sélectionner une option valide.")