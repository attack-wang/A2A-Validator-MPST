'''
settings.py
Central configuration module for the Pong game.
All tunable constants (screen size, speeds, colours, keys, winning score)
live here so the rest of the code stays clean and easy to tweak.
'''
import pygame
# ----------------------------------------------------------------------------
# Window / frame-rate
# ----------------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WINDOW_CAPTION = "Pong - Two Player"
# ----------------------------------------------------------------------------
# Colours (R, G, B)
# ----------------------------------------------------------------------------
BACKGROUND_COLOR = (15, 15, 25)
FOREGROUND_COLOR = (240, 240, 240)
ACCENT_COLOR = (180, 180, 180)
# ----------------------------------------------------------------------------
# Paddle
# ----------------------------------------------------------------------------
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7
PADDLE_MARGIN = 30          # distance of each paddle from its screen edge
PLAYER1_UP_KEY = pygame.K_w
PLAYER1_DOWN_KEY = pygame.K_s
PLAYER2_UP_KEY = pygame.K_UP
PLAYER2_DOWN_KEY = pygame.K_DOWN
# ----------------------------------------------------------------------------
# Ball
# ----------------------------------------------------------------------------
BALL_SIZE = 14
BALL_INITIAL_SPEED = 6.0
BALL_SPEED_INCREMENT = 0.35   # speed gained after every paddle hit
BALL_MAX_SPEED = 14.0
BALL_MAX_BOUNCE_ANGLE = 45    # degrees, max deflection off a paddle
SERVE_DELAY_FRAMES = 45       # short pause after a point before the serve
# ----------------------------------------------------------------------------
# Scoring
# ----------------------------------------------------------------------------
WINNING_SCORE = 5
# ----------------------------------------------------------------------------
# Fonts
# ----------------------------------------------------------------------------
FONT_NAME = None              # None -> pygame's built-in default font
SCORE_FONT_SIZE = 72
MESSAGE_FONT_SIZE = 32
SMALL_FONT_SIZE = 20