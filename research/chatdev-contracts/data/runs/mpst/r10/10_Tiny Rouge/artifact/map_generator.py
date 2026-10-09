'''
map_generator.py
Procedural generation of the 80x80 tower floor: rooms, corridors, guaranteed
start->door path, monster and treasure chest placement.
'''
import random
from collections import deque
import config
from entities import Monster, TreasureChest
class GameMap:
    """Holds one tower floor: tile grid, spawn/door positions and entities."""
    def __init__(self, grid, start, door, monsters, chests):
        self.grid = grid
        self.start = start
        self.door = door
        self.monsters = monsters
        self.chests = chests
        self._entity_index = {(e.x, e.y): e for e in monsters + chests}
    def in_bounds(self, x, y):
        return 0 <= x < config.GRID_WIDTH and 0 <= y < config.GRID_HEIGHT
    def tile_at(self, x, y):
        return self.grid[y][x]
    def is_wall(self, x, y):
        return self.tile_at(x, y) == config.TILE_WALL
    def is_door(self, x, y):
        return self.tile_at(x, y) == config.TILE_DOOR
    def entity_at(self, x, y):
        return self._entity_index.get((x, y))
    def remove_entity(self, entity):
        self._entity_index.pop((entity.x, entity.y), None)
        if entity in self.monsters:
            self.monsters.remove(entity)
        if entity in self.chests:
            self.chests.remove(entity)
class MapGenerator:
    """Generates connected floors and guarantees a start->door path."""
    def generate(self, level, player_hp):
        """Produce a GameMap for the given level, or a safe fallback."""
        for _ in range(50):
            grid, rooms = self._carve_rooms_and_corridors()
            if grid is None:
                continue
            start, door, path = self._pick_start_and_door(grid, rooms)
            if path is None or len(path) < config.MIN_START_DOOR_DISTANCE:
                continue
            grid[door[1]][door[0]] = config.TILE_DOOR
            monsters, chests = self._place_entities(grid, path, level, player_hp)
            return GameMap(grid, start, door, monsters, chests)
        return self._fallback_map(level)