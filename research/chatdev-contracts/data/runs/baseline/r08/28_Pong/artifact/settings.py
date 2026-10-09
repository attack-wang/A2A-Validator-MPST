'''
Central configuration for the two-player Pong game.
All tunable numbers (sizes, speeds, colors, scoring rules) live here so the
game can be balanced without touching gameplay code.
'''
# --- Window -----------------------------------------------------------------
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
WINDOW_CAPTION = "Pong - Two Player"
FPS = 60
MAX_DT = 1.0 / 30.0  # clamp for the frame delta-time to avoid physics jumps
# --- Colors (R, G, B) -------------------------------------------------------
COLOR_BACKGROUND = (16, 18, 28)
COLOR_CENTER_LINE = (60, 64, 84)
COLOR_BALL = (245, 245, 245)
COLOR_PADDLE_LEFT = (86, 156, 245)
COLOR_PADDLE_RIGHT = (240, 110, 90)
COLOR_TEXT = (235, 235, 235)
COLOR_TEXT_DIM = (140, 145, 160)
# --- Paddles ----------------------------------------------------------------
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 430.0        # pixels per second
PADDLE_MARGIN = 24          # distance between paddle and side wall
# --- Ball -------------------------------------------------------------------
BALL_DIAMETER = 14
BALL_INITIAL_SPEED = 330.0  # pixels per second
BALL_MAX_SPEED = 760.0
BALL_SPEEDUP = 1.045        # speed multiplier on every paddle hit
BALL_MAX_BOUNCE_ANGLE = 60.0  # steepest deflection from horizontal, degrees
# --- Scoring ----------------------------------------------------------------
WINNING_SCORE = 5
SERVE_DELAY = 1.0           # seconds between a point and the next serve
# --- Fonts ------------------------------------------------------------------
FONT_NAME = None            # None -> pygame's built-in font
SCORE_FONT_SIZE = 64
MESSAGE_FONT_SIZE = 34
SMALL_FONT_SIZE = 20