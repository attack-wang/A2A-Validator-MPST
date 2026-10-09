'''
settings.py
Central configuration for the Flappy Bird clone.
All tunable constants (screen size, physics, difficulty curve, colours)
live here so gameplay can be balanced without touching game logic.
'''
# ---------------------------------------------------------------------------
# Window / timing
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Flappy Bird"
# ---------------------------------------------------------------------------
# World layout
# ---------------------------------------------------------------------------
GROUND_HEIGHT = 90          # height of the scrolling ground strip
CEILING_MARGIN = 40         # min distance between pipe gap edge and screen top
GROUND_TILE_WIDTH = 24      # width of one scrolling ground stripe
# ---------------------------------------------------------------------------
# Bird physics
# ---------------------------------------------------------------------------
BIRD_X = 120
BIRD_RADIUS = 16
GRAVITY = 0.45
FLAP_VELOCITY = -8.5
MAX_FALL_SPEED = 12.0
MAX_ROTATION_UP = -25
MAX_ROTATION_DOWN = 80
# ---------------------------------------------------------------------------
# Pipes
# ---------------------------------------------------------------------------
PIPE_WIDTH = 70
PIPE_CAP_HEIGHT = 26
PIPE_CAP_OVERHANG = 5
PIPE_SPACING = 230
BASE_PIPE_SPEED = 3.0
MAX_PIPE_SPEED = 6.5
SPEED_INCREMENT = 0.08
BASE_GAP_SIZE = 175
MIN_GAP_SIZE = 120
GAP_DECREMENT = 1.8
GAP_VARIANCE = 12
MAX_GAP_SHIFT = 90          # max vertical jump between consecutive gap centres
# ---------------------------------------------------------------------------
# Game states
# ---------------------------------------------------------------------------
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
SKY_TOP = (120, 199, 222)
SKY_BOTTOM = (168, 224, 227)
CLOUD_WHITE = (245, 248, 250)
PIPE_GREEN = (92, 178, 62)
PIPE_DARK = (56, 118, 38)
PIPE_LIGHT = (140, 210, 105)
GROUND_GREEN = (222, 216, 149)
GROUND_DIRT = (196, 128, 82)
GROUND_GRASS = (126, 200, 88)
BIRD_YELLOW = (255, 204, 0)
BIRD_ORANGE = (255, 140, 0)
BIRD_WHITE = (255, 255, 255)
BIRD_BLACK = (30, 30, 30)
TEXT_WHITE = (255, 255, 255)
TEXT_SHADOW = (40, 60, 70)
TEXT_GOLD = (255, 200, 40)
OVERLAY_BLACK = (0, 0, 0)