'''
settings.py
Global configuration constants for the Tower of the Sorcerer inspired roguelike.
'''
# --- Grid / window -------------------------------------------------------
GRID_WIDTH = 80
GRID_HEIGHT = 80
TILE_SIZE = 10
SIDEBAR_WIDTH = 280
WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE + SIDEBAR_WIDTH   # 1080
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE                 # 800
FPS = 30
# --- Tile codes ----------------------------------------------------------
WALL = 0
FLOOR = 1
DOOR = 2
# --- Player --------------------------------------------------------------
PLAYER_START_HP = 100
TREASURE_MIN_HEAL = 20
TREASURE_MAX_HEAL = 30
# --- Level generation ----------------------------------------------------
MAZE_BRAID_CHANCE = 0.10      # base probability of opening a dead-end wall
ROOMS_PER_LEVEL = 5
MONSTERS_BASE = 14            # monsters on level 1
MONSTERS_PER_LEVEL = 4        # extra monsters each level
TREASURES_BASE = 6
TREASURES_PER_LEVEL = 1
MONSTER_HP_SCALING = 5        # extra HP added to every monster per level
# --- Monster catalogue ---------------------------------------------------
# (name, base hp, color)
MONSTER_TYPES = [
    {"name": "Green Slime", "hp": 10, "color": (80, 200, 80)},
    {"name": "Red Bat",     "hp": 15, "color": (220, 70, 70)},
    {"name": "Skeleton",    "hp": 25, "color": (230, 230, 230)},
    {"name": "Blue Wizard", "hp": 35, "color": (70, 120, 230)},
    {"name": "Demon",       "hp": 50, "color": (160, 40, 200)},
]
# --- Colors --------------------------------------------------------------
COLOR_BACKGROUND = (15, 15, 25)
COLOR_WALL = (70, 70, 85)
COLOR_FLOOR = (205, 205, 200)
COLOR_DOOR = (60, 200, 90)
COLOR_PLAYER = (30, 90, 220)
COLOR_TREASURE = (235, 185, 40)
COLOR_SIDEBAR = (30, 30, 45)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (160, 160, 170)
COLOR_HP_BAR_BG = (90, 30, 30)
COLOR_HP_BAR_FG = (60, 200, 80)
COLOR_GAME_OVER = (180, 40, 40)
# --- Fonts ---------------------------------------------------------------
FONT_NAME = None  # pygame default
FONT_SIZE_SMALL = 16
FONT_SIZE_MEDIUM = 20
FONT_SIZE_LARGE = 30