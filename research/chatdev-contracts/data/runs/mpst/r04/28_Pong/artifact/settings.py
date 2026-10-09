'''
settings.py
Global configuration constants for the two-player Pong game.
'''
# Screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "ChatDev Pong - Two Player"
# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
BLUE = (80, 160, 255)
RED = (255, 90, 90)
YELLOW = (255, 210, 60)
# Paddle
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7
PADDLE_MARGIN = 20  # distance of paddles from side edges
# Ball
BALL_SIZE = 14
BALL_INITIAL_SPEED_X = 6.0
BALL_INITIAL_SPEED_Y = 4.0
BALL_SPEED_INCREMENT = 0.4
BALL_MAX_SPEED = 14.0
MAX_BOUNCE_ANGLE = 60  # degrees, max vertical angle off paddle
# Scoring
WINNING_SCORE = 5
SERVE_DELAY_FRAMES = 60  # frames to wait before ball moves after a point
# Fonts
FONT_SIZE_SCORE = 60
FONT_SIZE_TEXT = 28
FONT_SIZE_TITLE = 64