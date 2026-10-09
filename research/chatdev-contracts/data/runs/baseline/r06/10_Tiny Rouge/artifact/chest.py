'''
chest.py
Treasure chest entity: touching it restores 20-30 HP.
'''
class Chest:
    """A treasure chest; touching it restores 20-30 HP."""
    def __init__(self, x, y, heal_amount):
        self.x = x
        self.y = y
        self.heal_amount = heal_amount