'''
game.py
Core game logic: level state, player movement, combat resolution,
treasure chests and progression to the next floor.
'''
import random
import config
from entities import Player, Monster
from map_generator import MapGenerator
class Game:
    '''Holds the complete state of the current run and mutates it in
    response to player actions.'''
    def __init__(self, seed=None):
        '''Create a new game: player, level 1 map and populations.'''
        self.rng = random.Random(seed)
        self.generator = MapGenerator(seed)
        self.level = 1
        self.player = None
        self.grid = None
        self.start = None
        self.door = None
        self.monsters = {}      # (x, y) -> Monster
        self.chests = set()     # {(x, y), ...}
        self.encountered = []   # stat lines of monsters met this floor
        self.last_combat = None
        self.game_over = False
        self.victory = False
        self.messages = []
        self.build_level()
    # ------------------------------------------------------------------
    # Level construction
    # ------------------------------------------------------------------
    def build_level(self):
        '''Generate the map for the current level and populate it.'''
        grid, start, door, protected = self.generator.generate(self.level)
        self.grid = grid
        self.start = start
        self.door = door
        self.monsters = {}
        self.chests = set()
        self.encountered = []
        self.last_combat = None
        if self.player is None:
            self.player = Player(start[0], start[1])
        else:
            self.player.move_to(start[0], start[1])
        self._populate(protected)
        self.log(f"-- Floor {self.level}: find the green door! "
                 f"({len(self.monsters)} monsters, {len(self.chests)} chests)")
    def _populate(self, protected):
        '''Place monsters and chests on eligible floor tiles.
        Eligible tiles are FLOOR tiles that are not on the protected
        start->door corridor, not the start tile and not already used.
        '''
        size = config.GRID_SIZE
        eligible = [
            (x, y)
            for y in range(size)
            for x in range(size)
            if self.grid[y][x] == config.FLOOR
            and (x, y) != self.start
            and (x, y) not in protected
        ]
        self.rng.shuffle(eligible)
        n_monsters = min(
            config.MONSTERS_PER_LEVEL_BASE
            + (self.level - 1) * config.MONSTERS_PER_LEVEL_SCALE,
            len(eligible),
        )
        n_chests = min(
            config.CHESTS_PER_LEVEL_BASE
            + (self.level - 1) * config.CHESTS_PER_LEVEL_SCALE,
            len(eligible) - n_monsters,
        )
        monster_tiles = eligible[:n_monsters]
        chest_tiles = eligible[n_monsters:n_monsters + n_chests]
        for x, y in monster_tiles:
            monster = Monster.random(x, y, self.level, rng=self.rng)
            self.monsters[(x, y)] = monster
        for x, y in chest_tiles:
            self.chests.add((x, y))