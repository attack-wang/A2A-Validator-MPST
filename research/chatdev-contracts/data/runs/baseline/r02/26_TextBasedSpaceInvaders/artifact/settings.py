'''
settings.py — central configuration for the Space Invaders game.
Stores all tunable constants: screen size, colors, speeds, fleet layout,
bullet properties, lives and scoring rules in one place.
'''
class Settings:
    '''Hold every tunable value used across the game.'''
    def __init__(self):
        '''Initialize all game settings.'''
        # --- Screen ---
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (10, 10, 30)
        self.caption = "Space Invaders"
        # --- Timing ---
        self.fps = 60
        # --- Ship ---
        self.ship_speed = 4.5          # pixels per frame
        self.ship_limit = 3            # number of lives
        # --- Player bullets ---
        self.bullet_width = 4
        self.bullet_height = 14
        self.bullet_color = (255, 230, 90)
        self.bullet_speed = 8.0
        self.bullets_allowed = 3
        # --- Alien bullets ---
        self.alien_bullet_width = 4
        self.alien_bullet_height = 12
        self.alien_bullet_color = (255, 80, 80)
        self.alien_bullet_speed = 3.5
        # --- Fleet ---
        self.alien_rows = 4
        self.alien_cols = 9
        self.alien_speed = 0.6
        self.fleet_drop_speed = 25
        self.fleet_direction = 1       # 1 = right, -1 = left
        self.alien_fire_chance = 0.02  # per-frame chance a random alien fires
        # --- Scoring ---
        # Points per alien, indexed by row (0 = top row, worth the most).
        self.alien_points_by_row = [50, 40, 30, 20]
    def points_for_row(self, row):
        '''Return the score value of an alien in the given row (0 = top row).'''
        if row < len(self.alien_points_by_row):
            return self.alien_points_by_row[row]
        return self.alien_points_by_row[-1]