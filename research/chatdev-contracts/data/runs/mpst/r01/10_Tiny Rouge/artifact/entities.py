'''
entities.py
Data classes for the actors that populate the tower.
`Player`  – keeps track of the hero's grid position and hit points.
`Monster` – a simple container describing one monster standing on a tile
            (name + HP); combat subtracts its HP from the player's HP.
'''
class Player:
    """The hero.  Moves on floor tiles, fights monsters, opens chests."""
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
    @property
    def position(self):
        return (self.x, self.y)
    def move_to(self, x, y):
        self.x = x
        self.y = y
    def heal(self, amount):
        self.hp += amount
    def take_damage(self, amount):
        self.hp -= amount
    def is_alive(self):
        return self.hp > 0
class Monster:
    """One monster guarding a floor tile."""
    def __init__(self, name, hp, x, y):
        self.name = name
        self.hp = hp
        self.x = x
        self.y = y
    @property
    def position(self):
        return (self.x, self.y)