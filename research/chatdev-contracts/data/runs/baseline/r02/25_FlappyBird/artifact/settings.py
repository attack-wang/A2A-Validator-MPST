'''
Configuration constants for the Flappy Bird clone.
'''
# Screen
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Flappy Bird"
# Colors (R, G, B)
SKY_TOP = (112, 197, 206)
SKY_BOTTOM = (186, 232, 222)
GROUND_COLOR = (222, 184, 106)
GROUND_DARK = (196, 158, 84)
GRASS_COLOR = (106, 190, 82)
GRASS_DARK = (88, 160, 68)
PIPE_BODY = (92, 180, 80)
PIPE_LIGHT = (130, 210, 110)
PIPE_DARK = (60, 140, 55)
PIPE_OUTLINE = (40, 90, 40)
BIRD_BODY = (255, 204, 0)
BIRD_WING = (240, 160, 20)
BIRD_BEAK = (255, 120, 40)
BIRD_EYE = (30, 30, 30)
CLOUD_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
TEXT_SHADOW = (40, 40, 40)
SCORE_COLOR = (255, 255, 255)
# Bird physics (pixels per second / per second squared)
GRAVITY = 1500.0
FLAP_VELOCITY = -430.0
MAX_FALL_SPEED = 750.0
BIRD_X = 140  # fixed horizontal position
BIRD_RADIUS = 15
# Pipes
PIPE_WIDTH = 70
PIPE_CAP_HEIGHT = 26
PIPE_CAP_OVERHANG = 6
BASE_PIPE_SPEED = 160.0
MAX_PIPE_SPEED = 330.0
BASE_GAP_SIZE = 175.0
MIN_GAP_SIZE = 115.0
PIPE_SPACING = 230.0  # horizontal distance between pipes
MIN_PIPE_SPACING = 190.0
GAP_MARGIN = 70  # min distance of gap edges from screen top/ground
# Difficulty progression
SPEED_PER_POINT = 5.0
GAP_SHRINK_PER_POINT = 2.0
SPACING_SHRINK_PER_POINT = 1.0
# Ground
GROUND_HEIGHT = 90
def get_pipe_speed(score):
    """Return current pipe scroll speed based on score."""
    return min(BASE_PIPE_SPEED + score * SPEED_PER_POINT, MAX_PIPE_SPEED)
def get_gap_size(score):
    """Return current vertical gap size based on score."""
    return max(BASE_GAP_SIZE - score * GAP_SHRINK_PER_POINT, MIN_GAP_SIZE)
def get_pipe_spacing(score):
    """Return horizontal spacing between pipes based on score."""
    return max(PIPE_SPACING - score * SPACING_SHRINK_PER_POINT, MIN_PIPE_SPACING)