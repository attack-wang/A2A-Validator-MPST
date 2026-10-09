'''
alienfleet.py
The grid of aliens: creation, side-to-side marching with drops on edge,
bottom detection, and bomb spawning from the lowest alien of a column.
'''
import random
from alien import Alien
class AlienFleet:
    """Manages all aliens as a group that marches and descends."""
    def __init__(self, settings, wave=1):
        self.settings = settings
        self.wave = wave
        self.speed = settings.fleet_speed + (wave - 1) * settings.fleet_speed_increment
        self.direction = 1  # 1 = moving right, -1 = moving left
        self.aliens = []
        self._create_fleet()
    def _create_fleet(self):
        """Fill the grid with aliens row by row."""
        for row in range(self.settings.alien_rows):
            for col in range(self.settings.alien_cols):
                self.aliens.append(Alien(self.settings, row, col))
    def update(self):
        """March the fleet one step; drop down and reverse at screen edges.
        Returns True if the fleet dropped closer to the player this step.
        """
        dx = int(self.speed) * self.direction
        dy = 0
        if self._at_edge():
            self.direction *= -1
            dx = 0
            dy = self.settings.fleet_drop_distance
        for alien in self.aliens:
            alien.update(dx, dy)
        return dy > 0