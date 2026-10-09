'''
constants.py
Central configuration module that stores all game constants such as
window dimensions, paddle/ball parameters, colors, and the winning score.
'''
import math
# General game settings
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINNING_SCORE = 5
# Paddle settings
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
PADDLE_SPEED = 7
PADDLE_OFFSET = 30  # distance of paddles from left/right edges
# Ball settings
BALL_SIZE = 12
BALL_INITIAL_SPEED = 6
BALL_SPEEDUP_FACTOR = 1.05  # slight speed-up on each paddle hit
MAX_BALL_SPEED = 14
MAX_BOUNCE_ANGLE = math.radians(60)  # max deflection angle when hit at paddle edge
# Colors (R, G, B)
COLOR_BACKGROUND = (20, 20, 30)
COLOR_FOREGROUND = (240, 240, 240)
COLOR_PADDLE_LEFT = (80, 200, 120)
COLOR_PADDLE_RIGHT = (240, 100, 100)
COLOR_BALL = (255, 255, 255)
COLOR_TEXT = (240, 240, 240)
COLOR_CENTER_LINE = (90, 90, 110)
# Fonts
FONT_SIZE_SCORE = 60
FONT_SIZE_MESSAGE = 32
FONT_SIZE_HINT = 20