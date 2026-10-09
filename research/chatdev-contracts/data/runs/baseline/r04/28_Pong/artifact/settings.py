'''
settings.py
Global configuration constants for the two-player Pong game.
Tweak values here to adjust gameplay without touching the game logic.
'''
import pygame
# ---------------------------------------------------------------------------
# Window / loop
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
WINDOW_CAPTION = "Pong - Two Player"
FPS = 60
MAX_DT = 1.0 / 30.0  # clamp for frame hitches (prevents tunneling)
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (15, 15, 30)
COLOR_FOREGROUND = (235, 235, 235)
COLOR_PADDLE_LEFT = (80, 200, 255)
COLOR_PADDLE_RIGHT = (255, 110, 110)
COLOR_BALL = (250, 250, 250)
COLOR_SCORE = (190, 190, 210)
COLOR_MESSAGE = (255, 215, 120)
COLOR_CENTER_LINE = (70, 70, 100)
# ---------------------------------------------------------------------------
# Paddle
# ---------------------------------------------------------------------------
PADDLE_WIDTH = 14
PADDLE_HEIGHT = 96
PADDLE_SPEED = 430.0        # pixels per second
PADDLE_MARGIN = 26          # distance from side walls
PADDLE_CORNER_RADIUS = 4
# ---------------------------------------------------------------------------
# Ball
# ---------------------------------------------------------------------------
BALL_RADIUS = 8
BALL_INITIAL_SPEED = 330.0  # pixels per second at serve
BALL_MAX_SPEED = 760.0
BALL_SPEEDUP_PER_HIT = 1.045  # speed multiplier after every paddle hit
BALL_MAX_BOUNCE_ANGLE = 60.0  # max deflection (degrees) off a paddle edge
BALL_SERVE_MAX_ANGLE = 30.0   # max random serve angle (degrees)
# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
WINNING_SCORE = 5
# ---------------------------------------------------------------------------
# Fonts (None -> pygame default font)
# ---------------------------------------------------------------------------
FONT_NAME = None
FONT_SIZE_SCORE = 72
FONT_SIZE_MESSAGE = 30
FONT_SIZE_SMALL = 20
# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------
CONTROLS = {
    "left": {"up": pygame.K_w, "down": pygame.K_s},
    "right": {"up": pygame.K_UP, "down": pygame.K_DOWN},
}