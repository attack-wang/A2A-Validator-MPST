'''
settings.py
Central configuration for the Space Invaders game.
All tunable constants (screen size, speeds, fleet layout, scoring, colors)
live here so gameplay can be balanced without touching game logic.
'''
class Settings:
    def __init__(self):
        # Screen
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (10, 10, 30)
        self.caption = "Space Invaders"
        # Player
        self.player_speed = 5.0
        self.player_width = 40
        self.player_height = 24
        self.player_lives = 3
        self.player_fire_cooldown = 350  # ms between shots
        self.player_invulnerable_ms = 1500  # respawn invulnerability window
        self.player_bottom_margin = 20  # distance of ship from screen bottom
        # Player bullets
        self.bullet_speed = 8.0
        self.bullet_width = 4
        self.bullet_height = 14
        self.bullet_color = (255, 255, 80)
        self.max_player_bullets = 3
        # Alien bombs
        self.bomb_speed = 4.0
        self.bomb_width = 4
        self.bomb_height = 12
        self.bomb_color = (255, 80, 80)
        self.bomb_chance = 0.015  # chance per frame that a bomb is dropped
        self.bomb_min_interval = 800  # ms minimum between bombs
        # Aliens / fleet
        self.alien_rows = 5
        self.alien_cols = 8
        self.alien_width = 36
        self.alien_height = 24
        self.alien_x_spacing = 60
        self.alien_y_spacing = 50
        self.fleet_top_margin = 80
        self.fleet_side_margin = 40
        self.fleet_speed = 1.0
        self.fleet_speed_increment = 0.3  # extra speed per wave
        self.fleet_drop_distance = 24
        self.alien_points = [30, 20, 20, 10, 10]  # points per row from top
        # HUD / colors
        self.hud_color = (230, 230, 230)
        self.font_size = 24
        self.big_font_size = 48
        self.star_count = 120