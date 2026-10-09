'''
settings.py
Central configuration for the Tetris game.
Contains all tunable constants: board dimensions, window layout, colours,
the seven tetromino shape definitions, scoring rules, level/speed
progression and control timing. Keeping every constant in one place makes
the game easy to tweak without touching game logic.
'''
# ---------------------------------------------------------------------------
# Board & window layout
# ---------------------------------------------------------------------------
CELL_SIZE = 30          # Pixel size of one board cell
COLS = 10               # Playfield width  (standard Tetris)
ROWS = 20               # Playfield height (standard Tetris)
SIDEBAR_WIDTH = 230     # Width of the info panel on the right
PADDING = 12            # Outer margin around the playfield
WINDOW_WIDTH = COLS * CELL_SIZE + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = ROWS * CELL_SIZE + PADDING * 2
# ---------------------------------------------------------------------------
# Colours (R, G, B)
# ---------------------------------------------------------------------------
BLACK = (17, 17, 17)        # Window / playfield background
GRID_LINE = (45, 45, 45)    # Playfield grid lines
WHITE = (235, 235, 235)     # Primary text
GRAY = (130, 130, 130)      # Secondary text
PANEL_BG = (28, 28, 40)     # Sidebar background
OVERLAY_BG = (0, 0, 0)      # Pause / game-over overlay base
GHOST_COLOR = (200, 200, 200)  # Ghost piece outline
# ---------------------------------------------------------------------------
# The seven standard tetromino shapes (1 = filled cell)
# ---------------------------------------------------------------------------
SHAPES = {
    'I': [[0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'S': [[0, 1, 1],
          [1, 1, 0],
          [0, 0, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]],
    'J': [[1, 0, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'L': [[0, 0, 1],
          [1, 1, 1],
          [0, 0, 0]],
}
# One distinct colour per shape, keyed like SHAPES
TETROMINO_COLORS = {
    'I': (0, 200, 220),    # cyan
    'O': (225, 195, 0),    # yellow
    'T': (170, 0, 220),    # purple
    'S': (0, 200, 70),     # green
    'Z': (225, 55, 55),    # red
    'J': (45, 75, 225),    # blue
    'L': (235, 145, 10),   # orange
}
# ---------------------------------------------------------------------------
# Timing & difficulty progression
# ---------------------------------------------------------------------------
FPS = 60
FALL_INTERVAL_START = 900   # ms per automatic drop at level 1
FALL_INTERVAL_MIN = 120     # fastest possible drop interval
FALL_INTERVAL_STEP = 70     # interval reduction per level
LINES_PER_LEVEL = 10        # lines cleared to reach the next level
LINE_SCORES = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_SCORE = 1         # points per cell dropped manually
HARD_DROP_SCORE = 2         # points per cell dropped instantly
# ---------------------------------------------------------------------------
# Control timing (held-key auto repeat, DAS style)
# ---------------------------------------------------------------------------
MOVE_REPEAT_DELAY = 180     # ms before a held key starts repeating
MOVE_REPEAT_INTERVAL = 55   # ms between repeats of a held key