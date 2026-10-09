'''
settings.py
Central configuration for the two-player Pong game.
All tunable constants (dimensions, colors, speeds, scoring) live here
so gameplay can be adjusted from a single file.
'''
# --- Window / loop -------------------------------------------------------
SCREEN_WIDTH = 800          # Playfield width in pixels
SCREEN_HEIGHT = 600         # Playfield height in pixels
FPS = 60                    # Target frames per second
CAPTION = "Pong - Two Player"
# --- Colors (R, G, B) ----------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
GREEN = (0, 200, 0)         # Player 1 paddle
BLUE = (60, 120, 230)       # Player 2 paddle
# --- Paddle --------------------------------------------------------------
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7            # Pixels per frame
PADDLE_MARGIN = 25          # Distance of paddles from side edges
# --- Ball ----------------------------------------------------------------
BALL_SIZE = 12
BALL_INITIAL_SPEED_X = 5.0
BALL_INITIAL_SPEED_Y = 4.0
BALL_MAX_SPEED = 14.0       # Cap for horizontal speed after rallies
BALL_SPEED_INCREMENT = 0.4  # Horizontal speed-up per paddle hit
MAX_DEFLECTION = 6.0        # Max vertical speed from paddle hit offset
SERVE_DELAY_FRAMES = 45     # Pause after each point before the serve
# --- Scoring -------------------------------------------------------------
WINNING_SCORE = 5           # First player to reach this wins the match
# --- Fonts ---------------------------------------------------------------
FONT_NAME = None            # None -> pygame's built-in default font
SCORE_FONT_SIZE = 48
LABEL_FONT_SIZE = 22
MESSAGE_FONT_SIZE = 30