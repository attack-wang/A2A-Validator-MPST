'''
door.py
Door entity marking the level exit. When the player steps onto the door tile
the current level is completed and the next floor of the tower is generated.
'''
class Door:
    '''The level exit. Reaching it advances to the next level.'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def pos(self):
        return (self.x, self.y)