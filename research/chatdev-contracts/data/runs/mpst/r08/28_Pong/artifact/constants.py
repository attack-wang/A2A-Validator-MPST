'''
constants.py
Global configuration constants shared by all game modules:
window setup, entity dimensions, physics tuning, gameplay rules,
and the color palette.
'''
# Window / display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
FPS = 60
WINDOW_TITLE = "Two-Player Pong"
# Court / entities
PADDLE_MARGIN = 20          # Distance of each paddle from the side edges
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
PADDLE_SPEED = 6            # Pixels the paddle moves per frame
BALL_SIZE = 12
BALL_SPEED_X = 5            # Initial horizontal ball speed (px/frame)
BALL_SPEED_Y = 4            # Max vertical speed component used when serving
BALL_SPEEDUP = 0.35         # Speed gained by the ball on every paddle hit
MAX_BALL_SPEED = 12         # Upper bound for total ball speed
MAX_BOUNCE_ANGLE = 60       # Max deflection angle (degrees) off a paddle
# Gameplay
WINNING_SCORE = 5           # First player to reach this score wins
SERVE_DELAY_FRAMES = 45     # Frames to wait before/after each serve (~0.75s)
# Colors (R, G, B)
BLACK = (10, 10, 20)
WHITE = (240, 240, 240)
GRAY = (120, 120, 130)
ACCENT = (80, 200, 255)     # Player 1 (left) color
ACCENT2 = (255, 120, 90)    # Player 2 (right) color