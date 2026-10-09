'''
config.py
Global configuration and constants for the Tower of the Sorcerer roguelike game.
'''
# --- Grid / Map ---
GRID_SIZE = 80          # 80x80 tile grid
CELL_SIZE = 10          # each generation cell is 10x10 tiles (8x8 cells)
TILE_SIZE = 10          # pixels per tile when rendering
# --- Window ---
UI_PANEL_WIDTH = 320
WINDOW_WIDTH = GRID_SIZE * TILE_SIZE + UI_PANEL_WIDTH   # 800 + 320 = 1120
WINDOW_HEIGHT = GRID_SIZE * TILE_SIZE                   # 800
FPS = 60
# --- Tiles ---
FLOOR = 0
WALL = 1
DOOR = 2
# --- Gameplay ---
PLAYER_START_HP = 100
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30
MONSTERS_PER_LEVEL = 14
CHESTS_PER_LEVEL = 6
MONSTER_HP_SCALE_PER_LEVEL = 0.25   # +25% monster HP each level
SAFE_RADIUS = 6                     # no monsters/chests within this radius of start
# --- Monster definitions: name -> base HP, color ---
MONSTER_TYPES = [
    ("Slime",    8,  (80, 200, 120)),
    ("Bat",     12,  (150, 80, 200)),
    ("Skeleton", 18, (220, 220, 220)),
    ("Ghost",   26,  (170, 200, 255)),
    ("Demon",   38,  (200, 60, 60)),
    ("Dragon",  60,  (255, 140, 0)),
]
# --- Colors (R, G, B) ---
COLOR_BACKGROUND = (18, 18, 24)
COLOR_FLOOR = (52, 52, 62)
COLOR_WALL = (110, 110, 125)
COLOR_DOOR = (230, 180, 40)
COLOR_CHEST = (160, 100, 40)
COLOR_PLAYER = (60, 200, 90)
COLOR_PANEL_BG = (28, 28, 36)
COLOR_PANEL_BORDER = (90, 90, 110)
COLOR_TEXT = (230, 230, 230)
COLOR_TEXT_DIM = (150, 150, 160)
COLOR_HP_FULL = (70, 200, 90)
COLOR_HP_EMPTY = (90, 30, 30)
COLOR_MESSAGE = (200, 200, 140)
COLOR_GAME_OVER = (200, 40, 40)