from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console
from rich.box import Box
from rich.box import ROUNDED 
from rich.live import Live
from rich.progress import Progress, BarColumn
from rich.text import Text
import itertools
import os
import random
import time
import bcrypt
import random

ascii_art = r"""
   ___                   ____      __        __         _     _ 
  / _ \ _ __   ___ _ __ |  _ \ _   \ \      / /__  _ __| | __| |
 | | | | '_ \ / _ \ '_ \| |_) | | | \ \ /\ / / _ \| '__| |/ _` |
 | |_| | |_) |  __/ | | |  __/| |_| |\ V  V / (_) | |  | | (_| |
  \___/| .__/ \___|_| |_|_|    \__, | \_/\_/ \___/|_|  |_|\__,_|
       |_|                     |___/                            
"""

def attack_animation(live=None):
    frames = ["⚔️", "🔥", "💥", "✨"]
    for frame in frames:
        if live:
            live.update(Text(frame, style="bold red"))
        else:
            print(frame)  # Fallback if no live instance is provided
        time.sleep(0.3)


def show_animated_ascii():
    console = Console()
    colors = ["#FF69B4", "#4B0082", "#0000FF", "#00FF00", "#FFFF00", "#FF7F00", "#FF0000"]
    
    for color in colors:
        console.clear()
        console.print(ascii_art, style=color)
        time.sleep(0.1)

def animate_xp_gain(start, end, required):
    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.0f}%",
    )
    
    with Live(progress, refresh_per_second=20):
        task = progress.add_task("XP", total=required)
        for xp in range(start, end + 1):
            progress.update(task, advance=1, description=f"{xp}/{required} XP")
            time.sleep(0.02)

def scroll_text(text, style="white", delay=0.03):
    console = Console()
    for char in str(text):
        console.print(char, style=style, end="", highlight=False)
        time.sleep(delay)
    print()

def screen_transition(style="cyan", length=30):
    console = Console()
    for i in range(length):
        console.print("▉" * i, style=style, end="\r")
        time.sleep(0.03)
    console.clear()

class Item:
    def __init__(self, name, description, effect_type, value):
        self.name = name
        self.description = description
        self.effect_type = effect_type
        self.value = value

