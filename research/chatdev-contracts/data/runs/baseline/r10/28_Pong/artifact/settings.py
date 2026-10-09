'''
settings.py
Configuration constants for the two-player Pong game.
'''
# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CAPTION = "Two-Player Pong"
# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (60, 120, 255)
RED = (220, 60, 60)
GREY = (100, 100, 100)
# Paddle configuration
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
PADDLE_SPEED = 7
PADDLE_MARGIN = 20  # distance of paddles from left/right edges
# Ball configuration
BALL_SIZE = 14
BALL_INITIAL_SPEED_X = 6
BALL_INITIAL_SPEED_Y = 4
BALL_MAX_SPEED = 14
BALL_SPEED_INCREMENT = 0.4  # speed gained per paddle hit
# Scoring / win condition
WINNING_SCORE = 5
# Serve delay in frames (ball waits at center after a point)
SERVE_DELAY_FRAMES = 60
# Fonts
FONT_NAME = None  # use pygame default
SCORE_FONT_SIZE = 48
MESSAGE_FONT_SIZE = 32
SMALL_FONT_SIZE = 24