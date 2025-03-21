from character import Character
from dice import Dice
from ui import Damages


if __name__ == "__main__":
    print("\n")

    char_1 = Character("Jamessss", 20, 8, 3, Dice("red", 6))
    char_2 = Character("Elsaaaa", 20, 8, 3, Dice("red", 6))

    while (char_1.is_alive() and char_2.is_alive()):
        dmg = char_1.attack()
        char_2.defend(dmg)

        dmg = char_2.attack()
        char_1.defend(dmg)