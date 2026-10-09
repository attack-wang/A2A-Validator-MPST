'''
settings.py
Central configuration module for the two-player Pong game.
Every tunable value of the game lives here: window dimensions,
colors, paddle and ball physics, scoring rules and font sizes.
'''
# ---------------------------------------------------------------- screen ----
SCREEN_WIDTH = 900            # play field width in pixels
SCREEN_HEIGHT = 600           # play field height in pixels
FPS = 60                      # target frames per second
WINDOW_TITLE = "ChatDev Pong - Two Player"
# ---------------------------------------------------------------- colors ----
BLACK = (15, 15, 25)          # background
WHITE = (240, 240, 240)       # main text
LINE_COLOR = (90, 90, 110)    # center line / subtle elements
HINT_COLOR = (130, 130, 150)  # small helper texts
PADDLE_L_COLOR = (80, 200, 120)   # Player 1 paddle (green)
PADDLE_R_COLOR = (235, 90, 90)    # Player 2 paddle (red)
BALL_COLOR = (250, 250, 120)      # ball (yellow)
# --------------------------------------------------------------- paddles ----
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7              # pixels per frame
PADDLE_MARGIN = 25            # distance of paddles from screen edges
# ----------------------------------------------------------------- ball -----
BALL_SIZE = 14                # diameter in pixels
BALL_INITIAL_SPEED = 6.0      # pixels per frame at serve time
BALL_SPEED_INCREMENT = 0.35   # speed gained after every paddle hit
BALL_MAX_SPEED = 13.0         # speed cap
MAX_BOUNCE_ANGLE = 60         # max deflection angle off a paddle (degrees)
SERVE_DELAY_FRAMES = 60       # pause (frames) after each point before serve
# -------------------------------------------------------------- scoring -----
WINNING_SCORE = 5             # first player to reach this wins the match
# ---------------------------------------------------------------- fonts -----
SCORE_FONT_SIZE = 64
TITLE_FONT_SIZE = 72
TEXT_FONT_SIZE = 28
SMALL_FONT_SIZE = 20