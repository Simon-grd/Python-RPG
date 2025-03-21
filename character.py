from dice import Dice
import random


class Character:
    label = "character"

    def __init__(self, name, max_hp, attack_value, defend_value, dice):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_value = attack_value
        self.defend_value = defend_value
        self.dice = dice
        self.level = 1
        self.experience = 0
        self.inventory = []

    def __str__(self):
        return f"I'm {self.name} the {self.label}, Level {self.level}."

    def is_alive(self):
        return self.hp > 0

    def decrease_hp(self, amount):
        self.hp -= max(amount, 0)
        self.show_healthbar()

    def show_healthbar(self):
        print(f"({'❤️' * self.hp}{'♡' * (self.max_hp - self.hp)} {self.hp}/{self.max_hp} hp)")

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 100:  # il faut avoir 100 xp pour up
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 5
        self.attack_value += 2
        self.defend_value += 1
        self.hp = self.max_hp
        self.experience = 0
        print(f"{self.name} leveled up! Now Level {self.level}!")

    def compute_damages(self, roll):
        damages = self.attack_value + roll
        return damages

    def attack(self, target):
        roll = self.dice.roll()
        damages = self.compute_damages(roll)
        print(
            f"{self.name} [red]attacks[/red] with {damages} damage ({self.attack_value} atk + {roll} rng)")
        target.defend(damages)

    def compute_defend(self, damages, roll):
        return max(damages - self.defend_value - roll, 0)

    def defend(self, damages):
        roll = self.dice.roll()
        wounds = self.compute_defend(damages, roll)
        print(f"{self.name} [green]defends[/green] and takes {wounds} wounds!")
        self.decrease_hp(wounds)


class Warrior(Character):
    label = "warrior"

    def compute_damages(self, roll):
        print("🪓 Warrior bonus: +3 dmg")
        return super().compute_damages(roll) + 3

    def level_up(self):
        super().level_up()
        self.attack_value += 2  # bonus d'attaque sa mère
        print("Warrior's strength increased!")


class Mage(Character):
    label = "mage"
    mana = 10

    def compute_defend(self, damages, roll):
        print("🔮 Mage bonus: -3 wounds")
        return max(super().compute_defend(damages, roll) - 3, 0)

    def cast_spell(self, target):
        if self.mana >= 5:
            spell_damage = random.randint(5, 15)
            print(f"{self.name} casts a spell for {spell_damage} damage!")
            target.defend(spell_damage)
            self.mana -= 5
        else:
            print(f"{self.name} is out of mana!")

    def level_up(self):
        super().level_up()
        self.mana += 5
        print("Mage's mana increased!")


class Thief(Character):
    label = "thief"

    def attack(self, target):
        roll = self.dice.roll()
        if random.random() < 0.3:
            print("💀 Thief performs a sneak attack!")
            roll *= 2
        damages = self.attack_value + roll
        print(
            f"{self.name} [red]attacks[/red] ignoring defense! {damages} damage dealt.")
        target.decrease_hp(damages)

    def level_up(self):
        super().level_up()
        print("Thief's agility increased!")


if __name__ == "__main__":
    print("\n")

    char_1 = Warrior("James", 20, 8, 3, Dice("red", 6))
    char_2 = Mage("Elsa", 20, 8, 3, Dice("red", 6))

    print(char_1)
    print(char_2)

    char_1.attack(char_2)
    char_2.cast_spell(char_1)
