from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console
import os
import time
import bcrypt

ascii_art = r"""
   ___                   ____      __        __         _     _ 
  / _ \ _ __   ___ _ __ |  _ \ _   \ \      / /__  _ __| | __| |
 | | | | '_ \ / _ \ '_ \| |_) | | | \ \ /\ / / _ \| '__| |/ _` |
 | |_| | |_) |  __/ | | |  __/| |_| |\ V  V / (_) | |  | | (_| |
  \___/| .__/ \___|_| |_|_|    \__, | \_/\_/ \___/|_|  |_|\__,_|
       |_|                     |___/                            
"""

class Item:
    def __init__(self, name, description, effect_type, value):
        self.name = name
        self.description = description
        self.effect_type = effect_type  # 'attack', 'defense', 'health'
        self.value = value

# Définit la classe Joueur
class Player:
    def __init__(self, ign, character_type, password_hash):
        self.ign = ign
        self.character_type = character_type
        self.password_hash = password_hash
        self.attack = character_type.attack
        self.health = character_type.health
        self.max_health = character_type.health  # Fix: Use character_type.health directly
        self.defense = character_type.defense
        self.xp = 0
        self.level = 1
        self.inventory = []
        self.active_effects = {}

    def add_item(self, item):
        self.inventory.append(item)
        print(f"[green]Vous avez obtenu : {item.name} ![/green]")
        
    def show_inventory(self):
        if not self.inventory:
            print("[bold red]Votre inventaire est vide ![/bold red]")
            return

        panels = []
        for idx, item in enumerate(self.inventory, 1):
            panel = Panel.fit(
                f"{item.description}\n[bold]Effet : [/bold]+{item.value} {item.effect_type}",
                title=f"[yellow]{item.name}[/yellow]",
                subtitle=f"[cyan]Item {idx}[/cyan]"
            )
            panels.append(panel)
        
        print(Columns(panels))
        
    def use_item(self, item_index):
        try:
            item = self.inventory.pop(item_index - 1)
            effect_duration = 3  # Nombre de combats
            self.active_effects[item.effect_type] = {
                'value': item.value,
                'duration': effect_duration
            }
            print(f"[bold green]Vous utilisez {item.name} ! (+{item.value} {item.effect_type} pour {effect_duration} combats)[/bold green]")
        except IndexError:
            print("[bold red]Numéro d'objet invalide ![/bold red]")

    def update_player_stats(self, new_attack, new_health, new_defense):
        self.attack = new_attack
        self.health = new_health
        self.defense = new_defense

    def is_alive(self):
        return self.health > 0

    # Ajoutez cette méthode dans la classe Player
    def get_rank(self):
        if self.level <= 5:
            return "Novice"
        elif 6 <= self.level <= 10:
            return "Aventurier"
        elif 11 <= self.level <= 15:
            return "Héros"
        elif 16 <= self.level <= 20:
            return "Maître"
        else:
            return "Légende"

    def level_up(self):
        self.level += 1
        rank = self.get_rank()
        print(f"[bold green]Niveau supérieur ![/bold green] Vous êtes maintenant [bold]{rank}[/bold] (niveau {self.level})")
        self.save_to_file()

    # Modifiez la méthode show_healthbar pour inclure le rang
    def show_healthbar(self):
        filled_hearts = self.health // 10
        empty_hearts = (self.max_health - self.health) // 10
        rank = self.get_rank()
        print(f"\n[bold]Niveau {self.level} - {rank}[/bold]")
        print(f"[{'❤️' * filled_hearts}{'♡' * empty_hearts}] {self.health}/{self.max_health} PV")

    def show_xp_bar(self):
        required_xp = self.calculate_level()
        progress = self.xp / required_xp if required_xp > 0 else 0
        filled_blocks = int(20 * progress)
        empty_blocks = 20 - filled_blocks
        
        xp_bar = Panel(
            f"[green]▮[/green]" * filled_blocks + 
            f"[white]▯[/white]" * empty_blocks +
            f"\n\n[bold]{self.xp}/{required_xp} XP[/bold] ([cyan]{progress:.0%}[/cyan])",
            title="[bold yellow]Progression du Niveau[/bold yellow]",
            border_style="blue"
        )
        print(xp_bar)

    def calculate_level(self):
        return self.level * 100
    
    def gain_xp(self, amount):
        prev_level = self.level
        self.xp += amount
        while self.xp >= self.calculate_level():
            self.level_up()
        if prev_level == self.level:
            self.show_xp_bar()
        self.save_to_file()
            
    def save_to_file(self):
        with open("players.txt", "r") as file:
            lines = file.readlines()

        with open("players.txt", "w") as file:
            for line in lines:
                if self.ign in line:
                    # Modification de la ligne pour utiliser password_hash
                    line = f"{self.ign} {self.password_hash.decode()} {self.character_type.name} {self.attack} {self.health} {self.defense} {self.level} {self.xp}\n"
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

