# character.py
class CharacterType:
    def __init__(self, name, attack, health, defense):
        self.name = name
        self.attack = attack
        self.health = health
        self.defense = defense

# Types de personnages disponibles
fairy = CharacterType("Fée", 100, 1150, 100)
wizard = CharacterType("Magicien", 275, 900, 175)
elf = CharacterType("Elfe", 200, 1000, 150)
goblin = CharacterType("Gobelin", 125, 1000, 225)
valkyrie = CharacterType("Valkyrie", 250, 850, 250)
