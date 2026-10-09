'''
constants.py
Global configuration constants for the two-player Pong game.
'''
# Window settings
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pong - Two Player"
FPS = 60
# Colors (R, G, B)
COLOR_BACKGROUND = (20, 20, 30)
COLOR_FOREGROUND = (240, 240, 240)
COLOR_PADDLE_LEFT = (80, 200, 255)
COLOR_PADDLE_RIGHT = (255, 120, 80)
COLOR_BALL = (255, 255, 255)
COLOR_TEXT = (240, 240, 240)
COLOR_CENTER_LINE = (90, 90, 110)
COLOR_WINNER = (120, 255, 140)
# Paddle settings
PADDLE_WIDTH = 14
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7
PADDLE_MARGIN = 24  # distance of paddles from left/right edges
# Ball settings
BALL_SIZE = 14
BALL_INITIAL_SPEED = 6.0
BALL_SPEED_INCREMENT = 0.35  # speed gained per paddle hit
BALL_MAX_SPEED = 14.0
BALL_MAX_BOUNCE_ANGLE = 60  # degrees, max vertical deflection off paddle
# Scoring / match settings
WINNING_SCORE = 5
POINT_PAUSE_SECONDS = 1.2  # delay after a point before serving
# Fonts
FONT_MAIN_SIZE = 28
FONT_SCORE_SIZE = 56
FONT_SMALL_SIZE = 20