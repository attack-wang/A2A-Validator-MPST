'''
level.py
The Level class: one dungeon floor with tiles, entities and key positions.
'''
import settings
class Level:
    """Holds one dungeon floor: tile grid, entities and key positions."""
    def __init__(self, number, grid, start, door, monsters, chests):
        self.number = number
        self.grid = grid
        self.start = start
        self.door = door
        self.monsters = monsters
        self.chests = chests
        self._monster_map = {(m.x, m.y): m for m in monsters}
        self._chest_map = {(c.x, c.y): c for c in chests}
    def tile_at(self, x, y):
        """Return the tile identifier at grid coordinates (x, y)."""
        return self.grid[y][x]
    def in_bounds(self, x, y):
        """Return True if (x, y) lies inside the grid."""
        return 0 <= x < settings.GRID_WIDTH and 0 <= y < settings.GRID_HEIGHT
    def is_wall(self, x, y):
        """Return True if the tile at (x, y) is a wall (out of bounds counts as wall)."""
        if not self.in_bounds(x, y):
            return True
        return self.tile_at(x, y) == settings.TILE_WALL
    def is_door(self, x, y):
        """Return True if (x, y) is the level exit door."""
        return (x, y) == self.door
    def monster_at(self, x, y):
        """Return the monster occupying (x, y), or None."""
        return self._monster_map.get((x, y))
    def chest_at(self, x, y):
        """Return the chest occupying (x, y), or None."""
        return self._chest_map.get((x, y))
    def remove_monster(self, monster):
        """Remove a defeated monster from the level."""
        self.monsters.remove(monster)
        self._monster_map.pop((monster.x, monster.y), None)
    def remove_chest(self, chest):
        """Remove an opened chest from the level."""
        self.chests.remove(chest)
        self._chest_map.pop((chest.x, chest.y), None)