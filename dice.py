import random

class Dice:
    def __init__(self, color, faces):
        self.color = color
        self.faces = faces

    def __str__(self):
        return f"I'm {self.color} dice with {self.faces} faces"

    def __eq__(self, another_dice):
        return self.faces == another_dice.faces

    def roll(self):
        return random.randint(1, self.faces)

class RiggedDice(Dice):
    def roll(self):
        return self.faces

class ElementalDice(Dice):
    #dé qui peut appliquer des effets en plus
    ELEMENTS = ["Fire", "Ice", "Lightning", "Poison"]

    def roll(self):
        roll_value = super().roll()
        if random.random() < 0.3:  # 30% de chance d'avoir un effet
            element = random.choice(self.ELEMENTS)
            print(f"🔥 Elemental effect triggered: {element}!")
            return roll_value, element
        return roll_value, None

if __name__ == "__main__":
    d1 = Dice("red", 6)
    d2 = ElementalDice("blue", 10)

    for _ in range(3):
        print(f"Standard dice roll: {d1.roll()}")

    print("---")
    for _ in range(3):
        roll_value, element = d2.roll()
        if element:
            print(f"Elemental dice roll: {roll_value} with {element} effect!")
        else:
            print(f"Elemental dice roll: {roll_value}")

    d1_rigged = RiggedDice("green", 20)
    print(f"Rigged dice roll: {d1_rigged.roll()}")