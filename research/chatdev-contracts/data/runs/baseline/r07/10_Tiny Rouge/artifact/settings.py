'''
settings.py
Global configuration: grid dimensions, tile size, gameplay balance
constants, monster tiers and the colour palette.
'''
# --- grid & window -------------------------------------------------
GRID_WIDTH = 80
GRID_HEIGHT = 80
TILE_SIZE = 12                      # pixels per tile -> 960x960 map
UI_WIDTH = 300                      # side panel width in pixels
WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE + UI_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE
# --- tile codes ------------------------------------------------------
WALL = 0
FLOOR = 1
# --- gameplay balance -------------------------------------------------
PLAYER_START_HP = 100
CHEST_HEAL_MIN = 20                 # chest restores 20-30 HP
CHEST_HEAL_MAX = 30
ROOMS_PER_LEVEL_MIN = 8
ROOMS_PER_LEVEL_MAX = 14
ROOM_MIN_SIZE = 5
ROOM_MAX_SIZE = 10
CORRIDOR_EXTRA_LINKS = 3
MONSTERS_BASE = 10
MONSTERS_PER_LEVEL = 4
CHESTS_BASE = 4
CHESTS_PER_LEVEL = 2
MONSTER_HP_PER_LEVEL = 6            # extra monster HP per dungeon level
MONSTER_TIERS = [
    {"name": "Slime",    "base_hp": 10, "color": (80, 200, 120)},
    {"name": "Bat",      "base_hp": 16, "color": (170, 120, 220)},
    {"name": "Skeleton", "base_hp": 24, "color": (220, 220, 200)},
    {"name": "Ghost",    "base_hp": 34, "color": (140, 190, 255)},
    {"name": "Demon",    "base_hp": 50, "color": (230, 80, 80)},
]
# --- fonts -----------------------------------------------------------
FONT_SIZE_TITLE = 26
FONT_SIZE_NORMAL = 18
FONT_SIZE_SMALL = 14
FONT_SIZE_TILE = 10
# --- colours ----------------------------------------------------------
COLOR_BG = (16, 18, 24)
COLOR_UI_BG = (10, 10, 14)
COLOR_UI_PANEL = (34, 36, 46)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (150, 150, 160)
COLOR_DANGER = (230, 80, 80)
COLOR_SUCCESS = (90, 200, 120)
COLOR_WALL = (60, 62, 76)
COLOR_FLOOR = (24, 26, 34)
COLOR_START = (50, 60, 90)
COLOR_DOOR = (240, 200, 60)
COLOR_CHEST = (200, 140, 40)
COLOR_PLAYER = (80, 160, 255)