"""
settings.py
Central configuration for the Flappy Bird clone.
All tunable gameplay constants (physics, pipe generation, difficulty
progression, colours and UI layout) live here so the game can be
re-balanced from a single file.
"""
# ---------------------------------------------------------------------------
# Window / timing
# ---------------------------------------------------------------------------
WIDTH = 480                 # play-field width in pixels
HEIGHT = 720                # play-field height in pixels
FPS = 60                    # target frames per second
TITLE = "Flappy Bird"      # window caption
# ---------------------------------------------------------------------------
# Physics (units: pixels & seconds)
# ---------------------------------------------------------------------------
GRAVITY = 1500.0            # downward acceleration applied to the bird
FLAP_STRENGTH = -420.0      # vertical velocity impulse of a flap
MAX_FALL_SPEED = 700.0      # terminal velocity while falling
# ---------------------------------------------------------------------------
# Bird
# ---------------------------------------------------------------------------
BIRD_X = 120.0              # fixed horizontal position of the bird
BIRD_RADIUS = 15.0          # body radius, also drives the drawn size
HITBOX_SHRINK = 0.80        # collision box scale (forgiving hit-box)
BIRD_START_Y_RATIO = 0.45   # spawn height as a fraction of HEIGHT
# ---------------------------------------------------------------------------
# Pipes
# ---------------------------------------------------------------------------
PIPE_WIDTH = 70             # pipe body width
PIPE_CAP_H = 26             # height of the wider pipe "cap"
PIPE_CAP_OVERHANG = 5       # how far the cap sticks out on each side
PIPE_MARGIN_X = 40.0        # pipes spawn this far beyond the right edge
PIPE_SPACING = 250.0        # horizontal distance between consecutive pipes
GAP_TOP_MARGIN = 70.0       # min distance between screen top and gap
GAP_BOTTOM_MARGIN = 70.0    # min distance between gap and ground
# ---------------------------------------------------------------------------
# Difficulty progression
# ---------------------------------------------------------------------------
BASE_SPEED = 170.0          # world scroll speed at score 0
MAX_SPEED = 330.0           # speed ceiling
SPEED_PER_POINT = 6.0       # speed gained for every point scored
BASE_GAP = 175.0            # vertical gap between pipes at score 0
MIN_GAP = 112.0             # smallest allowed gap
GAP_PER_POINT = 2.5         # gap shrinkage for every point scored
GAP_VARIATION = 20.0        # random +/- variation applied to each gap
# ---------------------------------------------------------------------------
# Ground
# ---------------------------------------------------------------------------
GROUND_HEIGHT = 90          # height of the ground strip
GROUND_STRIP = 14           # height of the green grass strip on top
GROUND_STRIPE_W = 24        # width of the scrolling grass pattern
# ---------------------------------------------------------------------------
# Scenery
# ---------------------------------------------------------------------------
CLOUD_COUNT = 6             # number of drifting background clouds
# ---------------------------------------------------------------------------
# Colours (R, G, B)
# ---------------------------------------------------------------------------
SKY_TOP = (108, 191, 206)
SKY_BOTTOM = (144, 214, 222)
CLOUD = (245, 250, 252)
PIPE_BODY = (94, 168, 76)
PIPE_DARK = (58, 118, 47)
PIPE_LIGHT = (140, 205, 110)
GROUND_TAN = (222, 216, 149)
GROUND_TAN_DARK = (206, 199, 130)
GRASS = (126, 200, 88)
GRASS_DARK = (88, 158, 62)
BIRD_BODY = (255, 204, 61)
BIRD_WING = (232, 162, 40)
BIRD_BELLY = (255, 236, 160)
BEAK = (255, 122, 51)
EYE_WHITE = (255, 255, 255)
EYE_BLACK = (40, 40, 40)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
SCORE_OUTLINE = (55, 90, 60)
PANEL = (24, 32, 44)
PANEL_ALPHA = 170
FLASH_ALPHA = 160