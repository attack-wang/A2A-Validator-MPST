'''
config.py
Global configuration constants for the Tower of the Sorcerer inspired
roguelike game.
'''
# --- Grid / rendering -------------------------------------------------
GRID_SIZE = 80          # Fixed 80x80 grid map.
TILE_SIZE = 8           # Pixel size of one grid tile on screen.
CANVAS_SIZE = GRID_SIZE * TILE_SIZE  # 640 px
# --- Terrain codes stored in the grid ---------------------------------
WALL = 0
FLOOR = 1
DOOR = 2
# --- Input ------------------------------------------------------------
# Directions mapped from W/A/S/D (and arrow keys) -> (dx, dy).
KEY_BINDINGS = {
    'w': (0, -1), 'W': (0, -1), 'Up': (0, -1),
    'a': (-1, 0), 'A': (-1, 0), 'Left': (-1, 0),
    's': (0, 1), 'S': (0, 1), 'Down': (0, 1),
    'd': (1, 0), 'D': (1, 0), 'Right': (1, 0),
}
# --- Player / gameplay balance ----------------------------------------
PLAYER_START_HP = 100
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30
MONSTER_TYPES = [
    ("Slime", 10),
    ("Bat", 15),
    ("Ghost", 20),
    ("Skeleton", 25),
    ("Demon", 30),
]
MONSTERS_PER_LEVEL_BASE = 40
MONSTERS_PER_LEVEL_SCALE = 10   # extra monsters per level
CHESTS_PER_LEVEL_BASE = 8
CHESTS_PER_LEVEL_SCALE = 2
LEVEL_HP_SCALE = 5  # extra monster HP per level beyond the first
# --- Colors -----------------------------------------------------------
COLOR_BG = "#111111"
COLOR_WALL = "#2b2b2b"
COLOR_FLOOR = "#e8e4d8"
COLOR_PLAYER = "#1e88e5"
COLOR_MONSTER = "#d32f2f"
COLOR_CHEST = "#fbc02d"
COLOR_DOOR = "#43a047"
COLOR_PANEL_BG = "#f5f5f5"
COLOR_TEXT = "#222222"
COLOR_GAME_OVER = "#b71c1c"
# --- Misc -------------------------------------------------------------
MAX_LOG_MESSAGES = 200