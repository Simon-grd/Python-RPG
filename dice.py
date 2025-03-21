import random


class Dice:
    def __init__(self, color, faces):
        self.color = color
        self.faces = faces

    def __str__(self):
        return f"I'm {self.color} a dice with {self.faces} faces"

    def __eq__(self, another_dice):
        if self.faces == another_dice.faces:
            return True
        return False

    def roll(self):
        return random.randint(1, self.faces)


class RiggedDice(Dice):
    def roll(self):
        return self.faces


if __name__ == "__main__":
    d1 = Dice("red", 6)
    d2 = Dice("red", 10)

    for _ in range(3):
        print(d1.roll())

    print("---")

    for _ in range(3):
        print(d2.roll())

    d1_rigged = RiggedDice("green", 20)
    print(d1_rigged.roll())
