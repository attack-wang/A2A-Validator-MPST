'''
config.py
Central configuration for the Tower of the Sorcerer inspired roguelike.
Contains all tunable constants: grid dimensions, tile type codes,
ASCII symbols used by the console renderer, monster templates and
difficulty scaling rules.
This version uses ONLY the Python standard library (no pygame), so the
game runs on any machine with a plain Python interpreter.
'''
# --- Grid -----------------------------------------------------------
GRID_SIZE = 80          # fixed 80x80 grid map (customer requirement)
VIEW_WIDTH = 41         # console viewport width in tiles (odd -> player centred)
VIEW_HEIGHT = 21        # console viewport height in tiles
# --- Tile type codes -------------------------------------------------
TILE_WALL = 0
TILE_FLOOR = 1
TILE_DOOR = 2
# --- Player -----------------------------------------------------------
PLAYER_START_HP = 100
PLAYER_MAX_HP = 200
# --- Treasure chests ---------------------------------------------------
CHEST_HEAL_MIN = 20   # customer requirement: 20-30 HP restored
CHEST_HEAL_MAX = 30
# --- Monsters -----------------------------------------------------------
MONSTER_TEMPLATES = [
    {"name": "Slime",    "hp": 10, "symbol": "s"},
    {"name": "Bat",      "hp": 14, "symbol": "b"},
    {"name": "Skeleton", "hp": 24, "symbol": "k"},
    {"name": "Ghost",    "hp": 30, "symbol": "g"},
    {"name": "Golem",    "hp": 45, "symbol": "G"},
]
MONSTER_COUNT_BASE = 14
MONSTER_COUNT_PER_LEVEL = 4
MONSTER_HP_LEVEL_SCALE = 6
# --- Chests --------------------------------------------------------------
CHEST_COUNT_BASE = 5
CHEST_COUNT_PER_LEVEL = 1
# --- Wall scatter ---------------------------------------------------------
WALL_BLOB_COUNT = 90
WALL_BLOB_SIZE_MIN = 2
WALL_BLOB_SIZE_MAX = 6
# --- ASCII symbols used by the console renderer ----------------------------
SYM_WALL = "#"
SYM_FLOOR = "."
SYM_DOOR = "D"
SYM_PLAYER = "@"
SYM_CHEST = "$"
SYM_UNKNOWN = "?"
# --- UI ----------------------------------------------------------------
HP_BAR_WIDTH = 20
LOG_MAX_ENTRIES = 8