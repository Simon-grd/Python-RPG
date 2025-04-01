# menu.py
import os
import time
import bcrypt
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from player import Player
from character import fairy, wizard, elf, goblin, valkyrie

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
                    from character import fairy
                    player = Player(player_name, fairy, password_hash)
                    break
                elif character_type_choice == "2":
                    from character import wizard
                    player = Player(player_name, wizard, password_hash)
                    break
                elif character_type_choice == "3":
                    from character import elf
                    player = Player(player_name, elf, password_hash)
                    break
                elif character_type_choice == "4":
                    from character import goblin
                    player = Player(player_name, goblin, password_hash)
                    break
                elif character_type_choice == "5":
                    from character import valkyrie
                    player = Player(player_name, valkyrie, password_hash)
                    break
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
                return player

def login():
    console = Console()
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
        except:
            with open("players.txt", "r", encoding="latin-1") as file:
                lines = file.readlines()
        for line in lines:
            if line.startswith(username + " "):
                fields = line.strip().split()
                if len(fields) >= 8 and username == fields[0]:
                    if bcrypt.checkpw(password.encode('utf-8'), fields[1].encode('utf-8')):
                        player_found = True
                        from character import CharacterType
                        character_type = CharacterType(fields[2], int(fields[3]), int(fields[4]), int(fields[5]))
                        user = Player(fields[0], character_type, fields[1].encode('utf-8'))
                        user.level = int(fields[6])
                        user.xp = int(fields[7])
                        user.attack = int(fields[3])
                        user.defense = int(fields[5])
                        user.max_health = int(fields[4])
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

def search_player_stats():
    username = input("\nEntrez le pseudo à rechercher : ")
    found = False
    try:
        try:
            with open("players.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
        except:
            with open("players.txt", "r", encoding="latin-1") as file:
                lines = file.readlines()
        for line in lines:
            if line.startswith(username + " "):
                fields = line.strip().split()
                player_data = {
                    "NomUtilisateur": fields[0],
                    "TypePersonnage": fields[2],
                    "Attaque": int(fields[3]),
                    "Santé": int(fields[4]),
                    "Défense": int(fields[5]),
                    "Niveau": int(fields[6]),
                    "XP": int(fields[7]),
                    "Rang": Player(fields[0], None, "").get_rank()  # Simplifié pour l'affichage
                }
                from ui import display_player_stats
                display_player_stats(player_data)
                found = True
                break
    except FileNotFoundError:
        pass
    if not found:
        print(f"\n[bold red]Aucun joueur trouvé avec le pseudo '{username}'[/bold red]")

def show_leaderboard():
    players = []
    try:
        try:
            with open("players.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
        except:
            with open("players.txt", "r", encoding="latin-1") as file:
                lines = file.readlines()
        for line in lines:
            fields = line.strip().split()
            if len(fields) >= 8:
                players.append({
                    "username": fields[0],
                    "class": fields[2],
                    "level": int(fields[6]),
                    "xp": int(fields[7])
                })
        players.sort(key=lambda x: (-x["level"], -x["xp"]))
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Position", style="cyan")
        table.add_column("Pseudo", style="green")
        table.add_column("Classe")
        table.add_column("Niveau", justify="right")
        table.add_column("XP", justify="right")
        for idx, player in enumerate(players[:10], 1):
            pos = f"{idx}ère" if idx == 1 else f"{idx}ème"
            table.add_row(pos, player["username"], player["class"], str(player["level"]), f"{player['xp']:,}")
        print(Panel(table, title="[bold yellow]Classement des Joueurs[/bold yellow]"))
    except FileNotFoundError:
        print("[red]Aucun joueur enregistré ![/red]")
