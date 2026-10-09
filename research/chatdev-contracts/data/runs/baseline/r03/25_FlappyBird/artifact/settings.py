'''
Configuration constants for the Flappy Bird clone.
Complete set of tuning values and colors shared by bird.py, pipe.py and
game.py, guaranteeing that every settings.* attribute referenced in the
codebase is defined (window, bird physics, pipes, difficulty ramp, ground,
fonts and colors).
'''
# ----- window -----
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
TITLE = "Flappy Bird"
FPS = 60
# ----- bird physics -----
GRAVITY = 0.5
FLAP_STRENGTH = -9.0          # negative = upward impulse (y grows downward)
MAX_FALL_SPEED = 12.0
BIRD_RADIUS = 14
BIRD_X = 120
# ----- pipes -----
PIPE_WIDTH = 70
PIPE_CAP_HEIGHT = 26
PIPE_CAP_OVERHANG = 5
PIPE_MARGIN = 60
PIPE_SPAWN_DISTANCE = 220     # horizontal distance between pipe pairs
# ----- difficulty ramp -----
BASE_PIPE_SPEED = 3.0
MAX_PIPE_SPEED = 6.0
BASE_GAP_SIZE = 190.0
MIN_GAP_SIZE = 120.0
GAP_VARIANCE = 15.0
DIFFICULTY_RAMP_SCORE = 25    # score at which maximum difficulty is reached
# ----- ground -----
GROUND_HEIGHT = 80
# ----- fonts -----
FONT_LARGE = 48
FONT_MEDIUM = 32
FONT_SMALL = 22
# ----- colors -----
SKY_BLUE = (113, 197, 207)
CLOUD_COLOR = (255, 255, 255)
GROUND_COLOR = (222, 184, 135)
GROUND_DARK = (205, 133, 63)
YELLOW = (255, 221, 0)
ORANGE = (255, 140, 0)
GREEN = (90, 190, 90)
DARK_GREEN = (40, 120, 40)
LIGHT_GREEN = (150, 230, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)