'''Global settings and constants for the Tower of the Sorcerer roguelike game.'''
# Window / grid configuration
GRID_SIZE = 80          # The map is a fixed 80x80 grid of tiles
TILE_SIZE = 10          # Pixels per tile when rendered
PANEL_WIDTH = 250       # Width of the side UI panel (pixels)
WINDOW_WIDTH = GRID_SIZE * TILE_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = GRID_SIZE * TILE_SIZE
FPS = 60
# Tile codes stored in the 2D map grid
FLOOR = 0
WALL = 1
DOOR = 2
# Game balance
PLAYER_START_HP = 100
CHEST_HEAL_MIN = 20     # Minimum HP restored by a treasure chest
CHEST_HEAL_MAX = 30     # Maximum HP restored by a treasure chest
MAX_LEVELS = 10         # Reaching the door on this level wins the game
BASE_MONSTERS_PER_LEVEL = 5   # Monsters on level 1 (+1 per additional level)
BASE_CHESTS_PER_LEVEL = 3
# Monster archetypes (Tower of the Sorcerer inspired).
# "hp" is the damage dealt to the player when combat is resolved.
MONSTER_TYPES = [
    {"name": "Green Slime", "hp": 10, "atk": 5,  "color": (80, 200, 90)},
    {"name": "Red Bat",     "hp": 15, "atk": 8,  "color": (210, 90, 90)},
    {"name": "Skeleton",    "hp": 25, "atk": 12, "color": (225, 225, 215)},
    {"name": "Dark Wizard", "hp": 40, "atk": 18, "color": (160, 90, 220)},
    {"name": "Tower Boss",  "hp": 80, "atk": 30, "color": (230, 50, 50)},
]
# Colors (R, G, B)
COLOR_BACKGROUND   = (20, 20, 26)
COLOR_WALL         = (55, 55, 68)
COLOR_FLOOR        = (188, 182, 170)
COLOR_DOOR         = (230, 180, 40)
COLOR_PLAYER       = (40, 110, 230)
COLOR_CHEST        = (190, 130, 40)
COLOR_PANEL_BG     = (32, 32, 40)
COLOR_PANEL_TEXT   = (230, 230, 230)
COLOR_HP_BAR_BG    = (70, 30, 30)
COLOR_HP_BAR_FILL  = (60, 200, 90)
COLOR_MESSAGE      = (200, 200, 160)
COLOR_TITLE        = (240, 200, 80)
COLOR_OVERLAY      = (0, 0, 0)
# Fonts
FONT_NAME = "consolas"   # fallback handled in ui.py
FONT_SIZE_SMALL = 14
FONT_SIZE_MEDIUM = 18
FONT_SIZE_LARGE = 26