"""Central configuration constants for the Flappy Bird clone."""
# --- Screen / timing ---
WIDTH = 480
HEIGHT = 720
FPS = 60
TITLE = "Flappy Bird - ChatDev Edition"
# --- Colors (R, G, B) ---
SKY_TOP = (78, 192, 202)
SKY_BOTTOM = (140, 210, 230)
CLOUD_COLOR = (255, 255, 255)
PIPE_GREEN = (94, 190, 92)
PIPE_DARK = (60, 140, 60)
PIPE_LIGHT = (140, 220, 130)
GROUND_COLOR = (222, 184, 135)
GRASS_COLOR = (106, 190, 88)
GRASS_DARK = (80, 150, 66)
BIRD_BODY = (255, 204, 0)
BIRD_WING = (230, 170, 20)
BIRD_BEAK = (255, 120, 40)
BIRD_EYE = (255, 255, 255)
BIRD_PUPIL = (30, 30, 30)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
SCORE_COLOR = (255, 255, 255)
SCORE_OUTLINE = (0, 0, 0)
PANEL_COLOR = (240, 240, 230)
PANEL_BORDER = (90, 90, 90)
# --- Ground ---
GROUND_HEIGHT = 100
# --- Bird physics (units: pixels, seconds) ---
BIRD_X = 120
BIRD_RADIUS = 16
GRAVITY = 1500.0
FLAP_VELOCITY = -420.0
MAX_FALL_SPEED = 700.0
# --- Pipes / difficulty ---
PIPE_WIDTH = 70
PIPE_SPACING = 260
GAP_MARGIN = 60
BASE_GAP = 190
MIN_GAP = 130
GAP_SHRINK_PER_POINT = 2.5
BASE_SPEED = 160.0
MAX_SPEED = 320.0
SPEED_INCREMENT_PER_POINT = 4.0