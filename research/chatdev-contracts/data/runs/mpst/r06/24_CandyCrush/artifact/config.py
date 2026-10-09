'''Configuration constants for the Candy Crush-style match-3 game.'''
# Window
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 640
FPS = 60
TITLE = "Candy Crush Deluxe - ChatDev Edition"
# Board
ROWS = 8
COLS = 8
NUM_CANDY_TYPES = 6
CELL_SIZE = 64
BOARD_MARGIN = 16
BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE
BOARD_X = BOARD_MARGIN
BOARD_Y = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2  # maybe align differently
# Sidebar
SIDEBAR_X = BOARD_X + BOARD_WIDTH + BOARD_MARGIN
SIDEBAR_WIDTH = WINDOW_WIDTH - SIDEBAR_X - BOARD_MARGIN
Hmm, let me compute: BOARD_WIDTH = 8*64 = 512. BOARD_MARGIN=16. SIDEBAR_X = 16+512+16 = 544. SIDEBAR_WIDTH = 720-544-16 = 160. That's a bit narrow but workable. Maybe make window 760 wide: SIDEBAR_X = 544, SIDEBAR_WIDTH = 200. Let's do WINDOW_WIDTH = 760, WINDOW_HEIGHT = 560? BOARD_HEIGHT = 512, plus margins top/bottom 24 each → 560. OK: WINDOW_HEIGHT = 560, BOARD_Y = 24. WINDOW_WIDTH = 760.
Actually let me make it a bit bigger: CELL_SIZE = 60, ROWS=COLS=8 → board 480x480. WINDOW: width = 24 + 480 + 20 + 200 + 24 = 748 → round to 760. Height = 24+480+24 = 528 → 540. Fine.
Let me define:
- CELL_SIZE = 60
- BOARD_X = 24, BOARD_Y = 24
- BOARD_WIDTH = COLS*CELL_SIZE = 480
- BOARD_HEIGHT = 480
- SIDEBAR_X = BOARD_X + BOARD_WIDTH + 20 = 524
- SIDEBAR_WIDTH = WINDOW_WIDTH - SIDEBAR_X - 24 = 760-524-24 = 212
- WINDOW_HEIGHT = BOARD_Y + BOARD_HEIGHT + 24 = 528 → use 540 for a little breathing room? Let's set WINDOW_HEIGHT = 528. Hmm, game over overlay needs space; it's an overlay so fine. I'll use 540.
Colors:
- BACKGROUND = (30, 30, 46) dark
- BOARD_BG = (49, 50, 68)
- CELL_A = (69, 71, 90), CELL_B = (60, 62, 80)
- TEXT = (205, 214, 244)
- ACCENT = (137, 180, 250)
- Candy colors (6): red (244, 90, 102), orange (250, 165, 60), yellow (250, 220, 80), green (80, 200, 120), blue (80, 150, 250), purple (180, 100, 250)
- Candy names for fun: "Ruby", "Orange", "Lemon", "Emerald", "Sapphire", "Amethyst"
Scoring:
- BASE_MATCH_SCORE = 50 per candy? Common: 3-match = 60 (20 per candy?), let's do: score = candies_cleared * 30 * cascade_multiplier. Or base 50 for 3, +20 per extra candy, times cascade. I'll do: points = (30 * n_cleared + 20 * (n_cleared - 3)) * cascade_level. Simpler: points = n_cleared * 30 * cascade_level. Keep SCORE_PER_CANDY = 30.
Game constraints:
- STARTING_MOVES = 30
- TIME_LIMIT = 180 seconds (3 min). Both moves and time tracked; game ends when either runs out. Actually having both might be confusing; the task says "possibly track moves or time-based constraints". I'll track moves as primary and also show elapsed time. Hmm, or make it configurable: GAME_MODE with moves. Let me track both: moves limit 30 AND time limit 180s; whichever first ends the game. That satisfies "track moves or time-based constraints" — we do both. I'll display both.
Animation timings:
- SWAP_DURATION = 0.18 s
- POP_DURATION = 0.22 s
- FALL_SPEED = pixels per second, e.g., 900 px/s² with acceleration? Simpler: constant speed 1200 px/s, or gravity accel. I'll use constant speed per candy: candy.fall_speed = 1000 px/s. Actually nicer: accelerate. Keep simple: speed 900 px/s constant.
- CASCADE_DELAY = 0.05 s between cascades maybe.
**candy.py**: