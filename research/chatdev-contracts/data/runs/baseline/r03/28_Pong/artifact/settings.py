'''
settings.py
Central configuration module for the Pong game.
All tunable constants (window size, colours, physics parameters,
scoring rules, etc.) live here so that the rest of the code never
hard-codes magic numbers and the game can be tweaked from one place.
'''
# ---------------------------------------------------------------------------
# Window / frame-rate
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 900          # playfield width in pixels
SCREEN_HEIGHT = 600         # playfield height in pixels
FPS = 60                    # target frames per second
WINDOW_TITLE = "Pong - Two Player"
# ---------------------------------------------------------------------------
# Colours (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (15, 15, 25)
COLOR_FOREGROUND = (240, 240, 240)
COLOR_PADDLE_LEFT = (80, 200, 255)
COLOR_PADDLE_RIGHT = (255, 120, 90)
COLOR_BALL = (255, 235, 59)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (120, 220, 120)
# ---------------------------------------------------------------------------
# Paddle
# ---------------------------------------------------------------------------
PADDLE_WIDTH = 14
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7            # pixels per frame
PADDLE_MARGIN = 20          # distance of paddles from left/right walls
# ---------------------------------------------------------------------------
# Ball
# ---------------------------------------------------------------------------
BALL_SIZE = 14              # ball is a square of BALL_SIZE x BALL_SIZE pixels
BALL_INITIAL_SPEED = 6.0    # horizontal speed at serve (pixels per frame)
BALL_INITIAL_VY = 2.5       # small vertical drift at serve
BALL_SPEED_UP = 0.35        # speed gained after every paddle hit
BALL_MAX_SPEED = 13.0       # upper bound for ball speed
MAX_BOUNCE_ANGLE = 60       # max deflection angle off a paddle, in degrees
# ---------------------------------------------------------------------------
# Scoring / match rules
# ---------------------------------------------------------------------------
WINNING_SCORE = 5           # first player to reach this score wins
SERVE_DELAY_FRAMES = 60     # ~1 second pause between a point and the serve