'''
Configuration constants for the Flappy Bird clone.
'''
# Screen / timing
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
# Bird physics (units: pixels, seconds)
GRAVITY = 1400.0
FLAP_STRENGTH = -420.0
MAX_FALL_SPEED = 700.0
BIRD_RADIUS = 14
BIRD_X = 120
# Pipes
PIPE_WIDTH = 70
PIPE_CAP_HEIGHT = 26
BASE_GAP_SIZE = 175.0
MIN_GAP_SIZE = 115.0
GAP_VARIANCE = 25.0  # random +/- variance around target gap
BASE_PIPE_SPEED = 150.0
MAX_PIPE_SPEED = 300.0
PIPE_SPAWN_DISTANCE = 240.0  # horizontal distance between pipe spawns
PIPE_SPAWN_MARGIN = 60.0  # min vertical clearance from ceiling/ground to gap edges
# Difficulty ramp
DIFFICULTY_SCORE_SPAN = 30  # score at which max difficulty is reached
# Ground
GROUND_HEIGHT = 80
GROUND_SPEED_FACTOR = 1.0  # ground scrolls at pipe speed
# Persistence
BEST_SCORE_FILE = "best_score.txt"
# Colors
SKY_TOP = (113, 197, 207)
SKY_BOTTOM = (196, 232, 240)
CLOUD_COLOR = (255, 255, 255)
PIPE_BODY = (92, 184, 92)
PIPE_EDGE = (60, 145, 60)
PIPE_HIGHLIGHT = (140, 215, 140)
GROUND_COLOR = (222, 184, 121)
GROUND_DARK = (196, 158, 100)
GRASS_COLOR = (110, 200, 90)
GRASS_EDGE = (80, 140, 70)
BIRD_BODY = (255, 204, 0)
BIRD_WING = (255, 160, 0)
BIRD_BEAK = (255, 120, 40)
BIRD_EYE = (30, 30, 30)
BIRD_BELLY = (255, 230, 120)
TEXT_COLOR = (255, 255, 255)
TEXT_OUTLINE = (40, 40, 40)
FLASH_COLOR = (255, 255, 255)
FLASH_ALPHA = 120