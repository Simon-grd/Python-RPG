from rich import print

class UI:
    @staticmethod
    def show_damage(character, damage):
        print(f"[red]{character.name} takes {damage} damage!")

    @staticmethod
    def show_heal(character, heal):
        print(f"[bold green]{character.name} heals {heal} HP!")

    @staticmethod
    def show_experience(character, exp):
        print(f"[blue]{character.name} gains {exp} experience!")

    @staticmethod
    def show_status(character):
        print(f"[purple]{character.name} [level {character.level}, {character.hp}/{character.max_hp} HP] [/purple]")
    
    @staticmethod
    def show_inventory(character): 
        print(f"[yellow]{character.name}'s inventory: {', '.join(character.inventory)}[/yellow]")
    
    @staticmethod
    def show_menu(character):
        print(f"[light blue]Choose an action for {character.name}:[/light blue]")
        print("1. Attack")
        print("2. Use Item")
        print("3. View Status")
        print("4. View Inventory")
        print("5. Quit")
