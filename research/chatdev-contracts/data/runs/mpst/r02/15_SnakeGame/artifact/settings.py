'''
Configuration constants for the Snake game.
'''
import os
# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
# HUD (score bar) height at the top of the window
HUD_HEIGHT = 40
# Grid dimensions (play field sits below the HUD)
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - HUD_HEIGHT) // GRID_SIZE
# Colors (R, G, B)
COLOR_BACKGROUND = (18, 18, 18)
COLOR_GRID = (30, 30, 30)
COLOR_SNAKE_HEAD = (0, 200, 0)
COLOR_SNAKE_BODY = (0, 150, 0)
COLOR_FOOD = (220, 40, 40)
COLOR_TEXT = (240, 240, 240)
COLOR_TITLE = (0, 200, 100)
COLOR_HIGHLIGHT = (255, 215, 0)
COLOR_DIM = (140, 140, 140)
COLOR_OVERLAY = (0, 0, 0)
# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
# Difficulty levels: name -> speed in FPS and score multiplier
DIFFICULTY_LEVELS = {
    "Easy": {"speed": 8, "multiplier": 1},
    "Medium": {"speed": 12, "multiplier": 2},
    "Hard": {"speed": 18, "multiplier": 3},
}
# Scoring
POINTS_PER_FOOD = 1
# Input buffering: maximum number of queued direction changes so that
# rapid sequential turns (e.g., Up then Left) register on consecutive
# ticks instead of being silently dropped.
MAX_DIRECTION_QUEUE = 3
# High score persistence
HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_score.txt")
# Fonts
FONT_NAME = None  # use default pygame font