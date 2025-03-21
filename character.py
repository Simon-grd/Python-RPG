from dice import Dice

from rich import print


class Character:
    label = "character"

    def __init__(self, name, max_hp, attack_value, defend_value, dice):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.dice = dice

    def __str__(self):
        return f"I'm {self.name} the {self.label}."

    def is_alive(self):
        return self.hp > 0

    def decrease_hp(self, amount):
        self.hp -= amount
        self.show_healthbar()

    def show_healthbar(self):
        print(
            f"[{"❤️" * self.hp}{"♡" * (self.max_hp - self.hp)}] {self.hp}/{self.max_hp} hp")

    def compute_damages(self, roll):
        damages = self.attack_value + roll
        return damages

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(
            f"{self.name} [red]attack[/red] with {damages} damages ({self.attack_value} atk + {roll} rng)")
        target.defend(damages)

    def compute_defend(self, damages, roll):
        return damages - self.defend_value - roll

    def defend(self, damages):
        roll = self.dice.roll()
        wounds = self.compute_defend(damages, roll)
        print(f"{self.name} [green]defend[/green] against {damages} and take {wounds} wounds ({damages} dmg - {self.defend_value} def - {roll} rng)")
        self.decrease_hp(wounds)


class Warrior(Character):
    label = "warrior"

    def compute_damages(self, roll):
        print("🪓 Warrior bonus : +3 dmg")
        return super().compute_damages(roll) + 3


class Mage(Character):
    label = "mage"

    def compute_defend(self, damages, roll):
        print("🔮 Mage bonus : -3 wounds")
        return super().compute_defend(damages, roll) - 3
    

class Thief(Character):
    label = "thief"

    # ignore la défense de son adversaire (physique)


if __name__ == "__main__":
    print("\n")

    char_1 = Warrior("James", 20, 8, 3, Dice("red", 6))
    char_2 = Mage("Elsa", 20, 8, 3, Dice("red", 6))

    print(char_1)
    print(char_2)

    char_1.attack(char_2)

    # while (char_1.is_alive() and char_2.is_alive()):
    #     char_1.attack(char_2)
    #     char_2.attack(char_1)
