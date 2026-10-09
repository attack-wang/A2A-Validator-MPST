'''
settings.py
Central configuration for the two-player Pong game.
Every tunable value lives here: window size, colours, paddle and ball
physics, control bindings and the match rules (winning score, serve
delay). Modify this file to rebalance the game without touching logic.
'''
import pygame
# ---------------------------------------------------------------------------
# Window / rendering
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 900          # playfield width in pixels
SCREEN_HEIGHT = 600         # playfield height in pixels
FPS = 60                    # target frames per second
WINDOW_TITLE = "Pong - Two Player"
# ---------------------------------------------------------------------------
# Colours (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (15, 15, 25)      # dark navy playfield
COLOR_FOREGROUND = (235, 235, 235)   # lines / neutral text
COLOR_PADDLE_LEFT = (80, 200, 255)   # player 1 (left) paddle
COLOR_PADDLE_RIGHT = (255, 110, 110) # player 2 (right) paddle
COLOR_BALL = (255, 255, 255)         # the ball
COLOR_TEXT = (235, 235, 235)         # generic UI text
COLOR_ACCENT = (255, 210, 70)        # highlights (titles, winner banner)
# ---------------------------------------------------------------------------
# Paddle
# ---------------------------------------------------------------------------
PADDLE_WIDTH = 14
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7           # pixels moved per frame while a key is held
PADDLE_MARGIN = 24         # gap between paddle and its side wall
# ---------------------------------------------------------------------------
# Ball
# ---------------------------------------------------------------------------
BALL_SIZE = 14                       # ball is a square of this side length
BALL_BASE_SPEED = 6.0                # speed right after each serve
BALL_SPEED_INCREMENT = 0.5           # speed gained on every paddle hit
BALL_MAX_SPEED = 13.0                # speed cap so the game stays playable
BALL_ANGLE_FACTOR = 6.0              # vertical deflection for a full-edge hit
# ---------------------------------------------------------------------------
# Match rules
# ---------------------------------------------------------------------------
WINNING_SCORE = 5          # first player to reach this score wins the match
SERVE_DELAY_FRAMES = 60    # pause after a point before the ball is served
# ---------------------------------------------------------------------------
# Controls (pygame key constants)
# ---------------------------------------------------------------------------
KEY_LEFT_UP = pygame.K_w       # player 1 move up
KEY_LEFT_DOWN = pygame.K_s     # player 1 move down
KEY_RIGHT_UP = pygame.K_UP     # player 2 move up
KEY_RIGHT_DOWN = pygame.K_DOWN # player 2 move down