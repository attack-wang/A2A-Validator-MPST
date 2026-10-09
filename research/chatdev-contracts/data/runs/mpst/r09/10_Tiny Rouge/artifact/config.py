'''
config.py
Global configuration constants for the Tower of the Sorcerer-inspired roguelike.
'''
# --- Grid ---
GRID_SIZE = 80          # fixed 80x80 grid map
TILE_SIZE = 12          # pixels per tile
MAP_PIXEL_SIZE = GRID_SIZE * TILE_SIZE  # 960
# --- Window ---
UI_PANEL_WIDTH = 320
WINDOW_WIDTH = MAP_PIXEL_SIZE + UI_PANEL_WIDTH   # 1280
WINDOW_HEIGHT = MAP_PIXEL_SIZE                   # 960
WINDOW_TITLE = "Tower of the Sorcerer - Roguelike"
FPS = 60
# --- Tiles ---
TILE_WALL = 0
TILE_FLOOR = 1
# --- Colors (R, G, B) ---
COLOR_BACKGROUND = (18, 18, 24)
COLOR_WALL = (70, 70, 85)
COLOR_FLOOR = (200, 200, 200)
COLOR_FLOOR_ALT = (188, 188, 192)
COLOR_PLAYER = (30, 90, 220)
COLOR_DOOR = (220, 170, 40)
COLOR_CHEST = (190, 120, 30)
COLOR_TEXT = (230, 230, 230)
COLOR_TEXT_DIM = (150, 150, 160)
COLOR_HP_BAR_BG = (60, 20, 20)
COLOR_HP_BAR_FG = (200, 40, 40)
COLOR_PANEL_BG = (28, 28, 36)
COLOR_PANEL_BORDER = (80, 80, 100)
COLOR_MESSAGE_INFO = (170, 200, 170)
COLOR_MESSAGE_COMBAT = (230, 120, 120)
COLOR_MESSAGE_HEAL = (120, 220, 120)
COLOR_MESSAGE_LEVEL = (230, 200, 120)
COLOR_OVERLAY_BG = (10, 10, 14)
COLOR_TITLE = (240, 220, 140)
# --- Player ---
PLAYER_START_HP = 100
# --- Chest ---
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30
# --- Map generation ---
ROOM_MIN_SIZE = 5
ROOM_MAX_SIZE = 11
MAX_ROOMS = 26
MAX_GENERATION_ATTEMPTS = 50
# --- Entities per level ---
CHESTS_PER_LEVEL = 4
# Monster archetypes: (name, base_hp, color, min_level)
MONSTER_TYPES = [
    ("Slime", 10, (60, 180, 90), 1),
    ("Bat", 15, (150, 90, 200), 1),
    ("Skeleton", 25, (220, 220, 220), 2),
    ("Ghost", 35, (120, 210, 220), 3),
    ("Demon", 50, (220, 60, 60), 4),
]
# Monster count grows with level
def monsters_for_level(level):
    return min(6 + level * 2, 30)
def monster_hp_scale(level):
    return 1 + (level - 1) * 0.15