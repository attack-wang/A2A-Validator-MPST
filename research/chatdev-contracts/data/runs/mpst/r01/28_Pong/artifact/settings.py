'''
Global configuration constants for the two-player Pong game:
window dimensions, colors, entity sizes, speeds, scoring rules,
key bindings and font settings.
'''
import pygame
# --------------------------------------------------------------------- #
# Window                                                                #
# --------------------------------------------------------------------- #
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pong — Two Player"
FPS = 60
# --------------------------------------------------------------------- #
# Colors (R, G, B)                                                      #
# --------------------------------------------------------------------- #
COLOR_BACKGROUND = (15, 15, 35)
COLOR_FOREGROUND = (235, 235, 235)
COLOR_PADDLE_LEFT = (235, 235, 235)
COLOR_PADDLE_RIGHT = (235, 235, 235)
COLOR_BALL = (235, 235, 235)
COLOR_SCORE = (235, 235, 235)
COLOR_MESSAGE = (235, 235, 235)
COLOR_CENTER_LINE = (70, 70, 100)
# --------------------------------------------------------------------- #
# Paddles                                                               #
# --------------------------------------------------------------------- #
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7          # pixels per frame
PADDLE_MARGIN = 25        # distance from the left/right window edges
# --------------------------------------------------------------------- #
# Ball                                                                  #
# --------------------------------------------------------------------- #
BALL_SIZE = 12                      # square ball edge length (pixels)
BALL_INITIAL_SPEED_X = 5.0          # horizontal speed at each serve
BALL_MAX_SERVE_ANGLE = 30.0         # max random serve deflection (degrees)
BALL_MAX_BOUNCE_ANGLE = 60.0        # max deflection off a paddle (degrees)
BALL_SPEED_INCREMENT = 0.4          # speed gained per paddle hit
BALL_MAX_SPEED = 13.0               # speed cap
# --------------------------------------------------------------------- #
# Scoring / flow                                                        #
# --------------------------------------------------------------------- #
WINNING_SCORE = 5         # first player to reach this score wins
SERVE_DELAY_MS = 1000     # pause after each point before the ball is served
# --------------------------------------------------------------------- #
# Controls                                                              #
# --------------------------------------------------------------------- #
KEY_LEFT_UP = pygame.K_w
KEY_LEFT_DOWN = pygame.K_s
KEY_RIGHT_UP = pygame.K_UP
KEY_RIGHT_DOWN = pygame.K_DOWN
KEY_RESTART = pygame.K_r
KEY_RESTART_NAME = "R"
# --------------------------------------------------------------------- #
# Fonts                                                                 #
# --------------------------------------------------------------------- #
FONT_NAME = None          # None -> pygame's built-in default font
FONT_SIZE_SCORE = 64
FONT_SIZE_MESSAGE = 34
FONT_SIZE_SMALL = 22