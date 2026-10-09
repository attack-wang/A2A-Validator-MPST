'''
settings.py
Global configuration constants for the Tower of the Sorcerer roguelike game.
'''
import pygame
# --- Window / grid layout ---
GRID_WIDTH = 80
GRID_HEIGHT = 80
TILE_SIZE = 10
MAP_PIXEL_WIDTH = GRID_WIDTH * TILE_SIZE  # 800
MAP_PIXEL_HEIGHT = GRID_HEIGHT * TILE_SIZE  # 800
UI_PANEL_WIDTH = 300
WINDOW_WIDTH = MAP_PIXEL_WIDTH + UI_PANEL_WIDTH  # 1100
WINDOW_HEIGHT = MAP_PIXEL_HEIGHT  # 800
WINDOW_TITLE = "Tower of the Sorcerer"
FPS = 60
# --- Tile type identifiers ---
TILE_WALL = 0
TILE_FLOOR = 1
# --- Colors ---
COLOR_BACKGROUND = (18, 18, 24)
COLOR_WALL = (86, 60, 42)
COLOR_WALL_EDGE = (52, 36, 26)
COLOR_FLOOR = (222, 205, 168)
COLOR_FLOOR_ALT = (214, 196, 158)
COLOR_DOOR = (240, 190, 40)
COLOR_CHEST = (150, 90, 30)
COLOR_PLAYER = (40, 120, 220)
COLOR_MONSTER = (190, 40, 40)
COLOR_UI_BG = (28, 28, 36)
COLOR_UI_TEXT = (235, 235, 235)
COLOR_UI_ACCENT = (240, 190, 40)
COLOR_HP_HIGH = (70, 200, 90)
COLOR_HP_MID = (230, 180, 40)
COLOR_HP_LOW = (220, 60, 60)
COLOR_MESSAGE = (200, 200, 210)
# --- Player ---
PLAYER_START_HP = 100
PLAYER_START_X = 1
PLAYER_START_Y = 1
# --- Chests ---
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30
# --- Monsters ---
MONSTER_HP_LEVEL_SCALE = 0.15
MONSTER_TYPES = [
    {"name": "Slime", "hp": 10, "glyph": "s", "color": (120, 200, 90)},
    {"name": "Bat", "hp": 15, "glyph": "b", "color": (150, 80, 200)},
    {"name": "Skeleton", "hp": 25, "glyph": "k", "color": (220, 220, 210)},
    {"name": "Orc", "hp": 40, "glyph": "o", "color": (90, 160, 60)},
    {"name": "Golem", "hp": 70, "glyph": "G", "color": (140, 140, 150)},
    {"name": "Demon", "hp": 100, "glyph": "D", "color": (220, 60, 60)},
]
MONSTER_BASE_COUNT = 8
MONSTER_PER_LEVEL = 3
MONSTER_MAX_COUNT = 40
CHEST_BASE_COUNT = 4
CHEST_PER_LEVEL = 1
CHEST_MAX_COUNT = 12
# --- UI ---
MAX_MESSAGES = 6