'''
settings.py
Central configuration for the Flappy Bird clone.
Every tunable value (window size, physics constants, difficulty ramp,
colors) lives here so the game can be balanced without touching any
game logic. All physics values use pixels and seconds, which keeps
movement frame-rate independent.
'''
# ---------------------------------------------------------------------------
# Window / timing
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Flappy Bird - ChatDev Edition"
MAX_DT = 0.05              # clamp for delta time (avoids tunneling after lag)
# ---------------------------------------------------------------------------
# Bird physics
# ---------------------------------------------------------------------------
GRAVITY = 1500.0           # downward acceleration (px/s^2)
FLAP_STRENGTH = -420.0     # upward velocity impulse on flap (px/s)
MAX_FALL_SPEED = 650.0     # terminal velocity (px/s)
# ---------------------------------------------------------------------------
# Bird appearance / collision
# ---------------------------------------------------------------------------
BIRD_RADIUS = 14
BIRD_START_X = 120
BIRD_START_Y = SCREEN_HEIGHT // 2 - 40
BIRD_HITBOX_SHRINK = 4     # px trimmed from each side of the hitbox
BIRD_ROTATION_UP = -25.0   # nose-up angle right after a flap (degrees)
BIRD_ROTATION_DOWN = 90.0  # nose-down angle at terminal velocity (degrees)
BIRD_ROTATION_SPEED = 480.0  # nose-down rotation speed (degrees/s)
# ---------------------------------------------------------------------------
# Pipes
# ---------------------------------------------------------------------------
PIPE_WIDTH = 64
PIPE_CAP_HEIGHT = 26       # decorative lip at the gap-facing end
PIPE_CAP_OVERHANG = 4      # how much wider the cap is than the body
PIPE_GAP_START = 175       # gap size at difficulty level 0 (px)
PIPE_GAP_MIN = 115         # smallest allowed gap (px)
PIPE_GAP_STEP = 7          # gap shrink per difficulty level (px)
PIPE_SPEED_START = 150.0   # scroll speed at difficulty level 0 (px/s)
PIPE_SPEED_MAX = 300.0     # scroll speed cap (px/s)
PIPE_SPEED_STEP = 14.0     # speed gain per difficulty level (px/s)
PIPE_SPACING = 230         # horizontal distance between pipe pairs (px)
PIPE_MARGIN_TOP = 70       # min distance from screen top to gap top
PIPE_MARGIN_BOTTOM = 90    # min distance from gap bottom to ground
PIPE_MAX_GAP_SHIFT = 150   # max vertical jump between consecutive gaps (px)
# ---------------------------------------------------------------------------
# Difficulty progression
# ---------------------------------------------------------------------------
SCORE_PER_LEVEL = 4        # points required to advance one difficulty level
# ---------------------------------------------------------------------------
# Ground / scenery
# ---------------------------------------------------------------------------
GROUND_HEIGHT = 80
GRASS_HEIGHT = 12
GROUND_STRIPE_WIDTH = 24   # horizontal spacing of ground decorations (px)
CLOUD_COUNT = 5
# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
RESTART_DELAY = 0.45       # seconds before restart input is accepted
BEST_SCORE_FILE = "best_score.txt"
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_SKY_TOP = (78, 172, 190)
COLOR_SKY_BOTTOM = (168, 219, 220)
COLOR_CLOUD = (255, 255, 255)
COLOR_GRASS = (106, 190, 82)
COLOR_GRASS_DARK = (85, 158, 64)
COLOR_GROUND = (222, 184, 135)
COLOR_GROUND_STRIPE = (205, 160, 110)
COLOR_PIPE = (111, 196, 69)
COLOR_PIPE_LIGHT = (150, 222, 105)
COLOR_PIPE_DARK = (76, 145, 44)
COLOR_PIPE_OUTLINE = (52, 105, 30)
COLOR_BIRD_BODY = (255, 204, 0)
COLOR_BIRD_BODY_LIGHT = (255, 232, 105)
COLOR_BIRD_WING = (255, 152, 0)
COLOR_BIRD_BEAK = (255, 87, 34)
COLOR_BIRD_EYE_WHITE = (255, 255, 255)
COLOR_BIRD_EYE = (33, 33, 33)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_SHADOW = (0, 0, 0)
COLOR_PANEL = (0, 0, 0)