# Définit la classe Joueur
class Player:
    def __init__(self, ign, character_type, password_hash):
        self.ign = ign
        self.character_type = character_type
        self.password_hash = password_hash
        self.attack = character_type.attack
        self.health = character_type.health
        self.max_health = character_type.health
        self.defense = character_type.defense
        self.xp = 0
        self.level = 1
        self.inventory = []
        self.active_effects = {}
        self.completed_regions = []

    def add_item(self, item):
        self.inventory.append(item)
        print(f"[green]Vous avez obtenu : {item.name} ![/green]")
        
    def show_inventory(self):
        if not self.inventory:
            print("[blink bold red]Votre inventaire est vide ![/blink bold red]")
            return

        panels = []
        for idx, item in enumerate(self.inventory, 1):
            panel = Panel.fit(
                f"[bold]{item.description}[/bold]\n[blink]Effet : +{item.value} {item.effect_type}[/blink]",
                title=f"[reverse]{item.name}[/reverse]",
                border_style=random.choice(["green", "yellow", "cyan", "magenta"]),
                box=ROUNDED
            )
            panels.append(panel)
        
        print(Columns(panels, expand=True))
        
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

    def check_if_dead(self):
        if self.health <= 0:
            print("[bold red]Vous êtes mort ! Vous ne pouvez plus jouer tant que vos HP ne sont pas positifs.[/bold red]")
            return True
        return False

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
        previous_level = self.level
        self.level += 1
        
        base_multiplier = self.level ** 1.5 
        
        attack_gain = int(5 + base_multiplier * 1.2)
        defense_gain = int(3 + base_multiplier * 0.8)
        health_gain = int(20 + base_multiplier * 2.5)
        
        # Application des gains
        self.attack += attack_gain
        self.defense += defense_gain
        self.max_health += health_gain
        self.health = self.max_health

        rank = self.get_rank()
        print(Panel.fit(
            f"[bold cyan]NIVEAU {previous_level} → {self.level}[/bold cyan]\n"
            f"[green]↑ Attaque: +{attack_gain} ({self.attack - attack_gain} → {self.attack})[/green]\n"
            f"[blue]↑ Défense: +{defense_gain} ({self.defense - defense_gain} → {self.defense})[/blue]\n"
            f"[red]❤ Santé max: +{health_gain} ({self.max_health - health_gain} → {self.max_health})[/red]",
            title=f"[gold1]NIVEAU SUPÉRIEUR ![/gold1] [italic]({rank})[/italic]",
            border_style="green",
            padding=(1, 2)
        ))
        
        self.save_to_file()

    def show_healthbar(self):
        filled = self.health // 10
        empty = (self.max_health - self.health) // 10
        return f"[{'❤️' * filled}{'♡' * empty}] {self.health}/{self.max_health} PV"

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
        return int(100 * (1.5 ** (self.level - 1)))
    
    def gain_xp(self, amount):
        prev_level = self.level
        prev_xp = self.xp
        self.xp += amount
        
        if prev_level == self.level:
            required = self.calculate_level()
            animate_xp_gain(prev_xp, self.xp, required)
        
        while self.xp >= self.calculate_level():
            self.level_up()
        
        self.save_to_file()
            
    def save_to_file(self):
        # Lecture de toutes les lignes
        with open("players.txt", "r") as f:
            lines = f.readlines()

        # Création des nouvelles lignes
        new_lines = []
        player_found = False
        
        for line in lines:
            if line.startswith(self.ign + " "):
                new_line = f"{self.ign} {self.password_hash.decode()} {self.character_type.name} " \
                        f"{self.attack} {self.max_health} {self.defense} " \
                        f"{self.level} {self.xp} {','.join(self.completed_regions)}\n"
                new_lines.append(new_line)
                player_found = True
            else:
                new_lines.append(line)

        # Si le joueur n'était pas dans le fichier (normalement impossible)
        if not player_found:
            new_lines.append(f"{self.ign} {self.password_hash.decode()} {self.character_type.name} " \
                            f"{self.attack} {self.max_health} {self.defense} " \
                            f"{self.level} {self.xp} {','.join(self.completed_regions)}\n")

        # Réécriture complète du fichier
        with open("players.txt", "w") as f:
            f.writelines(new_lines)

    def set_username(self, new_username):
        old_username = self.ign
        self.ign = new_username
        
        # Mise à jour directe du fichier sans utiliser save_to_file()
        with open("players.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()
            
            for line in lines:
                if line.startswith(old_username + " "):
                    new_line = f"{self.ign} {self.password_hash.decode()} {self.character_type.name} " \
                            f"{self.attack} {self.max_health} {self.defense} " \
                            f"{self.level} {self.xp} {','.join(self.completed_regions)}\n"
                    f.write(new_line)
                else:
                    f.write(line)
        
        print("[green]Nom d'utilisateur modifié avec succès ![/green]")

    def set_password(self, new_password):
        """Modifie le mot de passe"""
        self.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.save_to_file()
        print("[bold green]Mot de passe modifié avec succès ![/bold green]")

    def show_account_menu(self):
        """Affiche le menu de gestion du compte"""
        while True:
            print(Columns([
                Panel("[bold]1. Changer le nom d'utilisateur\n2. Changer le mot de passe\n3. Retour[/bold]", 
                    title="Gestion du Compte", border_style="cyan"),
                Panel(f"[italic]Nom actuel:[/italic] [bold]{self.ign}[/bold]\n"
                      f"[italic]Classe:[/italic] {self.character_type.name}",
                    border_style="yellow")
            ]))
            
            choice = input("\nChoisissez une option : ")
            
            if choice == "1":
                new_name = input("Nouveau nom d'utilisateur : ")
                if new_name == self.ign:
                    print("[yellow]C'est déjà votre nom actuel ![/yellow]")
                    continue
                
                # Vérifie si le nom existe déjà
                with open("players.txt", "r") as f:
                    if any(line.startswith(new_name + " ") for line in f):
                        print("[bold red]Ce nom est déjà pris ![/bold red]")
                        continue
                
                self.set_username(new_name)
                
            elif choice == "2":
                current_pass = input("Mot de passe actuel : ")
                if not bcrypt.checkpw(current_pass.encode('utf-8'), self.password_hash):
                    print("[bold red]Mot de passe incorrect ![/bold red]")
                    continue
                
                new_pass = input("Nouveau mot de passe : ")
                confirm_pass = input("Confirmez le nouveau mot de passe : ")
                
                if new_pass != confirm_pass:
                    print("[bold red]Les mots de passe ne correspondent pas ![/bold red]")
                    continue
                
                self.set_password(new_pass)
                
            elif choice == "3":
                break
            
            else:
                print("[bold red]Option invalide ![/bold red]")

class Enemy:
    def __init__(self, name, health, attack, defense, xp_reward):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.xp_reward = xp_reward

    def check_if_dead(self):
        """Vérifie si l'ennemi est mort."""
        return self.health <= 0

    def show_health(self):
        filled = self.health // 10
        empty = (self.max_health - self.health) // 10
        return f"[{'❤️' * filled}{'♡' * empty}] {self.health}/{self.max_health} PV"

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

def start_combat(player, enemy):
    console = Console()
    console.clear()
    player_parry_cooldown = 0
    enemy_parry_cooldown = 0
    player_parry_active = False
    enemy_parry_active = False

    while not player.check_if_dead() and not enemy.check_if_dead():
        # Affichage des stats du joueur et de l'ennemi
        console.print(f"\n[bold cyan]{player.ign}[/bold cyan] - Santé : {player.show_healthbar()}")
        console.print(f"[bold red]{enemy.name}[/bold red] - Santé : {enemy.show_health()}")

        # Menu d'action
        print("\n[bold]Que voulez-vous faire ?[/bold]")
        print("1. Attaquer")
        print("2. Utiliser un objet")
        print(f"3. Parer {'(disponible)' if player_parry_cooldown == 0 else f'(cooldown {player_parry_cooldown} tours)'}")
        action = input("\nChoisissez une action : ")

        if action == "1":
            # Attaque du joueur
            if enemy_parry_active:
                console.print(f"[bold cyan]{enemy.name} pare votre attaque ![/bold cyan]")
                enemy_parry_active = False
            else:
                damage = max(int((player.attack * random.uniform(1.0, 1.5)) - (enemy.defense * 0.5)), 1)
                enemy.health -= damage
                console.print(f"[bold green]Vous infligez {damage} dégâts à {enemy.name} ![/bold green]")

        elif action == "2":
            # Utilisation d'un objet
            if not player.inventory:
                console.print("[red]Votre inventaire est vide ![/red]")
                continue
            player.show_inventory()
            try:
                choice = int(input("Entrez le numéro de l'objet à utiliser (0 pour annuler) : "))
                if choice == 0:
                    continue
                player.use_item(choice)
            except (ValueError, IndexError):
                console.print("[red]Choix invalide ![/red]")

        elif action == "3" and player_parry_cooldown == 0:
            # Activation de la parade
            player_parry_active = True
            player_parry_cooldown = 3
            console.print("[bold cyan]Vous vous préparez à parer ![/bold cyan]")
        else:
            console.print("[red]Action invalide ou indisponible ![/red]")

        # Vérification si l'ennemi est mort
        if enemy.check_if_dead():
            break

        # Tour de l'ennemi
        if random.random() < 0.3 and enemy_parry_cooldown == 0:  # 30% de chance de parer
            enemy_parry_active = True
            enemy_parry_cooldown = 3
            console.print(f"[bold red]{enemy.name} se prépare à parer ![/bold red]")
        else:
            if player_parry_active:
                damage = max(int((enemy.attack * random.uniform(1.0, 1.5)) - (player.defense * 0.5)), 1)
                player.health -= damage
                console.print(f"[bold cyan]Vous contre-attaquez et infligez {damage} dégâts à {enemy.name} ![/bold cyan]")
                player_parry_active = False
            else:
                damage = max(int((enemy.attack * random.uniform(1.0, 1.5)) - (player.defense * 0.5)), 1)
                player.health -= damage
                console.print(f"[bold red]{enemy.name} vous inflige {damage} dégâts ![/bold red]")

        # Réduction des cooldowns de parade
        if player_parry_cooldown > 0:
            player_parry_cooldown -= 1
        if enemy_parry_cooldown > 0:
            enemy_parry_cooldown -= 1

    # Résultat du combat
    console.clear()
    if not player.check_if_dead():
        console.print(f"[bold green]Victoire ! Vous avez vaincu {enemy.name} et gagné {enemy.xp_reward} XP ![/bold green]")
        player.gain_xp(enemy.xp_reward)
    else:
        console.print(f"[bold red]Défaite... {enemy.name} vous a vaincu.[/bold red]")

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
        # Lecture du fichier avec gestion des encodages
        try:
            with open("players.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            with open("players.txt", "r", encoding="latin-1") as file:
                lines = file.readlines()
        
        # Parcours des lignes pour extraire les données des joueurs
        for line in lines:
            fields = line.strip().split()
            if len(fields) >= 8:  # Vérifie que la ligne contient suffisamment de données
                players.append({
                    "username": fields[0],
                    "class": fields[2],
                    "level": int(fields[6]),
                    "xp": int(fields[7])
                })
        
        # Trie par niveau (descendant) puis par XP (descendant)
        players.sort(key=lambda x: (-x["level"], -x["xp"]))
        
        # Création du tableau pour afficher les joueurs
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Position", style="cyan")
        table.add_column("Pseudo", style="green")
        table.add_column("Classe")
        table.add_column("Niveau", justify="right")
        table.add_column("XP", justify="right")
        
        # Ajout des joueurs au tableau (limité aux 10 premiers)
        for idx, player in enumerate(players[:10], 1):
            table.add_row(
                f"{idx}ère" if idx == 1 else f"{idx}ème",
                player["username"],
                player["class"],
                str(player["level"]),
                f"{player['xp']:,}"
            )
        
        # Affichage du tableau dans un panneau
        print(Panel(table, title="[bold yellow]Classement des Joueurs[/bold yellow]"))
    
    except FileNotFoundError:
        print("[red]Aucun joueur enregistré ![/red]")


potion_invisibilite = Item(
    "Potion d'invisibilité",
    "Une potion qui vous rend invisible",
    "defense",
    1
)

potion_invincibilite = Item(
    "Potion d'invincibilité",
    "Une potion qui vous rend invincible",
    "defense",
    999
)

potion_sante = Item(
    "Potion de Vitalité",
    "Une fiole contenant un liquide rougeoyant",
    "health",
    100
)

feuille_dor = Item(
    "Feuille d'or",
    "Une feuille permettant vla les choses",
    "health",
    1
)

epee_mcd_attack = Item(
    "Épée MCD",
    "Une épée légendaire très puissante",
    "attack",
    889
)

wamp_cave_plan = Item(
    "Plan de la Wamp Cave", 
    "Cette carte vous permettra de vous repérer dans le château de Wamp", 
    "health",
    1
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
                    f.write(f"{player.ign} {player.password_hash.decode()} {player.character_type.name} "
                    f"{player.character_type.attack} {player.character_type.health} "
                    f"{player.character_type.defense} {player.level} {player.xp} \n")
                    print("Utilisateur créé avec succès !")
                    time.sleep(3)
                    break

def show_game_map():
    console = Console()
    console.clear()
    
    ascii_map = r"""
  _________________________________________________________
 /                                                         \
|  [bold]1. La Montagne de l'Enfer[/bold]                    [bold]2. Le Vaisseau Amiral[/bold]  |
|   ___   ___   ___                      /\  /\  /\        |
|  /   \ /   \ /   \                   /  \/  \/  \       |
| |     Cavernes     |                /             \      |
|  \___/ \___/ \___/                  \/\        /\/      |
|      |                  ______________  \      /         |
|      |                 /              \ \    /           |
| [bold]2. Jardins Étincelants[/bold]  | [bold]5. Marais des Secrets[/bold] | |
|   o  o  o  o  o      |  ~~  ~~  ~~  ~~ |    | ~~  ~~    |
|  < Fleurs Magiques >  |  Marécages     |    |           |
|   o  o  o  o  o       \_______________/     |  Serpents |
|      |                          |            \_/  \_/    |
|      |                         / \                       |
| [bold]3. Forêt des Fées[/bold]       /   \                      |
|   /\  /\  /\              ____/     \____                |
|  /  \/  \/  \           /               \               |
| |  Arbres     |         |  [bold]Campement[/bold]   |              |
|  \  Ancestraux/          \_______________/               |
 \_________________________________________________________/
    """
    
    print(Panel.fit(f"[cyan]{ascii_map}[/cyan]", 
          title="[bold gold1]Carte du Royaume d'Eldoria[/bold gold1]", 
          border_style="green",
          padding=(1, 2)))
    input("\nAppuyez sur Entrée pour retourner au menu...")
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
                    if line.startswith(username + " "):
                        fields = line.strip().split()
                        if len(fields) >= 8 and username == fields[0]:
                            if bcrypt.checkpw(password.encode('utf-8'), fields[1].encode('utf-8')):
                                player_found = True
                                character_type = CharacterType(fields[2], int(fields[3]), int(fields[4]), int(fields[5]))
                                user = Player(fields[0], character_type, fields[1].encode('utf-8'))
                                # Chargement des données sauvegardées
                                user.level = int(fields[6])
                                user.xp = int(fields[7])
                                user.attack = int(fields[3])
                                user.defense = int(fields[5])
                                user.max_health = int(fields[4])  # Correction du max_health
                                user.health = int(fields[4])
                                if len(fields) >= 9:
                                    user.completed_regions = fields[8].split(',')
                                break

        if not player_found:
            print("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.")
        else:
            console.clear()
            print(f"\n[bold green]Connexion réussie ![/bold green]")
            print(f"Bienvenue [bold]{user.ign}[/bold] - Rang actuel : [bold]{user.get_rank()}[/bold]")
            return user

def la_montagne_de_lenfer(player):
    scroll_text("Vous tombez sur une feuille d'or au sol...", style="#FFA500")
    print("1. Vous ramassez la feuille\n2. Vous mangez la feuille \n")
    feuille = input("Que souhaitez vous faire ? ")
    if feuille == "1":
        print("Trop cool une feuille !")
        player.add_item(feuille_dor)
        print("Vous rencontrez Gandalf 'Bonjour jeune fourbe, que faites vous ici ?' :")
        print("1. Bonjour, je suis perdu, aide moi par pitié !\n2. Bonjour Monsieur, qui êtes vous ? Je suis à la recherche du One Piece \n")
        rep_gand = input("Quoi répondre a Gandalf ?")
        if rep_gand == "1":
            print("'Tiens pomme' -1500HP")
            player.health -= 1500
            if player.check_if_dead():
                return 
        elif rep_gand == "2":
            print("'Je suis Gandalf, le seul habitant de cette dimension. Prends cette carte, elle t'y mènera'")
            print("Vous arrivez devant le OnePiece et donc devant le boss de la montagne")
            print("Le boss MODELIO se dresse sur le chemin (BOSS : NAME : Modelio 1350HP ATTACK : 500 DEFENSE : 300)")
            print("1. Vous donnez la feuille au boss\n2. Vous attaquez le boss \n")
            modelio = input("Pris de panique vous devez prendre une décision crutiale : ")
            if modelio == "1":
                print("Vous avez vaincu le cruel boss modelio !")
                player.gain_xp(300)
            elif modelio == "2":
                boss_modelio = Enemy("MODELIO", 1350, 300, 150, 500)
                start_combat(player, boss_modelio)
    elif feuille == "2":
        print("Miam c'est vraiment trop bon !")
        player.gain_xp(100)

def le_vaisseau_amiral(player):
    print("Vous êtes à l'entrée du vaisseau et rencontrez l'alien ' Salut, que fais tu ici ?'")
    print("1. Si on fait une partie d'échecs et que je gagne, tu me laisse passer ?")
    print("2. Bonjour, je cherche le commandant du vaisseau")
    choice = input("Quoi lui répondre ? : ")
    if choice == "1":
        print("'T'es pas très fort pour le goat des échecs dis donc !'")
        print("Tu te fais ratio salement avec un mat du berger -50HP")
        player.health = player.health - 50
        player.show_healthbar()
        player.gain_xp(50)
    elif choice == "2":
        print("'Suivez moi, je vais vous y mener'")
        print("Vous ouvrez la porte du centre de commandement")
        print("'Que faites vous ici !?'")
        print("1. Votre vaisseau m'appartient dès à présent !\n2. Ah non rien, je visite\n")
        prise_vaisseau = input("Que souhaitez vous faire ? : ")
        if prise_vaisseau == "1":
            print("Votre vaisseau m'appartient dès à présent ! + 50 DEF")
            player.defense += 50
            player.gain_xp(50)
            print("Le commandant du vaisseau veut vous combattre")
            print("1. Vous décidez d'utiliser le pion d'échecs comme totem d'immortalité")
            print("2. Vous essayez de vaincre le commandant du vaisseau")
            commandant = input("Que souhaitez vous faire ? : ")
            if commandant == "1":
                print("Le boss finit par mourir car vous êtes immortel")
                print("EZ bouffon")
            elif commandant == "2":
                boss_vaisseau = Enemy("Commandant du vaisseau", 500, 200, 100, 200)
                start_combat(player, boss_vaisseau)
        elif prise_vaisseau == "2":
            print("Vous vous faites expulser du vaisseau par l'alien")

def le_parc_mcd(player):
    scroll_text("Vous vous retrouvez devant un parc d'attraction à l'abandon et rencontrez l'armée de Looping :", style="#FFA500")
    print("1. Je tente de les contourner en escaladant la structure de l'attraction devant moi.")
    print("2. Je vais directement dans la direction de l'armée en espérant qu'ils me laissent passer.")
    parc = input("Que souhaitez vous faire ? : ")
    if parc == "1":
        print("Vous êtes sur une plateforme au dessus de l'armée :")
        print("1. Vous décidez de vous faufiler sur la plateforme jusqu'au boss Looping en espérant ne pas vous faire repérer.")
        print("2. Vous tentez de descendre de la plateforme juste derrière les gardes.")
        plateforme = input("Que souhaitez vous faire ? : ")
        if plateforme == "1":
            print("L'armée de Looping vous attaque et vous perdez car vous vous prenez pour Francis Ngannou")
            player.health = player.health - 100
            player.show_healthbar()
        elif plateforme == "2":
            print("Un garde vous repère 'Revenez !'")
            garde = input("Voulez vous retourner vers le garde ? \n1. Oui\n2. Non")
            if garde == "1":
                print("Le garde vous donne son épée de fou malade")
                player.add_item(epee_mcd_attack)
            elif garde == "2":
                print("Vous continuez a courrir vers le boss")
                print("Vous vous trouvez maintenant devant le boss Looping(HP 1500  ATTACK : 750 DEFENSE : 250 )")
                loopi = input("1. Vous utilisez l'épée MCD du garde\n2. Vous Activez votre totem d'immortalité")
                if loopi == "1":
                    print("Vous vous faites ratio par les clés étrangères")
                    player.health = player.health - 100
                    player.show_healthbar()
                elif loopi == "2":
                    print("Vous gagnez")
                    print("EZ")
                    player.gain_xp(200)
    elif parc == "2":
        print("L'armée de Looping vous attaque et vous perdez car vous vous prenez pour Francis Ngannou")
        player.health = player.health - 100
        player.show_healthbar()

def la_foret_maria_db(player):
    scroll_text("Vous apparaissez dans une forêt assez sombre, avec autour de vous une clés étrangère :", style="#FFA500")
    key = input("1. Vous ramassez la clé\n2. Vous laissez la clé par terre\n")
    if key == "1":
        print("Une super clé inutile retour lobby...")
        player.health = player.health + 300
    elif key == "2":
        print("Soudain vous vous retrouvez face à une table de téléportation en plein milieu du chemin :")
        print("1 : Vous choisissez de vous téléporter à l'entrée de la forêt")
        print("2 : Vous choisissez de vous téléporter dans le royaume UTF8")
        print("3 : Vous choisissez de vous téléporter en tant qu'administrateur dans le royaume UTF8")
        tp = input("Que voulez vous faire ? : ")
        if tp == "1":
            print("BOUM")
        elif tp == "2":
            print("T mor")
            exit()
        elif tp == "3":
            print("Face à vous se trouve le Boss du royaume ( BOSS : NAME : UTF8MB4 HP : 1750 ATTACK : 600 DEFENSE : 400) vous possédez plusieurs droits admin :")
            print("1 : Vous utilisez /kill UTF8MB4")
            print("2 : Vous utilisez /ipconfig UTF8MB4")
            print("3 : Vous utilisez /lobby")
            adm = input("Quelle commande allez vous éxecuter ? : ")
            if adm == "1":
                print("Vous avez vaincu le boss UTF8MB4 QUEL BOSS BRAVO")
                player.gain_xp(500)
            elif adm == "2":
                print("Dommage si pres du but t mor")
                exit()
            elif adm == "3":
                print("T'es perdu là")

                
def le_chateau_de_wamp(player):
    scroll_text("Vous apparaissez face à un Enderman'brrrrr hrrr'")
    print("1. Vous vous imposez face à l'Enderman ")
    print("2. Vous passez devant lui sans le regarder")
    chateau = input("Que souhaitez vous faire? : ")
    if chateau == "1":
        print("L'Enderman vous téléporte dans le vide")
        player.health = player.health - 100
        player.show_healthbar()
    elif chateau == "2":
        print("Vous accédez au château de Wamp")
        print("Arrivé à l'intérieur, plusieurs choix s'offrent à vous :")
        print("1. Vous empruntez le grand escalier face à vous")
        print("2. Vous apercevez une bibliothèque suspecte à votre gauche et décidez de passer derrière elle.")
        print("3.  Une tenue de garde Wamp est vêtue sur un mannequin à l'entrée et vous décidez de vous habiller avec.")
        into_chateau = input("Que souhaitez vous faire ? :")
        if into_chateau == "1":
            print("L'escalier ne mène à rien et vous retournez à l'entrée")
        elif into_chateau == "2":
            print("vous mourrez en vous faisant écraser par la bibliothèque")
            player.health = player.health - 100 
            player.show_healthbar()
        elif into_chateau == "3":
            print("Vous continuez à parcourir les couloirs du château")
            print("Un garde Wamp vient vous aborder 'Qui es-tu ? Je ne t'ai jamais vu ici.'")
            print("1. 'Salut, je suis nouveau. Saurais-tu où se trouve le Wamp'")
            print("2. 'Je fais partie des nouvelles recrues de Wamp. Sais-tu où se trouve le grand mâge du château ?'")
            garde_wamp = input("Que souhaitez vous faire? : ")
            if garde_wamp == "1":
                print("'Nous n'avons pas le droit de rencontrer Mr Wamp, retournez faire votre garde !'")
            elif garde_wamp == "2" :
                print("'Oui bien sûr, suis moi !'")
                print("Vous accédez à la chambre du Mâge")
                print("Le Mâge 'De quoi as-tu besoin ?'")
                print("1. 'Donne moi une potion d'invisibilité'")
                print("2. 'Donne moi une potion d'invincibilité'")
                mage = input("Que souhaitez vous faire ?")
                if mage == "1":
                    print("Vous possédez maintenant une potion d'invisibilité")
                    player.add_item(potion_invisibilite)
                elif mage == "2":
                    print("Vous possédez maintenant une potion d'invincibilité")
                    player.add_item(potion_invincibilite)
                    print("Le Mâge 'Avez-vous besoin d'autre chose ?")
                    print("1. 'Il me faudrait le code d'accès à la Wamp Cave'")
                    print("2. 'Où se trouve la Wamp Cave ?'")
                    mage2 = input("Que souhaitez vous faire ?")
                    if mage2 == "1":
                        print("'Je n'ai pas le droit, retourne faire ta garde'")
                    elif mage2 == "2":
                        print("'Prends ce plan, il t'y mènera'")
                        player.add_item(wamp_cave_plan)
                        print("Après avoir suivi les indications du plan, vous vous retrouvez devant la porte de la Wamp Cave")
                        print("1. Vous frappez à la porte")
                        print("2. Vous ingurgitez la potion que vous a donné le grand mâge précédemment")
                        wamp_cave = input("Que souhaitez vous faire ?")
                        if wamp_cave == "1":
                            print("Vous mourrez d'électrocution en touchant la porte")
                            player.health = player.health - 100
                            player.show_healthbar()
                        elif wamp_cave == "2":
                            print("Vous utilisez la potion que vous a donné le grand mâge")
                            print("Vous apercevez une évacuation d'air provenant de la Wamp Cave")
                            print("1. Vous décidez d'enlever la grille et d'accéder au conduit de ventilation")
                            print("2. Vous cherchez un autre endroit afin d'accéder à la Wamp Cave")
                            wamp_cave2 = input("Que souhaitez vous faire? : ")
                            if wamp_cave2 == "1":
                                print("Vous voilà dans le plafond de la Wamp Cave")
                            elif wamp_cave2 == "2":
                                print("Vous finissez par vous faire repérer par Wamp dans un endroit interdit et vous a renvoyé à l'entrée du château")
                                print("Vous voulez attaquer Wamp, mais vous ne savez pas comment vous y prendre")
                                print("1. Vous essayez de vaincre Wamp discrètement en lui infligeant un coup par derrière")
                                print("2. Vous proposez directement un combat à Wamp")
                                wamp_combat = input("Que souhaitez vous faire :")
                                if wamp_combat == "1":
                                    print("Vous avez perdu votre chance de vaincre Wamp")
                                elif wamp_combat == "2":
                                    print("Vous attaquez Wamp")
                                    wamp_combat = Enemy("Wamp", 1000, 150, 75, 300)
                                    start_combat(player, wamp_combat)

regions = {
    "0": "Retour au menu principal",
    "1": "La Montagne de l'Enfer",
    "2": "Le Vaisseau Amiral",
    "3": "Le parc MCD",
    "4": "La forêt MariaDB",
    "5": "Le Chateau de WAMP"
}

def explore_region(player):
    screen_transition(style="purple")
    while True:
        if player.check_if_dead():
            print("[bold red]Vous devez restaurer vos HP avant de continuer.[/bold red]")
            break
        print("\n[bold cyan]Menu Principal d'Exploration[/bold cyan]")
        print(Columns([
            Panel("[bold]1. Explorer une zone\n2. Afficher l'inventaire\n"
                  "3. Gérer le compte\n4. Se déconnecter[/bold]", 
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
            if player.check_if_dead():
                print("[bold red]Vous êtes mort ! Vous ne pouvez pas explorer une région tant que vos HP ne sont pas positifs.[/bold red]")
                continue
            while True:
                print("\n[bold]Carte des Zones d'Exploration[/bold]")
                for key, value in regions.items():
                    print(f"[bold]{key}.[/bold] {value}")
                
                zone_choice = input("\nChoisissez une zone à explorer (0 pour annuler) : ")
                
                if zone_choice == "0":
                    break
                elif zone_choice == "1":
                    if '1' in player.completed_regions:
                        print("[bold red]Vous avez déjà exploré cette région ![/bold red]")
                        continue
                    la_montagne_de_lenfer(player)
                    player.completed_regions.append('1')
                elif zone_choice == "2":
                    if '2' in player.completed_regions:
                        print("[bold red]Vous avez déjà exploré cette région ![/bold red]")
                        continue
                    le_vaisseau_amiral(player)
                    player.completed_regions.append('2')
                elif zone_choice == "3":
                    if '3' in player.completed_regions:
                        print("[bold red]Vous avez déjà exploré cette région ![/bold red]")
                        continue
                    le_parc_mcd(player)
                    player.completed_regions.append('3')
                elif zone_choice == "4":
                    if '4' in player.completed_regions:
                        print("[bold red]Vous avez déjà exploré cette région ![/bold red]")
                        continue
                    la_foret_maria_db(player)
                    player.completed_regions.append('4')
                elif zone_choice == "5":
                    if '5' in player.completed_regions:
                        print("[bold red]Vous avez déjà exploré cette région ![/bold red]")
                        continue
                    le_chateau_de_wamp(player)
                    """ player.completed_regions.append('5') """
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
            player.show_account_menu()
        
        elif main_choice == "4":
            print("\nRetour au menu principal...")
            break
        
        else:
            print("[bold red]Choix invalide ![/bold red]")
        
        # Sauvegarder après chaque action
        player.save_to_file()

if __name__ == "__main__":
    console = Console()
    first_time = True
    with console.status("[bold green]Chargement du jeu...[/bold green]", spinner="dots12"):
        time.sleep(2)
    show_animated_ascii()
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
            Panel("[bold green]4. Rechercher un joueur\n5. Classement[/bold green]\n[bold magenta]6. Afficher la carte[/bold magenta]", 
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
            print("\n[bold yellow]Au revoir, merci d'avoir joué ![/bold yellow]")
            break
        elif choice == "4":
            search_player_stats()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == "5":
            show_leaderboard()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == "6":
            show_game_map()
        else:
            print("[bold red]Option invalide![/bold red]")
            time.sleep(1)