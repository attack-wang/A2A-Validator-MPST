'''
Central configuration for the two-player Pong game.
Every tunable value (window size, colours, physics constants, scoring
rules) lives here so gameplay can be adjusted without touching logic.
This version uses plain hex colour strings and millisecond timing so it
works with the tkinter backend (Python standard library, no pygame).
'''
# --- Window --------------------------------------------------------- #
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
FRAME_DELAY_MS = max(1, round(1000 / FPS))  # delay between frames in ms
CAPTION = "Pong - Two Player"
# --- Colours (hex strings understood by tkinter) --------------------- #
COLOR_BACKGROUND = "#0f0f19"
COLOR_CENTER_LINE = "#46465a"
COLOR_TEXT = "#ebebeb"
COLOR_WIN_TEXT = "#78ff8c"
COLOR_PADDLE_LEFT = "#50c8ff"
COLOR_PADDLE_RIGHT = "#ff7878"
COLOR_BALL = "#ffe65a"
# --- Paddle ---------------------------------------------------------- #
PADDLE_WIDTH = 14
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7          # pixels per frame
PADDLE_MARGIN = 24        # distance between paddle and side wall
# --- Ball ------------------------------------------------------------ #
BALL_SIZE = 14
BALL_BASE_SPEED = 6       # launch speed in pixels per frame
BALL_MAX_SPEED = 13       # speed cap after repeated paddle hits
BALL_SPEEDUP_FACTOR = 1.04  # speed multiplier applied on every paddle hit
BALL_MAX_BOUNCE_ANGLE = 60  # maximum deflection angle (degrees) off a paddle
# --- Scoring ---------------------------------------------------------- #
WINNING_SCORE = 5          # first player to reach this score wins
SERVE_DELAY_FRAMES = 90    # pause (in frames) after each point before serve
# --- Fonts ------------------------------------------------------------ #
SCORE_FONT_NAME = "Consolas"
SCORE_FONT_SIZE = 48
MESSAGE_FONT_SIZE = 26
TITLE_FONT_SIZE = 56