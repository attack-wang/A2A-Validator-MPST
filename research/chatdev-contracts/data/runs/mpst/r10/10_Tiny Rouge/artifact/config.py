'''
config.py
Global configuration constants for the Tower of the Sorcerer inspired roguelike.
'''
# --- Grid / map -----------------------------------------------------------
GRID_WIDTH = 80
GRID_HEIGHT = 80
TILE_WALL = 0
TILE_FLOOR = 1
TILE_DOOR = 2
# --- Map generation -------------------------------------------------------
ROOM_ATTEMPTS = 140
MIN_ROOMS = 12
ROOM_MIN_SIZE = 5
ROOM_MAX_SIZE = 10
MIN_START_DOOR_DISTANCE = 40
# --- Entities -------------------------------------------------------------
PLAYER_START_HP = 100
PLAYER_MAX_HP = 200
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30
LEVEL_CLEAR_BONUS = 10
WEAK_MONSTER_TYPES = (("Green Slime", 6), ("Red Slime", 9), ("Vampire Bat", 8))
STRONG_MONSTER_TYPES = (("Skeleton", 18), ("Ghost", 26), ("Dark Wizard", 34), ("Sorcerer", 42))
PATH_MONSTER_BUDGET = 40
PATH_MONSTER_SAFETY_MARGIN = 20
PATH_MONSTER_MAX_COUNT = 6
MONSTERS_PER_LEVEL_BASE = 8
MONSTERS_PER_LEVEL_SCALE = 2
MAX_MONSTERS = 30
CHESTS_PER_LEVEL_BASE = 3
CHESTS_PER_LEVEL_SCALE = 1
MAX_CHESTS = 8
# --- UI -------------------------------------------------------------------
TILE_SIZE = 12
INFO_PANEL_WIDTH = 300
WINDOW_TITLE = "Tower of the Sorcerer - Roguelike"
COLOR_BACKGROUND = "#1a1a1a"
COLOR_WALL = "#4a3728"
COLOR_FLOOR = "#d9c9a3"
COLOR_DOOR = "#2e8b57"
COLOR_PLAYER = "#2060c0"
COLOR_CHEST = "#d4a017"
COLOR_MONSTER_WEAK = "#c23b22"
COLOR_MONSTER_STRONG = "#8b0000"
COLOR_TEXT_ON_TILE = "#000000"
MESSAGE_LOG_LENGTH = 10
MONSTER_COLORS = {
    "Green Slime": "#3fa34d",
    "Red Slime": "#c23b22",
    "Vampire Bat": "#5c3a6e",
    "Skeleton": "#e8e4d8",
    "Ghost": "#b8c4d9",
    "Dark Wizard": "#6a0dad",
    "Sorcerer": "#8b0000",
}