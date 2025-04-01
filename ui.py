# ui.py
from rich.panel import Panel
from rich import print

def display_player_stats(player_data):
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
