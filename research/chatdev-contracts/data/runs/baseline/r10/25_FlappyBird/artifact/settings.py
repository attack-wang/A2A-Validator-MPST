'''
settings.py
Central configuration for the Flappy Bird clone.
Every tunable value used across the game lives here so that the physics,
difficulty curve and visuals can be adjusted from a single place.
'''
# ---------------------------------------------------------------------------
# Window / timing
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Flappy Bird"
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
SKY_COLOR = (111, 196, 229)
CLOUD_COLOR = (245, 250, 252)
BIRD_BODY = (255, 204, 0)
BIRD_WING = (255, 152, 0)
BIRD_BEAK = (255, 87, 34)
BIRD_EYE_WHITE = (255, 255, 255)
OUTLINE = (55, 44, 24)
PIPE_BODY = (92, 184, 92)
PIPE_DARK = (56, 142, 60)
PIPE_LIGHT = (139, 214, 137)
PIPE_CAP = (76, 175, 80)
GROUND_GRASS = (133, 187, 65)
GROUND_GRASS_DARK = (106, 152, 52)
GROUND_DIRT = (222, 184, 135)
GROUND_DIRT_DARK = (196, 156, 106)
TEXT_COLOR = (255, 255, 255)
TEXT_OUTLINE = (40, 40, 40)
PANEL_COLOR = (222, 216, 149)
SCORE_COLOR = (255, 255, 255)
# ---------------------------------------------------------------------------
# Bird physics
# ---------------------------------------------------------------------------
GRAVITY = 0.45            # downward acceleration per frame
FLAP_STRENGTH = -8.5      # upward impulse applied on flap
MAX_FALL_SPEED = 11.0     # terminal velocity
BIRD_START_X = 110
BIRD_START_Y = SCREEN_HEIGHT * 0.42
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BIRD_HITBOX_SHRINK = 6    # pixels removed from each side of the hitbox
MAX_ROTATION_UP = -25     # degrees, nose up while flapping
MAX_ROTATION_DOWN = 90    # degrees, nose dive when falling
# ---------------------------------------------------------------------------
# Pipes & difficulty
# ---------------------------------------------------------------------------
PIPE_WIDTH = 70
PIPE_CAP_HEIGHT = 26
PIPE_CAP_OVERHANG = 5     # how far the cap sticks out on each side
BASE_SPEED = 3.0          # starting horizontal scroll speed (px / frame)
MAX_SPEED = 7.0           # speed ceiling
SPEED_GAIN_PER_POINT = 0.09   # speed added for every point scored
BASE_GAP = 175            # starting vertical gap between pipe pair
MIN_GAP = 115             # smallest allowed gap
GAP_SHRINK_PER_POINT = 1.4    # gap reduction for every point scored
GAP_VARIATION = 15        # random +/- variation applied to every new gap
PIPE_SPACING = 240        # horizontal distance between consecutive pipes
PIPE_MARGIN = 70          # min distance of gap edges from top / ground
# ---------------------------------------------------------------------------
# Ground
# ---------------------------------------------------------------------------
GROUND_HEIGHT = 90
GROUND_STRIPE_WIDTH = 24  # width of one diagonal pattern tile
# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------
HIGHSCORE_FILE = "highscore.txt"
RESTART_DELAY_FRAMES = 30  # ignore restart input right after dying