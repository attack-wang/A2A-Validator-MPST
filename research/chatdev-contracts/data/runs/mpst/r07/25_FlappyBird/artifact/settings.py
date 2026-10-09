"""
settings.py
Central configuration for the Flappy Bird clone: window dimensions,
physics constants, difficulty tuning, colours and file paths.
"""
# ---------------------------------------------------------------- window
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
TITLE = "Flappy Bird"
FPS = 60
# ---------------------------------------------------------------- files
HIGHSCORE_FILE = "highscore.json"
# ---------------------------------------------------------------- bird
BIRD_X = 120
BIRD_RADIUS = 15
GRAVITY = 0.5
FLAP_STRENGTH = -9.0
MAX_FALL_SPEED = 12.0
# ---------------------------------------------------------------- pipes
PIPE_WIDTH = 70
PIPE_CAP_HEIGHT = 26
PIPE_CAP_OVERHANG = 5
PIPE_SPEED_START = 3.0
PIPE_SPEED_MAX = 6.5
PIPE_SPEED_PER_POINT = 0.08
PIPE_GAP_START = 175
PIPE_GAP_MIN = 110
PIPE_GAP_PER_POINT = 2.0
PIPE_SPACING = 260
FIRST_PIPE_DELAY = 90
GAP_CENTER_MARGIN = 60
# ---------------------------------------------------------------- ground
GROUND_HEIGHT = 90
# ---------------------------------------------------------------- colours
SKY_TOP = (78, 192, 202)
SKY_BOTTOM = (140, 210, 230)
CLOUD = (255, 255, 255)
PIPE_BODY = (92, 178, 62)
PIPE_BODY_LIGHT = (150, 220, 110)
PIPE_BODY_DARK = (56, 128, 40)
PIPE_OUTLINE = (30, 80, 30)
GROUND_DIRT = (222, 184, 135)
GROUND_DIRT_DARK = (190, 150, 105)
GRASS = (110, 200, 80)
GRASS_DARK = (70, 150, 55)
GRASS_EDGE = (200, 240, 160)
BIRD_BODY = (250, 210, 60)
BIRD_BODY_DARK = (180, 130, 20)
BIRD_BELLY = (255, 240, 180)
BIRD_WING = (240, 170, 40)
BEAK = (255, 120, 40)
BEAK_DARK = (200, 80, 20)
EYE_WHITE = (255, 255, 255)
EYE_BLACK = (30, 30, 30)
TEXT_WHITE = (255, 255, 255)
TEXT_GOLD = (255, 215, 80)
TEXT_RED = (230, 70, 60)
TEXT_OUTLINE = (40, 40, 40)
PANEL = (245, 235, 210)
PANEL_OUTLINE = (120, 90, 60)