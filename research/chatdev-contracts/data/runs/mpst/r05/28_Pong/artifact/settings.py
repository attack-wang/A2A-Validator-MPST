'''
settings.py
Central configuration for the two-player Pong game.
Every tunable value (window size, colors, physics constants, control
bindings and the winning score threshold) is collected here so the game
can be rebalanced or re-themed without touching any game logic.
'''
import pygame
# ---------------------------------------------------------------------------
# Window / loop configuration
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 900          # playable field width in pixels
WINDOW_HEIGHT = 600         # playable field height in pixels
WINDOW_CAPTION = "Two-Player Pong"
FPS = 60                    # target frames per second
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (15, 15, 30)
COLOR_CENTER_LINE = (70, 70, 100)
COLOR_PADDLE_LEFT = (80, 200, 255)
COLOR_PADDLE_RIGHT = (255, 120, 90)
COLOR_BALL = (245, 245, 245)
COLOR_TEXT = (235, 235, 235)
COLOR_SERVE_TEXT = (255, 220, 120)
COLOR_WIN_TEXT = (130, 255, 150)
COLOR_OVERLAY = (10, 10, 20)
# ---------------------------------------------------------------------------
# Paddle configuration
# ---------------------------------------------------------------------------
PADDLE_WIDTH = 14
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7            # pixels moved per frame while a key is held
PADDLE_MARGIN = 30          # horizontal distance from window edge
# ---------------------------------------------------------------------------
# Ball configuration
# ---------------------------------------------------------------------------
BALL_SIZE = 14              # square ball side length in pixels
BALL_INITIAL_SPEED = 6.0    # speed at every serve (pixels per frame)
BALL_MAX_SPEED = 14.0       # speed cap reached after repeated rallies
BALL_SPEED_INCREMENT = 0.5  # speed gained on every paddle hit
MAX_DEFLECTION_ANGLE = 60   # max vertical deflection off a paddle (degrees)
SERVE_MAX_ANGLE = 30        # max random serve angle (degrees)
# ---------------------------------------------------------------------------
# Scoring configuration
# ---------------------------------------------------------------------------
WINNING_SCORE = 7           # first player to reach this score wins the match
SERVE_DELAY_FRAMES = 60     # ~1 second pause between a point and the next serve
# ---------------------------------------------------------------------------
# Player controls
# ---------------------------------------------------------------------------
# Player 1 (left paddle)
KEY_LEFT_UP = pygame.K_w
KEY_LEFT_DOWN = pygame.K_s
# Player 2 (right paddle)
KEY_RIGHT_UP = pygame.K_UP
KEY_RIGHT_DOWN = pygame.K_DOWN
# Global keys
KEY_RESTART = pygame.K_SPACE
KEY_QUIT = pygame.K_ESCAPE