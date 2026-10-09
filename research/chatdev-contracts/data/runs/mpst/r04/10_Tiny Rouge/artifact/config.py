'''
config.py
Configuration constants for the Tower of the Sorcerer-inspired roguelike.
All tunable gameplay values, colors and window dimensions live here so the
rest of the codebase stays free of magic numbers.
'''
# ---------------------------------------------------------------------------
# Map
# ---------------------------------------------------------------------------
MAP_WIDTH = 80
MAP_HEIGHT = 80
TILE_SIZE = 10
# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------
SIDEBAR_WIDTH = 240
WINDOW_WIDTH = MAP_WIDTH * TILE_SIZE + SIDEBAR_WIDTH   # 1040
WINDOW_HEIGHT = MAP_HEIGHT * TILE_SIZE                 # 800
FPS = 30
# ---------------------------------------------------------------------------
# Tile types
# ---------------------------------------------------------------------------
WALL = 0
FLOOR = 1
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BG = (20, 20, 30)
COLOR_WALL = (60, 60, 80)
COLOR_FLOOR = (200, 200, 200)
COLOR_FLOOR_ALT = (185, 185, 190)          # checkerboard variation
COLOR_PLAYER = (40, 180, 90)
COLOR_PLAYER_BORDER = (240, 255, 240)
COLOR_MONSTER = (200, 50, 50)
COLOR_MONSTER_BORDER = (120, 20, 20)
COLOR_CHEST = (230, 180, 40)
COLOR_CHEST_BORDER = (120, 90, 10)
COLOR_DOOR = (150, 100, 50)
COLOR_DOOR_BORDER = (240, 200, 120)
COLOR_SIDEBAR_BG = (30, 30, 45)
COLOR_TEXT = (230, 230, 230)
COLOR_TEXT_HIGHLIGHT = (255, 220, 120)
COLOR_TEXT_DANGER = (255, 120, 120)
COLOR_TEXT_GOOD = (140, 230, 140)
COLOR_TITLE = (255, 200, 80)
COLOR_OVERLAY = (10, 10, 15)
# ---------------------------------------------------------------------------
# Gameplay balance
# ---------------------------------------------------------------------------
PLAYER_START_HP = 100
PLAYER_MAX_HP = 200
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30
# Monsters per level (unified naming, with sane caps for high levels)
MONSTERS_PER_LEVEL_BASE = 8
MONSTERS_PER_LEVEL_INCREMENT = 3
MONSTERS_MAX = 30
MONSTER_HP_BASE_MIN = 5
MONSTER_HP_BASE_MAX = 15
MONSTER_HP_LEVEL_SCALE = 5
# Treasure chests per level
CHESTS_PER_LEVEL_BASE = 4
CHESTS_PER_LEVEL_INCREMENT = 1
CHESTS_MAX = 12
# ---------------------------------------------------------------------------
# Map generation
# ---------------------------------------------------------------------------
MAX_GENERATION_ATTEMPTS = 20
ROOMS_MIN = 14
ROOMS_MAX = 20
ROOM_SIZE_MIN = 3
ROOM_SIZE_MAX = 9
# ---------------------------------------------------------------------------
# UI / input
# ---------------------------------------------------------------------------
MOVE_REPEAT_MS = 120      # repeat delay while a movement key is held
MAX_LOG_LINES = 8