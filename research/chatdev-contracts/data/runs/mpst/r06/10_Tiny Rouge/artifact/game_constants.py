'''
game_constants.py
Central configuration for the Tower of the Sorcerer roguelike game.
Contains grid dimensions, tile identifiers, colours, monster definitions
and all other tunable constants used across the project.
'''
# ------------------------------------------------------------------ #
# Grid / window geometry
# ------------------------------------------------------------------ #
GRID_SIZE = 80          # The map is a fixed 80 x 80 grid of tiles
TILE_SIZE = 10          # Pixels per tile when drawn
UI_PANEL_WIDTH = 280    # Width of the side panel that shows the UI
MAP_PIXEL_SIZE = GRID_SIZE * TILE_SIZE          # 800 px
WINDOW_WIDTH = MAP_PIXEL_SIZE + UI_PANEL_WIDTH  # 1080 px
WINDOW_HEIGHT = MAP_PIXEL_SIZE                  # 800 px
FPS = 60
WINDOW_TITLE = "Tower of the Sorcerer"
# ------------------------------------------------------------------ #
# Tile types
# ------------------------------------------------------------------ #
TILE_WALL = 0
TILE_FLOOR = 1
# ------------------------------------------------------------------ #
# Colours (R, G, B)
# ------------------------------------------------------------------ #
COLOR_BG = (18, 18, 24)
COLOR_WALL = (70, 60, 50)
COLOR_WALL_EDGE = (45, 38, 32)
COLOR_FLOOR = (205, 195, 175)
COLOR_FLOOR_ALT = (196, 186, 166)
COLOR_PLAYER = (40, 120, 255)
COLOR_PLAYER_EDGE = (230, 240, 255)
COLOR_CHEST = (255, 200, 40)
COLOR_CHEST_EDGE = (150, 105, 10)
COLOR_DOOR = (60, 220, 120)
COLOR_DOOR_EDGE = (20, 120, 60)
COLOR_UI_BG = (28, 28, 36)
COLOR_UI_TEXT = (235, 235, 235)
COLOR_UI_ACCENT = (255, 210, 90)
COLOR_HP_BAR_BACK = (70, 20, 20)
COLOR_HP_BAR_FILL = (220, 60, 60)
COLOR_OVERLAY = (10, 10, 14)
# ------------------------------------------------------------------ #
# Player
# ------------------------------------------------------------------ #
PLAYER_START_HP = 100
PLAYER_MAX_HP_BASE = 100
PLAYER_MAX_HP_PER_LEVEL = 20
# ------------------------------------------------------------------ #
# Treasure chests
# ------------------------------------------------------------------ #
CHEST_HEAL_MIN = 20     # minimum HP restored by a chest
CHEST_HEAL_MAX = 30     # maximum HP restored by a chest
# ------------------------------------------------------------------ #
# Monsters
# ------------------------------------------------------------------ #
# Each monster type: name, base HP on floor 1, colour, and spawn weight.
MONSTER_TYPES = [
    {"name": "Slime",    "base_hp": 8,  "color": (110, 220, 110), "weight": 30},
    {"name": "Bat",      "base_hp": 12, "color": (180, 100, 220), "weight": 25},
    {"name": "Skeleton", "base_hp": 18, "color": (230, 230, 220), "weight": 20},
    {"name": "Ghost",    "base_hp": 26, "color": (150, 200, 230), "weight": 15},
    {"name": "Demon",    "base_hp": 40, "color": (230, 70, 70),   "weight": 10},
]
MONSTER_HP_PER_LEVEL = 6   # extra HP every monster gains per floor
# ------------------------------------------------------------------ #
# Map population
# ------------------------------------------------------------------ #
MONSTERS_BASE = 22       # monsters on floor 1
MONSTERS_PER_LEVEL = 5   # extra monsters each floor
CHESTS_BASE = 7          # chests on every floor
ROOMS_TO_CARVE = 8       # extra open rooms carved on top of the maze
BRAID_CHANCE = 0.12      # chance to open a wall to create loops
# ------------------------------------------------------------------ #
# Movement directions (W/A/S/D)
# ------------------------------------------------------------------ #
DIRECTIONS = {
    "w": (0, -1),   # up
    "a": (-1, 0),   # left
    "s": (0, 1),    # down
    "d": (1, 0),    # right
}
MESSAGE_LOG_SIZE = 6