'''
Configuration constants for the Flappy Bird clone.
'''
# Window / loop
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Flappy Bird"
FPS = 60
GROUND_HEIGHT = 80
# Bird physics & animation
BIRD_X = 80
BIRD_RADIUS = 14
GRAVITY = 0.5
FLAP_STRENGTH = -9.0        # negative = upward impulse
MAX_FALL_SPEED = 10.0
MAX_ROTATION_UP = 25.0
MAX_ROTATION_DOWN = 70.0
ROTATION_SPEED_UP = 3.0
ROTATION_SPEED_DOWN = 4.0
# Pipes & difficulty scaling
PIPE_WIDTH = 60
PIPE_CAP_HEIGHT = 24
PIPE_CAP_OVERHANG = 5
PIPE_SPACING = 190
BASE_GAP_HEIGHT = 170       # gap height at score 0
MIN_GAP_HEIGHT = 115        # smallest gap at max difficulty
BASE_PIPE_SPEED = 2.5
MAX_PIPE_SPEED = 5.0
DIFFICULTY_SCORE = 30       # score at which difficulty caps out
GAP_MARGIN_TOP = 60
GAP_MARGIN_BOTTOM = 60
# HUD / persistence / effects
FONT_SIZE_SCORE = 40
FONT_SIZE_TEXT = 34
FONT_SIZE_SMALL = 20
DEATH_FLASH_FRAMES = 20
HIGHSCORE_FILE = "highscore.txt"
CLOUD_SEED = 42
CLOUD_COUNT = 6
# Colors
SKY_TOP = (78, 182, 235)
SKY_BOTTOM = (150, 222, 240)
BIRD_BODY = (255, 204, 0)
BIRD_WING = (255, 160, 20)
BIRD_EYE = (255, 255, 255)
BIRD_PUPIL = (30, 30, 30)
BIRD_BEAK = (255, 120, 40)
PIPE_BODY = (90, 190, 90)
PIPE_LIGHT = (150, 230, 150)
PIPE_OUTLINE = (40, 110, 40)
GROUND_BODY = (222, 184, 135)
GROUND_TOP = (110, 200, 80)
GROUND_LINE = (85, 170, 60)
GROUND_DARK = (170, 130, 90)
WHITE = (255, 255, 255)
SCORE_OUTLINE = (40, 40, 40)
PANEL_COLOR = (250, 250, 250)
PANEL_BORDER = (70, 70, 70)
GAME_OVER_COLOR = (225, 60, 60)