import random
from collections import deque
import settings
class Room:
    def __init__(self, x, y, w, h):
        self.x = x; self.y = y; self.w = w; self.h = h
    @property
    def center(self): return (self.x + self.w // 2, self.y + self.h // 2)
    def intersects(self, other, padding=1):
        return (self.x - padding < other.x + other.w and
                self.x + self.w + padding > other.x and
                self.y - padding < other.y + other.h and
                self.y + self.h + padding > other.y)
class MapGenerator:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate(self, level):
        while True:
            grid = self._empty_grid()
            rooms = self._place_rooms(grid)
            if len(rooms) >= 4:
                break
        self._connect_rooms(grid, rooms)
        start = rooms[0].center
        door_room = self._pick_door_room(grid, rooms, start)
        door = door_room.center
        # ensure door tile is floor (center always is, since room carved)
        path = self._bfs_path(grid, start, door)
        if path is None:
            self._carve_corridor(grid, start, door)
        monsters = self._place_monsters(grid, level, start, door)
        chests = self._place_chests(grid, level, start, door, monsters)
        return {...}