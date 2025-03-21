class UI:
    @staticmethod
    def show_damage(character, damage):
        print(f"[red]{character.name} takes {damage} damage![/red]")

    @staticmethod
    def show_heal(character, heal):
        print(f"[green]{character.name} heals {heal} HP![/green]")

    @staticmethod
    def show_experience(character, exp):
        print(f"[blue]{character.name} gains {exp} experience![/blue]")
