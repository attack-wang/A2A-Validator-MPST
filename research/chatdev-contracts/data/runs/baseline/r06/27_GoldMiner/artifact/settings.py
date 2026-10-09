'''Global configuration constants for the Gold Miner game.'''
import math
# Screen
WIDTH = 960
HEIGHT = 640
FPS = 60
TITLE = "Gold Miner"
# Colors
SKY_TOP = (135, 206, 235)
SKY_BOTTOM = (250, 220, 160)
DIRT_TOP = (139, 90, 43)
DIRT = (121, 85, 61)
DIRT_DARK = (94, 63, 42)
HUD_BG = (40, 40, 60)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GOLD = (255, 200, 40)
GOLD_DARK = (200, 150, 20)
GOLD_LIGHT = (255, 240, 160)
ROCK = (130, 130, 130)
ROCK_DARK = (95, 95, 95)
DIAMOND = (120, 220, 255)
DIAMOND_DARK = (60, 170, 220)
TNT_RED = (200, 40, 40)
TNT_DARK = (140, 25, 25)
ROPE = (60, 40, 20)
GREEN = (60, 180, 90)
RED = (220, 60, 60)
YELLOW = (255, 230, 100)
PURPLE = (170, 90, 220)
PURPLE_DARK = (110, 50, 160)
GRAY_TEXT = (180, 180, 200)
# Layout
HUD_HEIGHT = 70
PIVOT_X = WIDTH // 2
PIVOT_Y = HUD_HEIGHT + 30
GROUND_Y = 200  # top of dirt
# Claw
MIN_ROPE = 40
MAX_ANGLE = math.radians(75)
SWING_SPEED = 1.6          # radians per second
EXTEND_SPEED = 420         # pixels per second
BASE_RETRACT_SPEED = 520   # empty claw retract
GRAB_RADIUS = 14           # tip proximity to grab an object
# Reel speed: pixels per second at weight 1
REEL_SPEED = 300           # speed = REEL_SPEED / weight
# TNT
BLAST_RADIUS = 90
# Timer
BASE_TIME = 65
TIME_PER_LEVEL = 3
MIN_TIME = 40
# Goal
BASE_GOAL = 500
GOAL_STEP = 300