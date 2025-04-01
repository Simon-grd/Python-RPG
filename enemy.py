# enemy.py
import random
from rich.console import Console
from player import Player  # Pour taper dans la fonction de combat

class Enemy:
    def __init__(self, name, health, attack, defense, xp_reward):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.xp_reward = xp_reward

    def check_if_dead(self):
        return self.health <= 0

    def show_health(self):
        filled = self.health // 10
        empty = (self.max_health - self.health) // 10
        return f"[{'❤️' * filled}{'♡' * empty}] {self.health}/{self.max_health} PV"

def start_combat(player, enemy):
    console = Console()
    console.clear()
    player_parry_cooldown = 0
    enemy_parry_cooldown = 0
    player_parry_active = False
    enemy_parry_active = False

    while not player.check_if_dead() and not enemy.check_if_dead():
        console.print(f"\n[bold cyan]{player.ign}[/bold cyan] - Santé : {player.show_healthbar()}")
        console.print(f"[bold red]{enemy.name}[/bold red] - Santé : {enemy.show_health()}")
        print("\n[bold]Que voulez-vous faire ?[/bold]")
        print("1. Attaquer")
        print("2. Utiliser un objet")
        print(f"3. Parer {'(disponible)' if player_parry_cooldown == 0 else f'(cooldown {player_parry_cooldown} tours)'}")
        action = input("\nChoisissez une action : ")

        if action == "1":
            if enemy_parry_active:
                console.print(f"[bold cyan]{enemy.name} pare votre attaque ![/bold cyan]")
                enemy_parry_active = False
            else:
                damage = max(int((player.attack * random.uniform(1.0, 1.5)) - (enemy.defense * 0.5)), 1)
                enemy.health -= damage
                console.print(f"[bold green]Vous infligez {damage} dégâts à {enemy.name} ![/bold green]")
        elif action == "2":
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
            player_parry_active = True
            player_parry_cooldown = 3
            console.print("[bold cyan]Vous vous préparez à parer ![/bold cyan]")
        else:
            console.print("[red]Action invalide ou indisponible ![/red]")

        if enemy.check_if_dead():
            break

        if random.random() < 0.3 and enemy_parry_cooldown == 0:
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

        if player_parry_cooldown > 0:
            player_parry_cooldown -= 1
        if enemy_parry_cooldown > 0:
            enemy_parry_cooldown -= 1

    console.clear()
    if not player.check_if_dead():
        console.print(f"[bold green]Victoire ! Vous avez vaincu {enemy.name} et gagné {enemy.xp_reward} XP ![/bold green]")
        player.gain_xp(enemy.xp_reward)
    else:
        console.print(f"[bold red]Défaite... {enemy.name} vous a vaincu.[/bold red]")
