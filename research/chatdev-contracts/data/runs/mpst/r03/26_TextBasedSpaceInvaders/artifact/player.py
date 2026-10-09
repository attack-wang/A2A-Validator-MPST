'''
player.py
---------
The player's ship: horizontal movement, shooting with a cooldown and
a short respawn invulnerability used after losing a life.
'''
import settings
class Player:
    '''Ship controlled by the player on a fixed row near the bottom.'''
    def __init__(self):
        '''Create the ship centred at the bottom of the play field.'''
        self.x = settings.PLAYER_START_X
        self.row = settings.PLAYER_ROW
        self.cooldown = 0
        self.invincible = 0   # ticks of invulnerability after respawn
    def update(self, keys):
        '''Apply held movement keys and tick down cooldown/invincibility.'''
        if keys.get('left'):
            self.x -= settings.PLAYER_SPEED
        if keys.get('right'):
            self.x += settings.PLAYER_SPEED
        self.x = max(0, min(settings.GRID_WIDTH - 1, self.x))
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1
    def shoot(self):
        '''Return a new bullet fired from the ship, or None during cooldown.'''
        if self.cooldown == 0:
            self.cooldown = settings.PLAYER_COOLDOWN
            return Bullet(self.x, self.row - 1, -settings.PLAYER_BULLET_SPEED)
        return None