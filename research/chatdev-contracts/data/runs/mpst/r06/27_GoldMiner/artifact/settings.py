'''
Global configuration constants for the Gold Miner game.
'''
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Gold Miner"
# Colors
COLOR_SKY = (135, 206, 235)
COLOR_DIRT = (139, 90, 43)
COLOR_DIRT_DARK = (101, 67, 33)
COLOR_GOLD = (255, 200, 40)
COLOR_GOLD_DARK = (200, 150, 20)
COLOR_ROCK = (130, 130, 130)
COLOR_ROCK_DARK = (90, 90, 90)
COLOR_DIAMOND = (80, 220, 240)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (220, 40, 40)
COLOR_GREEN = (40, 180, 60)
COLOR_YELLOW = (255, 230, 80)
COLOR_BROWN = (120, 72, 36)
COLOR_TNT = (200, 60, 30)
COLOR_BAG = (150, 100, 60)
# Claw
CLAW_PIVOT = (SCREEN_WIDTH // 2, 90)
CLAW_SWING_SPEED = 1.2  # radians per second
CLAW_SWING_ANGLE = 75  # max swing angle in degrees from straight down
CLAW_EXTEND_SPEED = 420  # pixels per second
CLAW_RETRACT_SPEED_EMPTY = 700
CLAW_MIN_LENGTH = 40
CLAW_MAX_LENGTH = 620
# Game
START_TIME = 60
TARGET_BASE = 300
TARGET_GROWTH = 250
TIME_DECREASE_PER_LEVEL = 3
MIN_TIME = 30
# Physics-ish
WEIGHT_SPEED_DIVISOR = 90  # retract speed = base / (1 + weight * factor)