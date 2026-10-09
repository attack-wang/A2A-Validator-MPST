'''
settings.py
Central configuration for the Flappy Bird clone.
All tunable constants (screen, physics, difficulty, colors) live here.
'''
# --- Window ---
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Flappy Bird - ChatDev Edition"
# --- Ground ---
GROUND_HEIGHT = 80
GROUND_TILE = 24               # width of one scrolling ground stripe (px)
# --- Bird physics (units per second) ---
GRAVITY = 1400.0          # downward acceleration (px/s^2)
FLAP_VELOCITY = -420.0    # upward impulse (px/s)
MAX_FALL_SPEED = 700.0    # terminal velocity (px/s)
BIRD_RADIUS = 14
# --- Pipes ---
PIPE_WIDTH = 60
BASE_PIPE_SPEED = 160.0        # starting horizontal speed (px/s)
MAX_PIPE_SPEED = 320.0         # speed cap (px/s)
SPEED_GAIN_PER_POINT = 4.0     # speed added per point
BASE_GAP_SIZE = 170            # starting vertical gap (px)
MIN_GAP_SIZE = 110             # smallest gap (px)
GAP_SHRINK_PER_POINT = 2.0     # gap reduction per point
GAP_RANDOMNESS = 30            # random extra variation of the gap
PIPE_SPAWN_DISTANCE = 230      # horizontal distance between pipes (px)
# --- Scoring / difficulty ---
DIFFICULTY_RAMP_START = 0      # score at which difficulty ramping begins
# --- Colors ---
SKY_TOP = (112, 197, 206)
SKY_BOTTOM = (196, 231, 229)
BIRD_COLOR = (255, 204, 0)
BIRD_WING = (255, 153, 51)
BIRD_BEAK = (255, 87, 34)
PIPE_BODY = (76, 175, 80)
PIPE_EDGE = (46, 125, 50)
PIPE_HIGHLIGHT = (129, 199, 132)
GROUND_COLOR = (222, 184, 135)
GROUND_DARK = (205, 170, 125)
GRASS_COLOR = (101, 193, 84)
TEXT_COLOR = (255, 255, 255)
TEXT_SHADOW = (0, 0, 0)
GAME_OVER_COLOR = (231, 76, 60)