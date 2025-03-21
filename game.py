from character import Warrior, Mage, Thief
from dice import Dice
from ui import UI

if __name__ == "__main__":
    print("\n--- RPG Battle Begins! ---\n")

    char_1 = Warrior("James", 20, 8, 3, Dice("red", 6))
    char_2 = Mage("Elsa", 20, 8, 3, Dice("blue", 6))

    print(char_1)
    print(char_2)

    round_num = 1
    while char_1.is_alive() and char_2.is_alive():
        print(f"\n--- Round {round_num} ---\n")
        
        # attaque du perso 1
        dmg = char_1.attack(char_2)
        UI.show_damage(char_2, dmg)
        
        if not char_2.is_alive():
            break
        
        # attaque du perso 2
        dmg = char_2.attack(char_1)
        UI.show_damage(char_1, dmg)
        
        round_num += 1
    
    # fin du combat
    if char_1.is_alive():
        print(f"\n🏆 {char_1.name} wins the battle! 🏆")
        char_1.gain_experience(50)
        UI.show_experience(char_1, 50)
    else:
        print(f"\n🏆 {char_2.name} wins the battle! 🏆")
        char_2.gain_experience(50)
        UI.show_experience(char_2, 50)