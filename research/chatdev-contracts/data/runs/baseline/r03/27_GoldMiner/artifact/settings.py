"""
settings.py
Global constants and tuning parameters for the Gold Miner game.
Every tunable value used across the game lives here so that difficulty
and visuals can be adjusted from a single place.
"""
import math
# Screen / window
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60
TITLE = "Gold Miner"
# Colors
SKY_TOP = (120, 190, 240)
SKY_BOTTOM = (190, 225, 250)
DIRT_TOP = (146, 100, 52)
DIRT_BOTTOM = (96, 62, 30)
DIRT_SPECK = (120, 80, 40)
ROPE_COLOR = (60, 40, 20)
CLAW_COLOR = (70, 70, 80)
CLAW_HIGHLIGHT = (140, 140, 155)
TEXT_COLOR = (40, 30, 20)
HUD_PANEL = (25, 25, 35)
HUD_TEXT = (245, 235, 200)
GOLD_COLOR = (250, 200, 40)
GOLD_DARK = (200, 150, 20)
GOLD_SHINE = (255, 240, 170)
ROCK_COLOR = (130, 130, 135)
ROCK_DARK = (95, 95, 100)
DIAMOND_COLOR = (90, 220, 235)
DIAMOND_DARK = (40, 160, 190)
BONE_COLOR = (235, 225, 200)
BONE_DARK = (180, 165, 135)
TNT_COLOR = (200, 40, 40)
TNT_DARK = (140, 20, 20)
MESSAGE_GOOD = (90, 220, 90)
MESSAGE_BAD = (240, 80, 60)
MESSAGE_INFO = (250, 210, 90)
# World layout
GROUND_Y = 150
MINE_TOP = GROUND_Y + 40
MINE_MARGIN_X = 50
MINE_BOTTOM = SCREEN_HEIGHT - 30
CLAW_PIVOT_X = SCREEN_WIDTH // 2
CLAW_PIVOT_Y = 95
# Claw behaviour
CLAW_SWING_AMPLITUDE = 78.0
CLAW_MIN_LENGTH = 34.0
CLAW_EXTEND_SPEED = 460.0
CLAW_RETRACT_EMPTY_SPEED = 700.0
CLAW_RETRACT_BASE_SPEED = 620.0
CLAW_TIP_RADIUS = 12.0
CLAW_MAX_LENGTH = 900.0
# Object definitions
GOLD_SMALL_VALUE = 50
...