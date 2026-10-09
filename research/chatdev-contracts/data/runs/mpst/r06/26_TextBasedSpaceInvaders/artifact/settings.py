'''
Configuration constants for the Space Invaders game.
Centralises every tunable value (screen size, speeds, fleet layout,
scoring, lives) so gameplay can be adjusted from a single place.
'''
class Settings:
    '''Holds all game configuration values used across every module.'''
    def __init__(self):
        # --- Screen / window ------------------------------------------------
        self.screen_width = 800
        self.screen_height = 600
        self.fps = 60
        self.caption = 'Space Invaders'
        self.background_color = (10, 10, 30)
        # --- Ship -----------------------------------------------------------
        self.ship_width = 50
        self.ship_height = 30
        self.ship_speed = 6.0          # pixels per frame
        self.ship_color = (0, 200, 255)
        self.fire_cooldown_ms = 350    # minimum delay between shots
        self.max_player_bullets = 5    # bullets allowed on screen at once
        # --- Bullets ----------------------------------------------------------
        self.bullet_width = 4
        self.bullet_height = 14
        self.player_bullet_speed = 9.0
        self.player_bullet_color = (255, 230, 0)
        self.alien_bullet_speed = 5.0
        self.alien_bullet_color = (255, 70, 70)
        self.alien_fire_interval_ms = 900
        # --- Alien fleet ------------------------------------------------------
        self.alien_rows = 4
        self.alien_columns = 8
        self.alien_width = 40
        self.alien_height = 24
        self.alien_x_spacing = 55
        self.alien_y_spacing = 45
        self.fleet_top_margin = 70
        self.fleet_side_margin = 45
        self.alien_speed = 1.5         # horizontal pixels per frame
        self.fleet_drop_distance = 20  # downward step on edge bounce
        self.row_colors = [
            (170, 90, 255),   # top row
            (255, 120, 60),
            (80, 220, 120),
            (90, 200, 255),
        ]
        self.row_points = [30, 20, 15, 10]  # score value per row (top first)
        # --- Rules ------------------------------------------------------------
        self.starting_lives = 3
        self.invulnerability_ms = 1500  # grace period after being hit