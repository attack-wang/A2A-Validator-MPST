# settings.py
'''
settings.py
Central configuration for the Flappy Bird clone (tkinter edition).
All tunable constants (window, physics, difficulty, colors) live here.
'''
# --- Window ---
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60
FRAME_MS = max(1, int(1000 / FPS))
TITLE = "Flappy Bird - ChatDev Edition"
# --- Ground ---
GROUND_HEIGHT = 80
GROUND_TILE = 24
# --- Bird physics (units per second) ---
GRAVITY = 1400.0
FLAP_VELOCITY = -420.0
MAX_FALL_SPEED = 700.0
BIRD_RADIUS = 14
# --- Pipes ---
PIPE_WIDTH = 60
BASE_PIPE_SPEED = 160.0
MAX_PIPE_SPEED = 320.0
SPEED_GAIN_PER_POINT = 4.0
BASE_GAP_SIZE = 170
MIN_GAP_SIZE = 110
GAP_SHRINK_PER_POINT = 2.0
GAP_RANDOMNESS = 30
PIPE_SPAWN_DISTANCE = 230
# --- Colors ---
SKY_TOP = "#70c5ce"
SKY_BOTTOM = "#c4e7e5"
BIRD_COLOR = "#ffcc00"
BIRD_WING = "#ff9933"
BIRD_BEAK = "#ff5722"
BIRD_BELLY = "#ffeca0"
PIPE_BODY = "#4caf50"
PIPE_EDGE = "#2e7d32"
PIPE_HIGHLIGHT = "#81c784"
GROUND_COLOR = "#deb887"
GROUND_DARK = "#cdaa7d"
GRASS_COLOR = "#65c154"
TEXT_COLOR = "#ffffff"
TEXT_SHADOW = "#000000"
GAME_OVER_COLOR = "#e74c3c"