GRID_WIDTH = 80
GRID_HEIGHT = 80
TILE_SIZE = 10
MAP_PIXEL_WIDTH = GRID_WIDTH * TILE_SIZE  # 800
MAP_PIXEL_HEIGHT = GRID_HEIGHT * TILE_SIZE  # 800
PANEL_WIDTH = 260
WINDOW_WIDTH = MAP_PIXEL_WIDTH + PANEL_WIDTH
WINDOW_HEIGHT = MAP_PIXEL_HEIGHT
FPS = 60
# Tiles
TILE_WALL = 0
TILE_FLOOR = 1
# Colors
COLOR_BG = (18, 18, 24)
COLOR_WALL = (60, 60, 74)
COLOR_FLOOR = (30, 32, 40)
COLOR_PLAYER = (80, 200, 255)
COLOR_MONSTER = (220, 70, 70)
COLOR_CHEST = (230, 180, 40)
COLOR_DOOR = (120, 220, 120)
COLOR_PANEL_BG = (28, 28, 36)
COLOR_TEXT = (230, 230, 230)
COLOR_HP_BAR_BG = (80, 30, 30)
COLOR_HP_BAR_FG = (60, 200, 90)
COLOR_MESSAGE = (255, 210, 120)
# Controls
KEY_UP = 'w'
KEY_LEFT = 'a'
KEY_DOWN = 's'
KEY_RIGHT = 'd'
# Player
PLAYER_START_HP = 100
LEVEL_CLEAR_BONUS = 10
# Chest
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30
CHESTS_PER_LEVEL_BASE = 4
# Monsters
MONSTER_TYPES = [
    {"name": "Slime", "hp": 12, "color": (90, 200, 90), "char": "S"},
    {"name": "Bat", "hp": 18, "color": (150, 100, 200), "char": "B"},
    {"name": "Skeleton", "hp": 30, "color": (220, 220, 210), "char": "K"},
    {"name": "Ghost", "hp": 45, "color": (170, 200, 230), "char": "G"},
    {"name": "Demon", "hp": 65, "color": (230, 90, 40), "char": "D"},
    {"name": "Ogre", "hp": 90, "color": (200, 140, 60), "char": "O"},
]
MONSTERS_PER_LEVEL_BASE = 10
MONSTER_HP_LEVEL_SCALE = 0.35  # hp multiplier growth per level