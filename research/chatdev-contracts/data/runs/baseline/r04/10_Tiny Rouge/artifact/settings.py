'''Global settings and constants for the Tower of the Sorcerer roguelike.'''
import os
# --- Grid ----------------------------------------------------------
GRID_WIDTH = 80
GRID_HEIGHT = 80
# --- Tile codes ----------------------------------------------------
TILE_WALL = 0
TILE_FLOOR = 1
TILE_DOOR = 2
# --- Console symbols ------------------------------------------------
SYMBOL_WALL = '#'
SYMBOL_FLOOR = '.'
SYMBOL_DOOR = 'D'
SYMBOL_PLAYER = '@'
SYMBOL_MONSTER = 'M'
SYMBOL_CHEST = '$'
# --- Gameplay ------------------------------------------------------
PLAYER_START_HP = 100
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30
MONSTERS_BASE_COUNT = 8
MONSTERS_PER_LEVEL = 2
MONSTERS_MAX_COUNT = 40
CHESTS_BASE_COUNT = 4
CHESTS_MAX_COUNT = 8
VICTORY_LEVEL = 10
# --- Monster tiers -------------------------------------------------
MONSTER_TIERS = (
    ("Slime", 1.0),
    ("Red Slime", 1.25),
    ("Bat", 1.5),
    ("Skeleton", 1.9),
    ("Ghost", 2.4),
    ("Wizard", 3.0),
    ("Demon", 3.8),
)
# ANSI colors (optional; gracefully ignored if unsupported)
...