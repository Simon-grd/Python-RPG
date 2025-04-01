# main.py
from rich import print
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
import time
from animation import show_animated_ascii
import os

from menu import create_player, login, search_player_stats, show_leaderboard
from map import show_game_map, la_montagne_de_lenfer, le_vaisseau_amiral, le_parc_mcd, la_foret_maria_db, le_chateau_de_wamp

ascii_art = r"""
   ___                   ____      __        __         _     _ 
  / _ \ _ __   ___ _ __ |  _ \ _   \ \      / /__  _ __| | __| |
 | | | | '_ \ / _ \ '_ \| |_) | | | \ \ /\ / / _ \| '__| |/ _` |
 | |_| | |_) |  __/ | | |  __/| |_| |\ V  V / (_) | |  | | (_| |
  \___/| .__/ \___|_| |_|_|    \__, | \_/\_/ \___/|_|  |_|\__,_|
       |_|                     |___/                            
"""

def main_menu():
    console = Console()
    first_time = True
    while True:
        if first_time:
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
            Panel("[bold green]4. Rechercher un joueur\n5. Classement\n6. Afficher la carte[/bold green]", 
                  title="Autres Options", border_style="blue")
        ]))
        choice = input("\nSélectionnez une option : ")
        if choice == "1":
            create_player()
        elif choice == "2":
            player = login()
            if player:
                # Boucle d'exploration
                while True:
                    print("\n[bold cyan]Menu Principal d'Exploration[/bold cyan]")
                    print(Columns([
                        Panel("[bold]1. Explorer une zone\n2. Afficher l'inventaire\n3. Gérer le compte\n4. Se déconnecter[/bold]", title="Options", border_style="yellow"),
                        Panel(f"[bold green]Santé:[/bold green] {player.health}\n[bold red]Attaque:[/bold red] {player.attack}\n[bold blue]Défense:[/bold blue] {player.defense}", title="Stats", border_style="blue")
                    ]))
                    main_choice = input("\nChoisissez une action : ")
                    if main_choice == "1":
                        if player.check_if_dead():
                            print("[bold red]Vous êtes mort ! Vous ne pouvez pas explorer une région tant que vos HP ne sont pas positifs.[/bold red]")
                            continue
                        print("\n[bold]Carte des Zones d'Exploration[/bold]")
                        print("0. Retour au menu principal")
                        print("1. La Montagne de l'Enfer")
                        print("2. Le Vaisseau Amiral")
                        print("3. Le parc MCD")
                        print("4. La forêt MariaDB")
                        print("5. Le Chateau de WAMP")
                        zone_choice = input("\nChoisissez une zone à explorer (0 pour annuler) : ")
                        if zone_choice == "0":
                            continue
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
                            player.completed_regions.append('5')
                        else:
                            print("[bold red]Choix invalide ![/bold red]")
                    elif main_choice == "2":
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
                    player.save_to_file()
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
            show_game_map(ascii_art)
        else:
            print("[bold red]Option invalide![/bold red]")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