def display_player_stats(player_data):
    """Affiche les statistiques d'un joueur de manière élégante"""
    stats = Panel.fit(
        f"[bold]Classe:[/bold] {player_data['TypePersonnage']}\n"
        f"[bold]Niveau:[/bold] {player_data['Niveau']} ({player_data['XP']} XP)\n"
        f"[bold]Rang:[/bold] {player_data['Rang']}\n"
        f"[bold]Attaque:[/bold] {player_data['Attaque']}\n"
        f"[bold]Santé:[/bold] {player_data['Santé']}\n"
        f"[bold]Défense:[/bold] {player_data['Défense']}",
        title=f"[bold green]Statistiques de {player_data['NomUtilisateur']}[/bold green]",
        border_style="cyan"
    )
    print(stats)

def search_player_stats():
    """Cherche et affiche les stats d'un joueur"""
    username = input("\nEntrez le pseudo à rechercher : ")
    found = False
    
    try:
        # Essayer avec UTF-8 puis latin-1
        try:
            with open("players.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            with open("players.txt", "r", encoding="latin-1") as file:
                lines = file.readlines()
        
        for line in lines:
            if line.startswith(username + " "):
                fields = line.strip().split()
                # Convertir les données au bon format
                player_data = {
                    "NomUtilisateur": fields[0],
                    "TypePersonnage": fields[2],
                    "Attaque": int(fields[3]),
                    "Santé": int(fields[4]),
                    "Défense": int(fields[5]),
                    "Niveau": int(fields[6]),
                    "XP": int(fields[7]),
                    "Rang": Player(fields[0], CharacterType("",0,0,0), "").get_rank()
                }
                display_player_stats(player_data)
                found = True
                break
    except FileNotFoundError:
        pass
    
    if not found:
        print(f"\n[bold red]Aucun joueur trouvé avec le pseudo '{username}'[/bold red]")


def show_leaderboard():
    """Affiche le classement des joueurs"""
    players = []
    
    try:
        # Attempt to open the file with UTF-8 encoding
        try:
            with open("players.txt", "r", encoding="utf-8") as file:
                lines = file.readlines() # Ignorer l'en-tête
        except UnicodeDecodeError:
            # Fallback to latin-1 encoding if UTF-8 fails
            with open("players.txt", "r", encoding="latin-1") as file:
                lines = file.readlines()  # Ignorer l'en-tête
            
        for line in lines:
            fields = line.strip().split()
            if len(fields) == 8:
                players.append({
                    "username": fields[0],
                    "class": fields[2],
                    "level": int(fields[6]),
                    "xp": int(fields[7])
                })
                    
        # Trie par niveau puis XP
        players.sort(key=lambda x: (-x["level"], -x["xp"]))
        
        # Création du tableau
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Position", style="cyan")
        table.add_column("Pseudo", style="green")
        table.add_column("Classe")
        table.add_column("Niveau", justify="right")
        table.add_column("XP", justify="right")
        
        for idx, player in enumerate(players[:10], 1):
            table.add_row(
                f"{idx}ère" if idx == 1 else f"{idx}ème",
                player["username"],
                player["class"],
                str(player["level"]),
                f"{player['xp']:,}"
            )
            
        print(Panel(table, title="[bold yellow]Classement des Joueurs[/bold yellow]"))
        
    except FileNotFoundError:
        print("[red]Aucun joueur enregistré ![/red]")


bouclier_cristal = Item(
    "Bouclier de Cristal", 
    "Un bouclier translucide qui brille faiblement", 
    "defense", 
    50
)

potion_sante = Item(
    "Potion de Vitalité",
    "Une fiole contenant un liquide rougeoyant",
    "health",
    100
)

# Définit la fonction de création de joueur
def create_player():
    while True:
        player_name = input("Entrez votre nom d'utilisateur en jeu : ")
        password = input("Entrez votre mot de passe : ")

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
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
                    player = Player(player_name, fairy, password_hash)
                    break  # Ajout du break
                elif character_type_choice == "2":
                    player = Player(player_name, wizard, password_hash)
                    break  # Ajout du break
                elif character_type_choice == "3":
                    player = Player(player_name, elf, password_hash)
                    break  # Ajout du break
                elif character_type_choice == "4":
                    player = Player(player_name, goblin, password_hash)
                    break  # Ajout du break
                elif character_type_choice == "5":
                    player = Player(player_name, valkyrie, password_hash)
                    break  # Ajout du break
                else:
                    print("[bold red]Choix invalide ! Veuillez sélectionner 1 à 5.[/bold red]")

            if not os.path.exists("players.txt"):
                with open("players.txt", "w", encoding="utf-8") as f:
                    f.write("NomUtilisateur HashMotDePasse TypePersonnage Attaque Santé Défense Niveau XP\n")

            with open("players.txt", "a", encoding="utf-8") as f:
                f.write(f"{player.ign} {player.password_hash.decode()} {player.character_type.name} {player.character_type.attack} {player.character_type.health} {player.character_type.defense} {player.level} {player.xp}\n")
                print("Utilisateur créé avec succès !")
                time.sleep(3)
                break

# Fonction de connexion
def login():
    while True:
        print("\n[bold]Connexion (entrez '0' pour annuler)[/bold]")
        username = input("Nom d'utilisateur : ")
        if username == "0":
            return None
        password = input("Mot de passe : ")
        player_found = False
        user = None

        try:
            with open("players.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            with open("players.txt", "r", encoding="latin-1") as file:
                lines = file.readlines()

        for line in lines:
            fields = line.split()
            if len(fields) >= 8 and username == fields[0]:
                # Vérification du mot de passe avec bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), fields[1].encode('utf-8')):
                    player_found = True
                    character_type = CharacterType(fields[2], int(fields[3]), int(fields[4]), int(fields[5]))
                    user = Player(fields[0], character_type, fields[1].encode('utf-8'))
                    break

        if not player_found:
            print("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.")
        else:
            console.clear()
            print(f"\n[bold green]Connexion réussie ![/bold green]")
            print(f"Bienvenue [bold]{user.ign}[/bold] - Rang actuel : [bold]{user.get_rank()}[/bold]")
            return user

def crystal_cave_exploration(player):
    print("Vous entendez un bruit inquiétant provenant du tunnel gauche de la grotte, mais une faible lueur scintille.")
    print("Le tunnel de droite est plongé dans une obscurité totale et silencieux.")
    print("1. Gauche\n2. Droite\n")
    path = input("Quel chemin souhaitez-vous emprunter ? ")
    if path == "1":
        player.add_item(potion_sante)
        print("Quel soulagement ! Le bruit n'était que des gouttes d'eau tombant du plafond... Mais quelle est cette lumière ?")
        print("Vous avez trouvé un cristal de santé chanceux ! +50 Santé")
        player.health += 50
        player.show_healthbar()
        player.gain_xp(50)
    elif path == "2":
        player.add_item(bouclier_cristal)
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
        print("\n[bold cyan]Menu Principal d'Exploration[/bold cyan]")
        print(Columns([
        Panel("[bold]1. Explorer une zone\n2. Afficher l'inventaire\n3. Se déconnecter[/bold]", 
            title="Options", 
            border_style="yellow"),
        Panel(f"[bold green]Santé:[/bold green] {player.health}\n"
            f"[bold red]Attaque:[/bold red] {player.attack}\n"
            f"[bold blue]Défense:[/bold blue] {player.defense}",
            title="Stats",
            border_style="blue")
        ]))
        
        main_choice = input("\nChoisissez une action : ")
        
        if main_choice == "1":
            while True:
                print("\n[bold]Carte des Zones d'Exploration[/bold]")
                for key, value in regions.items():
                    print(f"[bold]{key}.[/bold] {value}")
                
                zone_choice = input("\nChoisissez une zone à explorer (0 pour annuler) : ")
                
                if zone_choice == "0":
                    break
                elif zone_choice == "1":
                    crystal_cave_exploration(player)
                elif zone_choice == "2":
                    glittering_gardens_exploration(player)
                elif zone_choice == "3":
                    fairy_forest_exploration(player)
                elif zone_choice == "4":
                    mystical_mountains_exploration(player)
                elif zone_choice == "5":
                    swamp_of_secrets_exploration(player)
                else:
                    print("[bold red]Choix invalide ![/bold red]")
                
                # Vérifier les effets actifs après chaque exploration
                for effect in list(player.active_effects.keys()):
                    player.active_effects[effect]['duration'] -= 1
                    if player.active_effects[effect]['duration'] <= 0:
                        del player.active_effects[effect]
                        print(f"[italic]L'effet {effect} a expiré ![/italic]")
        
        elif main_choice == "2":
            print("\n[bold yellow]Inventaire du Joueur[/bold yellow]")
            player.show_inventory()
            if player.inventory:
                item_choice = input("\nEntrez le numéro de l'objet à utiliser (enter pour annuler) : ")
                if item_choice.isdigit():
                    player.use_item(int(item_choice))
        
        elif main_choice == "3":
            print("\nRetour au menu principal...")
            break
        
        else:
            print("[bold red]Choix invalide ![/bold red]")
        
        # Sauvegarder après chaque action
        player.save_to_file()

if __name__ == "__main__":
    console = Console()
    first_time = True
    
    while True:
        if first_time:
            # Fade-in animation with clearing
            for step in range(20):
                intensity = int(255 * (step / 19))
                color = f"#{intensity:02X}{intensity:02X}{intensity:02X}"
                console.clear()
                console.print(ascii_art, style=color)
                time.sleep(0.05)
            first_time = False
        else:
            console.clear()
            print(ascii_art)
        
        print(Columns([
            Panel("[bold cyan]1. Créer un joueur\n2. Connexion\n3. Quitter[/bold cyan]", 
                   title="Menu Principal", border_style="yellow"),
            Panel("[bold green]4. Rechercher un joueur\n5. Classement[/bold green]", 
                   title="Autres Options", border_style="blue")
        ]))
        
        choice = input("\nSélectionnez une option : ")
        
        if choice == "1":
            create_player()
        elif choice == "2":
            player = login()
            if player:
                explore_region(player)
        elif choice == "3":
            console.clear()
            print("\n[bold yellow]Au revoir ![/bold yellow]")
            break
        elif choice == "4":
            search_player_stats()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == "5":
            show_leaderboard()
            input("\nAppuyez sur Entrée pour continuer...")
        else:
            print("[bold red]Option invalide![/bold red]")
            time.sleep(1)