# item.py
class Item:
    def __init__(self, name, description, effect_type, value):
        self.name = name
        self.description = description
        self.effect_type = effect_type
        self.value = value

# Définition des objets
potion_invisibilite = Item("Potion d'invisibilité", "Une potion qui vous rend invisible", "defense", 1)
potion_invincibilite = Item("Potion d'invincibilité", "Une potion qui vous rend invincible", "defense", 999)
potion_sante = Item("Potion de Vitalité", "Une fiole contenant un liquide rougeoyant", "health", 100)
feuille_dor = Item("Feuille d'or", "Une feuille permettant vla les choses", "health", 1)
epee_mcd_attack = Item("Épée MCD", "Une épée légendaire très puissante", "attack", 889)
wamp_cave_plan = Item("Plan de la Wamp Cave", "Cette carte vous permettra de vous repérer dans le château de Wamp", "health", 1)
