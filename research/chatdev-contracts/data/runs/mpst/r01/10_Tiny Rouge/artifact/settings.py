'''
settings.py
Central configuration for the Tower of the Sorcerer inspired roguelike.
Contains all tunable constants: grid dimensions, tile codes, colours,
player stats, chest healing range, monster templates and level generation
parameters.  Keeping them in one place makes balancing the game easy.
'''
# ---------------------------------------------------------------------------
# Grid / window geometry
# ---------------------------------------------------------------------------
GRID_WIDTH = 80          # number of columns of the fixed map
GRID_HEIGHT = 80         # number of rows of the fixed map
TILE_SIZE = 10           # pixels per tile
MAP_PIXEL_WIDTH = GRID_WIDTH * TILE_SIZE
MAP_PIXEL_HEIGHT = GRID_HEIGHT * TILE_SIZE
PANEL_WIDTH = 250        # side panel used for the minimal UI
WINDOW_WIDTH = MAP_PIXEL_WIDTH + PANEL_WIDTH
WINDOW_HEIGHT = MAP_PIXEL_HEIGHT
FPS = 60
WINDOW_TITLE = "Tower of the Sorcerer - Roguelike"
# ---------------------------------------------------------------------------
# Tile codes stored in the level grid
# ---------------------------------------------------------------------------
TILE_WALL = 0
TILE_FLOOR = 1
TILE_DOOR = 2
# ---------------------------------------------------------------------------
# Colours (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (18, 18, 26)
COLOR_WALL = (86, 74, 60)
COLOR_WALL_EDGE = (52, 44, 36)
COLOR_FLOOR = (203, 197, 182)
COLOR_FLOOR_ALT = (194, 188, 172)
COLOR_DOOR = (240, 190, 40)
COLOR_DOOR_EDGE = (150, 115, 15)
COLOR_PLAYER = (40, 110, 230)
COLOR_PLAYER_EDGE = (20, 60, 140)
COLOR_MONSTER = (205, 55, 45)
COLOR_MONSTER_EDGE = (120, 25, 20)
COLOR_CHEST = (196, 128, 34)
COLOR_CHEST_EDGE = (120, 75, 15)
COLOR_PANEL = (32, 34, 48)
COLOR_PANEL_EDGE = (70, 74, 96)
COLOR_TEXT = (232, 232, 232)
COLOR_TEXT_DIM = (150, 152, 165)
COLOR_HP_FULL = (70, 200, 90)
COLOR_HP_LOW = (220, 70, 60)
COLOR_OVERLAY = (15, 15, 20)
# ---------------------------------------------------------------------------
# Player / gameplay balance
# ---------------------------------------------------------------------------
PLAYER_START_HP = 100
CHEST_HEAL_MIN = 20      # treasure chests restore 20-30 HP ...
CHEST_HEAL_MAX = 30      # ... (inclusive range, chosen at random)
MAX_MESSAGES = 9         # lines kept in the on-screen message log
# ---------------------------------------------------------------------------
# Monster templates: (name, base HP).  HP is scaled up on deeper floors.
# ---------------------------------------------------------------------------
MONSTER_TEMPLATES = [
    ("Slime", 8),
    ("Bat", 12),
    ("Skeleton", 18),
    ("Ghost", 26),
    ("Golem", 34),
    ("Wizard", 44),
    ("Dragon", 60),
]
# ---------------------------------------------------------------------------
# Level generation parameters
# ---------------------------------------------------------------------------
ROOMS_TARGET = 18        # how many rooms a generated floor should contain
ROOM_MIN_SIZE = 6
ROOM_MAX_SIZE = 13
ROOM_PLACEMENT_ATTEMPTS = 400
EXTRA_CORRIDORS = 3      # extra loops so the map is not a pure tree
MAX_GENERATION_ATTEMPTS = 20   # safety net for the "path exists" guarantee
MONSTER_BASE_COUNT = 8   # monsters on floor N = base + per_level * N
MONSTER_PER_LEVEL = 2
MONSTER_HARD_CAP = 45
CHEST_BASE_COUNT = 5
CHEST_PER_LEVEL = 1
CHEST_HARD_CAP = 25