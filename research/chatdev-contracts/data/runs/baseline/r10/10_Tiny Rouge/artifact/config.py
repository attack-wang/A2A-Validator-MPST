"""Configuration constants for the Tower of the Sorcerer roguelike game."""
# --- Grid / Window ---
GRID_WIDTH = 80
GRID_HEIGHT = 80
TILE_SIZE = 10
UI_PANEL_WIDTH = 250
WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE + UI_PANEL_WIDTH  # 1050
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE                # 800
FPS = 60
# --- Tiles ---
TILE_WALL = 0
TILE_FLOOR = 1
TILE_DOOR = 2
# --- Player ---
PLAYER_START_HP = 100
PLAYER_MAX_HP_BASE = 100
MAX_HP_GAIN_PER_LEVEL = 10
LEVEL_CLEAR_HEAL = 25
MOVE_REPEAT_DELAY_MS = 220   # initial delay before auto-repeat
MOVE_REPEAT_INTERVAL_MS = 110 # interval between auto-repeat moves
# --- Chests ---
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30
CHESTS_PER_LEVEL_BASE = 6
# --- Monsters ---
MONSTERS_PER_LEVEL_BASE = 14
MONSTERS_PER_LEVEL_INCREMENT = 4
MONSTER_COUNT_CAP = 60
# name, base hp, hp per level, unlock level, color
MONSTER_TYPES = [
    {"name": "Slime",   "base_hp": 8,  "hp_per_level": 3, "unlock_level": 1, "color": (80, 200, 80)},
    {"name": "Bat",     "base_hp": 14, "hp_per_level": 4, "unlock_level": 1, "color": (150, 80, 200)},
    {"name": "Skeleton","base_hp": 22, "hp_per_level": 5, "unlock_level": 2, "color": (220, 220, 210)},
    {"name": "Ghost",   "base_hp": 32, "hp_per_level": 6, "unlock_level": 3, "color": (170, 200, 230)},
    {"name": "Demon",   "base_hp": 45, "hp_per_level": 8, "unlock_level": 4, "color": (200, 60, 60)},
    {"name": "Wizard",  "base_hp": 60, "hp_per_level": 10, "unlock_level": 5, "color": (240, 160, 40)},
]
# --- Colors (R, G, B) ---
COLOR_BACKGROUND = (18, 18, 24)
COLOR_WALL = (70, 60, 50)
COLOR_WALL_TOP = (95, 82, 68)
COLOR_FLOOR = (205, 195, 175)
COLOR_FLOOR_ALT = (196, 186, 166)
COLOR_DOOR = (180, 130, 40)
COLOR_DOOR_FRAME = (90, 60, 20)
COLOR_PLAYER = (40, 120, 230)
COLOR_PLAYER_EDGE = (20, 60, 140)
COLOR_CHEST = (212, 175, 55)
COLOR_CHEST_BAND = (120, 90, 20)
COLOR_UI_BG = (28, 28, 36)
COLOR_UI_TEXT = (230, 230, 230)
COLOR_UI_ACCENT = (120, 180, 255)
COLOR_HP_BAR_BG = (60, 60, 70)
COLOR_HP_BAR_FILL = (70, 200, 90)
COLOR_HP_BAR_FILL_LOW = (220, 70, 60)
COLOR_TEXT_DANGER = (255, 120, 100)
COLOR_LOG_TEXT = (200, 200, 200)
# --- Map generation ---
BRAID_PROBABILITY = 0.55   # chance to open a dead end into a loop
MAX_GENERATION_ATTEMPTS = 20