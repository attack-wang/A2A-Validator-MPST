'''
settings.py
Global configuration constants for the Gold Miner game: screen dimensions,
colors, physics tuning values, gameplay balance parameters and object stats.
'''
import math
# Screen / window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Gold Miner"
# Layout
GROUND_Y = 150
HUD_HEIGHT = 44
UNDERGROUND_TOP = GROUND_Y + 20
UNDERGROUND_BOTTOM = SCREEN_HEIGHT - 20
UNDERGROUND_LEFT = 40
UNDERGROUND_RIGHT = SCREEN_WIDTH - 40
# Colors
SKY_COLOR = (135, 206, 235)
GROUND_COLOR = (139, 90, 43)
DIRT_COLOR = (101, 67, 33)
DIRT_DOT_COLOR = (85, 55, 25)
HUD_BG_COLOR = (60, 40, 20)
HUD_TEXT_COLOR = (255, 230, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD_COLOR = (255, 200, 40)
GOLD_DARK_COLOR = (200, 150, 20)
ROCK_COLOR = (130, 130, 130)
ROCK_DARK_COLOR = (90, 90, 90)
DIAMOND_COLOR = (120, 220, 255)
DIAMOND_DARK_COLOR = (60, 160, 220)
BONE_COLOR = (240, 235, 210)
TNT_COLOR = (200, 40, 40)
TNT_FUSE_COLOR = (60, 60, 60)
BAG_COLOR = (150, 100, 60)
ROPE_COLOR = (60, 40, 20)
CLAW_COLOR = (180, 180, 190)
CLAW_DARK_COLOR = (110, 110, 120)
EXPLOSION_COLOR = (255, 120, 30)
EXPLOSION_INNER_COLOR = (255, 220, 100)
TEXT_POP_COLOR = (255, 230, 80)
MENU_BG_COLOR = (30, 20, 10)
# Claw physics
CLAW_PIVOT = (SCREEN_WIDTH // 2, GROUND_Y - 10)
CLAW_MIN_LENGTH = 30
CLAW_MAX_LENGTH = 480
CLAW_MAX_ANGLE = 75.0
CLAW_SWING_SPEED = 90.0     # degrees per second
CLAW_EXTEND_SPEED = 550.0   # pixels per second
CLAW_RETRACT_SPEED_EMPTY = 700.0
CLAW_BASE_REEL_SPEED = 260.0  # divided by object weight
# Gameplay balance
LEVEL_START_TIME = 60.0
MIN_LEVEL_TIME = 25.0
LEVEL_TIME_DECREMENT = 5.0
BASE_TARGET = 650
TARGET_INCREMENT = 450
LEVEL_BONUS = 100  # bonus per remaining second? Actually let's do time bonus
# Object stats
GOLD_STATS = {
    'small':  {'radius': 10, 'value': 50,  'weight': 1.5},
    'medium': {'radius': 18, 'value': 100, 'weight': 3.0},
    'large':  {'radius': 28, 'value': 250, 'weight': 5.0},
}
ROCK_STATS = {
    'small': {'radius': 14, 'value': 20,  'weight': 4.0},
    'large': {'radius': 26, 'value': 40,  'weight': 7.0},
}
DIAMOND_STATS = {'radius': 12, 'value': 600, 'weight': 1.0}
BONE_STATS = {'radius': 16, 'value': 30, 'weight': 2.0}
TNT_STATS = {'radius': 16, 'value': 0, 'weight': 2.0}
TNT_BLAST_RADIUS = 90
MYSTERY_STATS = {'radius': 15, 'value': 0, 'weight': 2.5}
MYSTERY_VALUES = [50, 100, 200, 350, -50]  # hmm, negative? Maybe keep positive but random. Actually classic gold miner mystery bag can give strength or random. Let's keep values positive plus maybe a small penalty. I'll include a small penalty option for spice but ensure it doesn't go below 0 score... Actually score could go negative; target check is score >= target. Let's keep it simple: random positive values [50, 100, 200, 350, 500].