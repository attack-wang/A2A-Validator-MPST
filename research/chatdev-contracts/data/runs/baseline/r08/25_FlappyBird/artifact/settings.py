'''
Configuration constants for the Flappy Bird clone.
'''
# Screen
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
# Colors (R, G, B)
SKY_BLUE = (113, 197, 207)
GROUND_COLOR = (222, 184, 135)
GROUND_DARK = (196, 154, 108)
PIPE_GREEN = (111, 196, 69)
PIPE_DARK = (76, 145, 44)
PIPE_LIGHT = (144, 224, 100)
BIRD_YELLOW = (255, 204, 0)
BIRD_ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
CLOUD_COLOR = (255, 255, 255)
# Physics
GRAVITY = 1400.0  # pixels per second^2
FLAP_VELOCITY = -420.0  # pixels per second
MAX_FALL_SPEED = 700.0  # terminal velocity
# Bird
BIRD_RADIUS = 14
BIRD_START_X = 120
BIRD_START_Y = SCREEN_HEIGHT // 2
# Pipes
PIPE_WIDTH = 70
PIPE_CAP_HEIGHT = 26  # lip height
PIPE_CAP_OVERHANG = 6  # lip wider than shaft
BASE_GAP_SIZE = 190
MIN_GAP_SIZE = 120
GAP_DECREASE_PER_POINT = 2.5
GAP_RANDOM_VARIATION = 30  # random +/- variation
BASE_PIPE_SPEED = 160.0
MAX_PIPE_SPEED = 340.0
SPEED_INCREASE_PER_POINT = 6.0
PIPE_SPAWN_DISTANCE = 260  # horizontal distance between pipes
# Ground
GROUND_HEIGHT = 80
# Scoring / difficulty
SCORE_PER_PIPE = 1
# Fonts
FONT_NAME = None  # default pygame font