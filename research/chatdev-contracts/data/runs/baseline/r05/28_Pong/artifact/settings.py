'''
settings.py
Central configuration module for the two-player Pong game.
Holds every tunable constant (screen, colors, paddles, ball,
scoring, fonts) so gameplay can be adjusted from one place.
'''
# --- Screen configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CAPTION = "Pong - Two Player"
# --- Colors (R, G, B) ---
BLACK = (15, 15, 15)
WHITE = (240, 240, 240)
GRAY = (110, 110, 110)
GREEN = (80, 220, 100)
BLUE = (90, 160, 255)
# --- Paddle configuration ---
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
PADDLE_SPEED = 6
PADDLE_MARGIN = 30  # distance of each paddle from its screen edge
# --- Ball configuration ---
BALL_SIZE = 12
BALL_INITIAL_SPEED_X = 5.0
BALL_INITIAL_SPEED_Y = 3.0
BALL_SPEED_INCREMENT = 0.4   # speed gained per paddle hit
BALL_MAX_SPEED = 12.0        # speed cap so the ball stays playable
MAX_BOUNCE_ANGLE = 60        # steepest bounce angle off a paddle (degrees)
# --- Scoring configuration ---
WINNING_SCORE = 5            # first player to reach this score wins