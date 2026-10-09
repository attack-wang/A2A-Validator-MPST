"""Global configuration constants for the Tower of the Sorcerer roguelike.
All geometry, tile codes, colors, gameplay numbers and generation limits
live here so the rest of the code stays free of magic values.
Coordinate convention used across the whole project: (row, col), where
row grows downward and col grows rightward.
"""
# --- Window / map geometry ---
MAP_SIZE = 80           # fixed 80x80 grid (task requirement)
TILE_SIZE = 10          # pixels per tile
MAP_PIXEL_SIZE = MAP_SIZE * TILE_SIZE   # 800 x 800 play field
PANEL_WIDTH = 280       # side panel for the minimal UI
WINDOW_WIDTH = MAP_PIXEL_SIZE + PANEL_WIDTH  # 1080
WINDOW_HEIGHT = MAP_PIXEL_SIZE               # 800
FPS = 30
# --- Tile codes ---
TILE_WALL = 0
TILE_FLOOR = 1
TILE_DOOR = 2
# --- Gameplay numbers ---
PLAYER_START_MAX_HP = 100
HEAL_MIN = 20           # chest heals 20-30 HP (task requirement)
HEAL_MAX = 30
MAX_GEN_ATTEMPTS = 50   # level regeneration attempts before giving up
ROOMS_PER_LEVEL = 14    # extra rooms carved besides the main corridor
MONSTERS_PER_LEVEL_BASE = 10
MONSTERS_PER_LEVEL_SPREAD = 6
CHESTS_PER_LEVEL_BASE = 3
CHESTS_PER_LEVEL_SPREAD = 2
# --- Colors (R, G, B) ---
COLOR_BG = (18, 18, 24)
COLOR_WALL = (52, 58, 74)
COLOR_FLOOR = (198, 198, 178)
COLOR_DOOR = (60, 200, 90)
COLOR_PLAYER = (70, 130, 240)
COLOR_MONSTER = (220, 70, 70)
COLOR_CHEST = (230, 180, 40)
COLOR_PANEL_BG = (28, 30, 38)
COLOR_PANEL_TEXT = (230, 230, 230)
COLOR_HP_BAR_BG = (70, 70, 70)
COLOR_HP_BAR_FG = (60, 200, 90)
COLOR_TITLE = (240, 200, 90)
COLOR_MESSAGE = (180, 200, 230)
# --- Monster roster: (name, hp) scaled by floor depth ---
MONSTER_TYPES = [
    ("Slime", 10), ("Bat", 18), ("Spider", 25), ("Skeleton", 35),
    ("Ghost", 50), ("Orc", 65), ("Wraith", 85), ("Demon", 110), ("Dragon", 150),
]