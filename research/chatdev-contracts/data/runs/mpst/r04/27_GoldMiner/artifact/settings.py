"""Global settings and configuration constants for the Gold Miner game."""
import pygame
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Gold Miner"
# Colors (R, G, B)
COLOR_SKY = (135, 206, 235)
COLOR_DIRT = (139, 90, 43)
COLOR_DIRT_DARK = (110, 70, 35)
COLOR_GROUND_LINE = (90, 55, 25)
COLOR_BLACK = (20, 20, 20)
COLOR_WHITE = (255, 255, 255)
COLOR_GOLD = (255, 200, 40)
COLOR_GOLD_DARK = (200, 150, 20)
COLOR_ROCK = (130, 130, 135)
COLOR_ROCK_DARK = (95, 95, 100)
COLOR_DIAMOND = (80, 220, 255)
COLOR_DIAMOND_DARK = (40, 170, 210)
COLOR_BONE = (235, 225, 200)
COLOR_BONE_DARK = (200, 190, 165)
COLOR_TNT = (200, 40, 40)
COLOR_TNT_DARK = (150, 25, 25)
COLOR_TNT_FUSE = (90, 60, 30)
COLOR_ROPE = (60, 40, 20)
COLOR_CLAW = (70, 70, 75)
COLOR_UI_PANEL = (40, 30, 25)
COLOR_GREEN = (60, 180, 75)
COLOR_RED = (220, 60, 50)
COLOR_ORANGE = (255, 140, 30)
COLOR_YELLOW = (255, 230, 90)
# Mine area (below the ground line)
GROUND_Y = 150
MINE_TOP = GROUND_Y + 40
MINE_BOTTOM = SCREEN_HEIGHT - 30
MINE_LEFT = 40
MINE_RIGHT = SCREEN_WIDTH - 40
# Claw
CLAW_PIVOT_X = SCREEN_WIDTH // 2
CLAW_PIVOT_Y = 60
CLAW_MIN_LENGTH = 60
CLAW_MAX_LENGTH = 500  # fixed from 700 (was off-screen)
CLAW_SWING_SPEED = 60.0
CLAW_EXTEND_SPEED = 420.0
CLAW_RETRACT_BASE_SPEED = 300.0
CLAW_MAX_ANGLE = 78.0
CLAW_RADIUS = 12
# Timing
LEVEL_TIME_BASE = 60
LEVEL_TIME_DECREASE = 5
LEVEL_TIME_MIN = 30
# Scoring
TIME_BONUS_PER_SECOND = 5
# Difficulty scaling
TNT_BLAST_RADIUS = 90
GOLD_SPECS = {
    "gold_large": (26, 500, 4.0),
    "gold_medium": (18, 250, 2.5),
    "gold_small": (12, 100, 1.2),
    "diamond": (12, 600, 1.0),
    "rock_large": (24, 20, 5.0),
    "rock_small": (14, 10, 3.0),
    "bone": (14, 30, 2.0),
    "tnt": (14, 0, 1.0),
    "mystery": (13, 0, 1.5),
}
GOLD_KINDS = ("gold_large", "gold_medium", "gold_small", "diamond")