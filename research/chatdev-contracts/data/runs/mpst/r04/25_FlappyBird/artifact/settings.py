'''
settings.py
Single source of truth for every tuning constant, colour and helper
used by the Flappy Bird clone.  Difficulty (pipe speed, gap size and
spawn interval) is derived from the current score with simple linear
formulas that are clamped so the game stays playable.
'''
import os
# ---------------------------------------------------------------- window
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Flappy Bird"
# ---------------------------------------------------------------- layout
GROUND_HEIGHT = 90
SKY_HEIGHT = SCREEN_HEIGHT - GROUND_HEIGHT
# ---------------------------------------------------------------- physics
GRAVITY = 1500.0          # px/s^2 pulling the bird down
FLAP_VELOCITY = -420.0    # upward impulse when the player flaps
MAX_FALL_SPEED = 750.0    # terminal velocity
BIRD_X = 100              # fixed horizontal position of the bird
BIRD_RADIUS = 12          # unused by collision (rect based) but handy
# ---------------------------------------------------------------- pipes
PIPE_WIDTH = 70
BASE_PIPE_SPEED = 160.0   # px/s at score 0
MAX_PIPE_SPEED = 330.0    # px/s cap
SPEED_PER_POINT = 6.0     # speed gained per point
BASE_GAP = 175            # vertical gap in px at score 0
MIN_GAP = 115             # gap floor
GAP_PER_POINT = 2.0       # gap shrink per point
BASE_SPAWN_INTERVAL = 1.45  # seconds between pipes at score 0
MIN_SPAWN_INTERVAL = 1.05   # spawn-interval floor
SPAWN_PER_POINT = 0.008     # interval shrink per point
GAP_MARGIN = 45            # min distance of gap edges from sky top/bottom
def pipe_speed_for_score(score):
    """Pipe scroll speed grows linearly with score, capped at MAX_PIPE_SPEED."""
    return min(MAX_PIPE_SPEED, BASE_PIPE_SPEED + score * SPEED_PER_POINT)
def gap_size_for_score(score):
    """Vertical gap shrinks with score, never below MIN_GAP."""
    return max(MIN_GAP, BASE_GAP - score * GAP_PER_POINT)
def spawn_interval_for_score(score):
    """Seconds between pipe spawns, shrinking with score, never below MIN."""
    return max(MIN_SPAWN_INTERVAL, BASE_SPAWN_INTERVAL - score * SPAWN_PER_POINT)
# ---------------------------------------------------------------- colours
SKY_BLUE = (113, 197, 207)
CLOUD_WHITE = (240, 249, 255)
BUSH_GREEN = (106, 190, 122)
BIRD_YELLOW = (255, 204, 0)
BIRD_LIGHT = (255, 236, 153)
BIRD_WING = (255, 179, 51)
BIRD_BEAK = (255, 102, 0)
BIRD_OUTLINE = (90, 60, 10)
PIPE_GREEN = (111, 196, 69)
PIPE_LIGHT = (163, 224, 93)
PIPE_DARK = (73, 141, 45)
PIPE_OUTLINE = (56, 96, 31)
GROUND_DIRT = (222, 184, 135)
GROUND_DIRT_DARK = (196, 154, 108)
GROUND_GRASS = (133, 212, 96)
GROUND_EDGE = (94, 160, 62)
TEXT_MAIN = (255, 255, 255)
TEXT_SHADOW = (60, 60, 60)
TEXT_MUTED = (120, 130, 140)
TEXT_ACCENT = (255, 120, 60)
NEW_BEST_COLOR = (255, 200, 40)
PANEL_COLOR = (250, 250, 245)
PANEL_BORDER = (120, 100, 80)
HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")