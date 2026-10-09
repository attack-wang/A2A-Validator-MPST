'''
settings.py
Global configuration and constants for the "Tower of the Sorcerer" style
roguelike: grid dimensions, tile codes, colors, gameplay balance numbers
and monster templates.
'''
# ---------------------------------------------------------------------------
# Grid / window layout
# ---------------------------------------------------------------------------
GRID_WIDTH = 80          # fixed map width in tiles
GRID_HEIGHT = 80         # fixed map height in tiles
TILE_SIZE = 10           # pixels per tile
SIDEBAR_WIDTH = 300      # UI sidebar width in pixels
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE
FPS = 60
# ---------------------------------------------------------------------------
# Tile codes stored in the grid
# ---------------------------------------------------------------------------
WALL = 0
FLOOR = 1
DOOR = 2
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BG          = (16, 16, 22)
COLOR_WALL        = (58, 58, 72)
COLOR_FLOOR       = (198, 198, 204)
COLOR_DOOR        = (222, 168, 48)
COLOR_CHEST       = (146, 84, 44)
COLOR_MONSTER     = (190, 48, 48)
COLOR_PLAYER      = (36, 130, 240)
COLOR_SIDEBAR     = (26, 26, 34)
COLOR_TEXT        = (232, 232, 232)
COLOR_TEXT_DIM    = (150, 150, 158)
COLOR_HP_BG       = (70, 24, 24)
COLOR_HP_FILL     = (210, 60, 60)
COLOR_TITLE       = (222, 168, 48)
COLOR_PANEL       = (38, 38, 48)
COLOR_PANEL_EDGE  = (80, 80, 96)
COLOR_MSG_DANGER  = (240, 110, 110)
COLOR_MSG_GOOD    = (120, 220, 140)
COLOR_MSG_INFO    = (150, 190, 250)
COLOR_OVERLAY     = (10, 10, 14)
# ---------------------------------------------------------------------------
# Gameplay balance
# ---------------------------------------------------------------------------
PLAYER_START_HP   = 100
CHEST_HEAL_MIN    = 20
CHEST_HEAL_MAX    = 30
# Map population (scales with floor number)
MONSTERS_BASE        = 12
MONSTERS_PER_FLOOR   = 3
MONSTERS_MAX         = 45
CHESTS_BASE          = 4
CHESTS_PER_FLOOR     = 1
CHESTS_MAX           = 12
# Map generation
EXTRA_WALKS      = 26     # number of extra drunkard walks for side corridors
EXTRA_WALK_STEPS = 220    # steps per extra walk
ROOMS            = 14     # number of open rooms carved per floor
ROOM_MIN         = 4      # min room width/height
ROOM_MAX         = 9      # max room width/height
GEN_ATTEMPTS     = 8      # regeneration attempts if the path check fails
# Monster templates: (name, base_hp). Higher floors unlock stronger ones.
MONSTER_TEMPLATES = [
    ("Green Slime",   10),
    ("Red Bat",       16),
    ("Skeleton",      24),
    ("Small Wizard",  32),
    ("Stone Guard",   45),
    ("Dark Knight",   60),
    ("Wraith",        78),
    ("Archmage",      95),
    ("Tower Guardian", 120),
]
# UI
LOG_LINES = 7            # message log capacity shown in the sidebar