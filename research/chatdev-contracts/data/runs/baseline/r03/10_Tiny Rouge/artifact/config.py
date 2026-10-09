'''
config.py
Central configuration for the roguelike game inspired by Tower of the Sorcerer.
Contains all tunable constants: grid dimensions, tile codes, colors,
player/chest/monster parameters and per-level difficulty scaling values.
'''
# ---------------------------------------------------------------------------
# Grid and window layout
# ---------------------------------------------------------------------------
GRID_WIDTH = 80          # number of horizontal tiles (fixed 80x80 map)
GRID_HEIGHT = 80         # number of vertical tiles
TILE_SIZE = 10           # pixels per tile
HUD_HEIGHT = 110         # pixel height of the bottom UI panel
WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE                    # 800 px
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE + HUD_HEIGHT     # 910 px
FPS = 30
# Window caption
WINDOW_TITLE = "Tower of the Sorcerer - Roguelike"
# ---------------------------------------------------------------------------
# Tile codes stored in the 2D grid
# ---------------------------------------------------------------------------
TILE_WALL = 0
TILE_FLOOR = 1
TILE_DOOR = 2
# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
PLAYER_START_HP = 100
# ---------------------------------------------------------------------------
# Treasure chests
# ---------------------------------------------------------------------------
CHEST_HEAL_MIN = 20      # minimum HP restored by a chest
CHEST_HEAL_MAX = 30      # maximum HP restored by a chest
CHESTS_PER_LEVEL_BASE = 4
# ---------------------------------------------------------------------------
# Monsters
# ---------------------------------------------------------------------------
MONSTERS_PER_LEVEL_BASE = 10
MONSTER_HP_SCALE_PER_LEVEL = 0.25   # monster HP grows 25% per level
MONSTER_MIN_SPAWN_DISTANCE = 8      # monsters never spawn next to the start
CHEST_MIN_SPAWN_DISTANCE = 4
# Monster archetypes. Combat subtracts the monster's HP from the player's HP;
# ATK / DEF are flavour stats shown in the UI.
MONSTER_TYPES = [
    {"name": "Green Slime", "hp": 10, "atk": 5,  "defense": 1, "color": (70, 200, 90)},
    {"name": "Vampire Bat", "hp": 15, "atk": 8,  "defense": 0, "color": (170, 90, 220)},
    {"name": "Skeleton",    "hp": 25, "atk": 12, "defense": 3, "color": (225, 225, 215)},
    {"name": "Ghost",       "hp": 35, "atk": 16, "defense": 2, "color": (110, 170, 235)},
    {"name": "Demon",       "hp": 50, "atk": 22, "defense": 5, "color": (215, 60, 60)},
]
# ---------------------------------------------------------------------------
# Map generation
# ---------------------------------------------------------------------------
EXTRA_PASSAGES = 320     # number of walls removed to create loops in the maze
ROOMS_PER_LEVEL = 14     # number of open rooms carved into the maze
ROOM_MIN_SIZE = 3
ROOM_MAX_SIZE = 7
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (18, 18, 26)
COLOR_WALL = (70, 55, 45)
COLOR_FLOOR = (205, 195, 175)
COLOR_DOOR = (60, 175, 70)
COLOR_CHEST = (235, 185, 40)
COLOR_CHEST_BORDER = (140, 100, 10)
COLOR_PLAYER = (40, 110, 230)
COLOR_PLAYER_BORDER = (240, 240, 255)
COLOR_MONSTER_BORDER = (30, 30, 30)
COLOR_HUD_BG = (30, 30, 40)
COLOR_HUD_TEXT = (230, 230, 230)
COLOR_HUD_TEXT_DIM = (160, 160, 170)
COLOR_HUD_HP_BAR_BG = (70, 30, 30)
COLOR_HUD_HP_BAR_FG = (210, 50, 50)
COLOR_GAME_OVER = (220, 40, 40)
# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------
KEY_UP = "w"
KEY_LEFT = "a"
KEY_DOWN = "s"
KEY_RIGHT = "d"