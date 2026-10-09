class Settings:
    # Screen
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    TITLE = "Space Invaders"
    # Colors
    BG_COLOR = (10, 10, 30)
    SHIP_COLOR = (0, 200, 255)
    ALIEN_COLORS = [(0, 255, 0), (255, 255, 0), (255, 120, 0), (255, 0, 255), (0, 255, 255)]
    BULLET_COLOR = (255, 255, 255)
    BOMB_COLOR = (255, 60, 60)
    TEXT_COLOR = (240, 240, 240)
    HUD_COLOR = (180, 180, 180)
    # Ship
    SHIP_WIDTH = 48
    SHIP_HEIGHT = 28
    SHIP_SPEED = 320.0
    SHIP_COOLDOWN = 0.35
    SHIP_LIVES = 3
    SHIP_INVINCIBILITY = 1.5
    SHIP_SCALE = 2
    # Player bullet
    BULLET_WIDTH = 4
    BULLET_HEIGHT = 14
    BULLET_SPEED = 520.0
    MAX_PLAYER_BULLETS = 4
    # Alien bomb
    BOMB_WIDTH = 4
    BOMB_HEIGHT = 12
    BOMB_SPEED = 200.0
    BOMB_CHANCE = 0.6  # expected bombs per second, fleet-wide
    MAX_BOMBS = 6
    # Aliens
    ALIEN_ROWS = 5
    ALIEN_COLUMNS = 8
    ALIEN_WIDTH = 40
    ALIEN_HEIGHT = 24
    ALIEN_SCALE = 2
    ALIEN_HORIZONTAL_SPEED = 40.0
    ALIEN_DROP_DISTANCE = 24
    ALIEN_SPEEDUP_PER_WAVE = 1.15
    ALIEN_ANIM_INTERVAL = 0.5
    FLEET_EDGE_MARGIN = 10
    # Scoring
    ALIEN_BASE_POINTS = 10
    ALIEN_ROW_BONUS = 10