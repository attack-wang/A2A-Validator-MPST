'''
alien.py
--------
Individual alien entity plus the AlienFleet container that moves the
whole formation as a single unit, reverses direction at the play-field
edges, descends when an edge is reached and drops bombs at random.
'''
import random
import settings
from bullet import Bullet
class Alien:
    '''One alien in the invasion fleet.'''
    def __init__(self, x, y, row):
        '''Place the alien at column `x`, row `y`; `row` sets its score value.'''
        self.x = x
        self.y = y
        self.row = row
        self.dead = False
    def value(self):
        '''Points awarded for destroying this alien (top rows worth more).'''
        return settings.ALIEN_SCORES.get(self.row, 10)
class AlienFleet:
    '''Moves and manages the formation of aliens as a single unit.'''
    def __init__(self, wave=1):
        '''Build the fleet; higher waves step and shoot more aggressively.'''
        self.wave = wave
        self.aliens = []
        self.direction = 1
        self.move_interval = max(1, settings.FLEET_MOVE_EVERY - (wave - 1))
        self.fire_chance = min(0.5, settings.ALIEN_FIRE_CHANCE
                               * (1 + settings.FIRE_CHANCE_PER_WAVE * (wave - 1)))
        self.tick_counter = 0
        self.build()
    def build(self):
        '''Create the rectangular grid of aliens.'''
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLS):
                x = settings.FLEET_LEFT_MARGIN + col * settings.FLEET_H_SPACING
                y = settings.FLEET_TOP_MARGIN + row * settings.FLEET_V_SPACING
                self.aliens.append(Alien(x, y, row))
    def alive_aliens(self):
        '''List of aliens that have not been destroyed yet.'''
        return [a for a in self.aliens if not a.dead]
    def update(self):
        '''Advance fleet timers; step the formation on its scheduled ticks.'''
        self.tick_counter += 1
        if self.tick_counter >= self.move_interval:
            self.tick_counter = 0
            self._step()
    def _step(self):
        '''Move one cell sideways; reverse and descend when an edge is hit.'''
        alive = self.alive_aliens()
        if not alive:
            return
        edge_hit = False
        for alien in alive:
            alien.x += self.direction
            if alien.x <= 0 or alien.x >= settings.GRID_WIDTH - 1:
                edge_hit = True
        if edge_hit:
            self.direction *= -1
            for alien in alive:
                alien.x -= self.direction  # undo the step that went out of bounds
                alien.y += settings.FLEET_DROP_DISTANCE