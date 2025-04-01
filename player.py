# player.py
import os
import time
import random
import bcrypt
from rich import print
from rich.panel import Panel
from rich.columns import Columns
from rich.box import ROUNDED
from rich.console import Console
from animation import animate_xp_gain

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
            self.active_effects[item.effect_type] = {'value': item.value, 'duration': effect_duration}
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
            f"[green]▮[/green]" * filled_blocks + f"[white]▯[/white]" * empty_blocks +
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
            animate_xp_gain(prev_xp, self.xp, self.calculate_level())
        while self.xp >= self.calculate_level():
            self.level_up()
        self.save_to_file()

    def save_to_file(self):
        with open("players.txt", "r") as f:
            lines = f.readlines()
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
        if not player_found:
            new_lines.append(f"{self.ign} {self.password_hash.decode()} {self.character_type.name} " \
                           f"{self.attack} {self.max_health} {self.defense} " \
                           f"{self.level} {self.xp} {','.join(self.completed_regions)}\n")
        with open("players.txt", "w") as f:
            f.writelines(new_lines)

    def set_username(self, new_username):
        old_username = self.ign
        self.ign = new_username
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
        self.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.save_to_file()
        print("[bold green]Mot de passe modifié avec succès ![/bold green]")

    def show_account_menu(self):
        while True:
            from rich.columns import Columns
            from rich.panel import Panel
            print(Columns([
                Panel("[bold]1. Changer le nom d'utilisateur\n2. Changer le mot de passe\n3. Retour[/bold]", 
                      title="Gestion du Compte", border_style="cyan"),
                Panel(f"[italic]Nom actuel:[/italic] [bold]{self.ign}[/bold]\n[italic]Classe:[/italic] {self.character_type.name}",
                      border_style="yellow")
            ]))
            choice = input("\nChoisissez une option : ")
            if choice == "1":
                new_name = input("Nouveau nom d'utilisateur : ")
                if new_name == self.ign:
                    print("[yellow]C'est déjà votre nom actuel ![/yellow]")
                    continue
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
