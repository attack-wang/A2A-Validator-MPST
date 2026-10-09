'''
Global configuration constants for the two-player Pong game.
Centralizes every tunable value (window size, colors, speeds, scoring rules)
so gameplay can be adjusted from a single file.
'''
# ---------------------------------------------------------------------------
# Window / timing
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 800          # Playable window width in pixels
SCREEN_HEIGHT = 600         # Playable window height in pixels
FPS = 60                    # Target frames per second
CAPTION = "Pong - Two Player"
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (60, 200, 90)
GRAY = (70, 70, 70)
# ---------------------------------------------------------------------------
# Paddle
# ---------------------------------------------------------------------------
PADDLE_WIDTH = 12           # Paddle thickness (horizontal size)
PADDLE_HEIGHT = 90          # Paddle length (vertical size)
PADDLE_SPEED = 7            # Pixels moved per frame when a key is held
PADDLE_MARGIN = 20          # Distance of each paddle from its side wall
# ---------------------------------------------------------------------------
# Ball
# ---------------------------------------------------------------------------
BALL_SIZE = 14                       # Ball is a square of this side length
BALL_INITIAL_SPEED_X = 5.0           # Horizontal speed at serve (px/frame)
BALL_INITIAL_SPEED_Y = 4.0           # Vertical speed magnitude at serve
BALL_SPEED_INCREMENT = 0.5           # Speed gained on every paddle hit
BALL_MAX_SPEED = 12.0                # Horizontal speed cap
# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
WINNING_SCORE = 5           # First player to reach this score wins
# ---------------------------------------------------------------------------
# Fonts (None -> pygame's default bundled font)
# ---------------------------------------------------------------------------
FONT_NAME = None
SCORE_FONT_SIZE = 60        # Big digits for the score
MESSAGE_FONT_SIZE = 34      # Winner / hint messages
HINT_FONT_SIZE = 20         # Small on-screen control hints