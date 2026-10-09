'''settings.py: central configuration for the Space Invaders game.'''
class Settings:
    def __init__(self):
        # Screen
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (8, 10, 28)
        self.caption = "Space Invaders"
        # Frames per second
        self.fps = 60
        # Ship
        self.ship_speed = 300.0  # px/second
        self.ship_limit = 3
        self.ship_width = 50
        self.ship_height = 34
        self.ship_color = (0, 200, 255)
        self.max_active_bullets = 3
        self.bullet_cooldown = 0.25
        # Player bullets
        self.bullet_speed = 480.0
        self.bullet_width = 4
        self.bullet_height = 14
        self.bullet_color = (80, 255, 120)
        # Alien bombs
        self.bomb_speed = 210.0
        self.bomb_width = 4
        self.bomb_height = 12
        self.bomb_color = (255, 80, 80)
        # Fleet
        self.alien_rows = 5
        self.alien_cols = 8
        self.alien_width = 44
        self.alien_height = 32
        self.fleet_speed = 40.0
        self.fleet_speed_increment = 12.0
        self.fleet_drop_distance = 18
        self.fleet_left_margin = 40
        self.fleet_right_margin = 40
        self.fleet_top_margin = 60
        self.alien_h_spacing = 14
        self.alien_v_spacing = 12
        self.alien_colors = [(80,255,120), (255,200,60), (255,120,220), (120,160,255), (180,120,255)]
        # Scoring
        self.alien_points_top = 50
        self.alien_points_step = 10
        # Bombing
        self.bomb_interval = 0.9
        self.bomb_interval_min = 0.35
        # Effects
        self.explosion_duration = 0.35
        self.flash_duration = 0.25
        self.wave_clear_pause = 1.5