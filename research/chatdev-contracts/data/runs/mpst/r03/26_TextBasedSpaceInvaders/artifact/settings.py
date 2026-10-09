'''
settings.py
-----------
Central configuration module for the text-based Space Invaders game.
Every tunable value lives here: grid dimensions, tick rate, display
characters, player and bullet behaviour, alien fleet layout, lives,
scoring and wave settings. Balancing the game never requires touching
the gameplay code -- only this file.
The game uses only the Python standard library (no pygame), so it runs
in any terminal on any platform where Python is available.
'''
# ------------------------------------------------------------------
# Grid / timing
# ------------------------------------------------------------------
GRID_WIDTH = 60            # playable columns of the play field
GRID_HEIGHT = 20           # playable rows of the play field
TICK_SECONDS = 0.08        # real seconds per game tick (~12.5 updates/s)
CAPTION = "TEXT SPACE INVADERS"
# ------------------------------------------------------------------
# Display characters
# ------------------------------------------------------------------
CHAR_EMPTY = ' '
CHAR_ALIEN = 'W'
CHAR_PLAYER = 'A'
CHAR_PLAYER_BULLET = '|'
CHAR_ALIEN_BULLET = '*'
CHAR_SHIELD = '='          # decorative ground line under the player
# ------------------------------------------------------------------
# Player ship
# ------------------------------------------------------------------
PLAYER_START_X = GRID_WIDTH // 2   # spawn / respawn column
PLAYER_ROW = GRID_HEIGHT - 2       # row the ship always sits on
PLAYER_SPEED = 2                   # cells moved per tick while a key is held
PLAYER_COOLDOWN = 3                # ticks that must pass between shots
PLAYER_RESPAWN_INVINCIBILITY = 15  # ticks of grace after losing a life
# ------------------------------------------------------------------
# Bullets
# ------------------------------------------------------------------
PLAYER_BULLET_SPEED = 1    # cells per tick (travels upward)
ALIEN_BULLET_SPEED = 1     # cells per tick (travels downward)
ALIEN_FIRE_CHANCE = 0.05   # per-tick chance the fleet drops one bomb
MAX_ALIEN_BULLETS = 4      # simultaneous bombs allowed (fairness cap)
# ------------------------------------------------------------------
# Alien fleet
# ------------------------------------------------------------------
ALIEN_ROWS = 4
ALIEN_COLS = 8
FLEET_TOP_MARGIN = 2       # first alien row inside the play field
FLEET_LEFT_MARGIN = 12     # first alien column inside the play field
FLEET_H_SPACING = 5        # columns between neighbouring aliens
FLEET_V_SPACING = 2        # rows between neighbouring alien rows
FLEET_MOVE_EVERY = 3       # wave 1: fleet steps once every N ticks
FLEET_DROP_DISTANCE = 1    # rows the fleet descends when an edge is hit
FIRE_CHANCE_PER_WAVE = 0.5 # fire chance multiplier added per wave
# ------------------------------------------------------------------
# Lives / scoring / waves
# ------------------------------------------------------------------
STARTING_LIVES = 3
TOTAL_WAVES = 3
ALIEN_SCORES = {0: 30, 1: 20, 2: 20, 3: 10}   # points per row (top rows worth more)
BOTTOM_LIMIT = GRID_HEIGHT - 4  # aliens reaching this row end the game