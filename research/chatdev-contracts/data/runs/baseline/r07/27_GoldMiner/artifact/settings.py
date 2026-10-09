'''Global constants and configuration for the Gold Miner game.'''
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Gold Miner"
# Colors
SKY_COLOR = (135, 206, 235)      # light blue sky
GROUND_COLOR = (139, 90, 43)     # brown dirt
DIRT_DARK = (110, 70, 33)
HUD_COLOR = (60, 40, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD_COLOR = (255, 200, 40)
GOLD_DARK = (200, 150, 20)
ROCK_COLOR = (130, 130, 135)
ROCK_DARK = (95, 95, 100)
DIAMOND_COLOR = (80, 220, 255)
DIAMOND_DARK = (40, 170, 210)
SKULL_COLOR = (235, 230, 215)
TNT_COLOR = (200, 40, 40)
ROPE_COLOR = (90, 60, 30)
CLAW_COLOR = (70, 70, 75)
GREEN = (40, 180, 60)
RED = (220, 50, 50)
YELLOW = (255, 220, 60)
# Layout
HUD_HEIGHT = 70
PIVOT_X = SCREEN_WIDTH // 2
PIVOT_Y = HUD_HEIGHT + 20
FIELD_TOP = 170
FIELD_BOTTOM = SCREEN_HEIGHT - 20
FIELD_LEFT = 40
FIELD_RIGHT = SCREEN_WIDTH - 40
# Claw
MAX_ANGLE = 75          # max swing angle in degrees from vertical
SWING_SPEED = 1.6       # degrees per frame (base)
EXTEND_SPEED = 8        # pixels per frame while extending
EMPTY_RETRACT_SPEED = 12
BASE_RETRACT_SPEED = 6  # divided by object weight
CLAW_MIN_LENGTH = 45
CLAW_MAX_LENGTH = SCREEN_HEIGHT - PIVOT_Y - 8
# Game
STARTING_LEVEL = 1
BASE_GOAL = 500
GOAL_INCREMENT = 300
BASE_TIME = 60
TIME_DECREMENT = 5
MIN_TIME = 30
# TNT
TNT_BLAST_RADIUS = 110
TNT_PENALTY = 50