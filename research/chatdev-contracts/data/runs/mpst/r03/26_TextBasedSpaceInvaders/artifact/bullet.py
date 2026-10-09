'''
bullet.py
---------
Bullet entity shared by the player (shots travelling upward) and the
alien fleet (bombs travelling downward). A bullet is a single character
that moves vertically each tick and destroys itself once it leaves the
play field.
'''
import settings
class Bullet:
    '''A vertical projectile. Positive speed moves down, negative moves up.'''
    def __init__(self, x, y, speed):
        '''Spawn a bullet at column `x`, row `y`, moving `speed` cells/tick.'''
        self.x = x
        self.y = y
        self.speed = speed
    @property
    def char(self):
        '''Character used to render this bullet on the play field.'''
        return (settings.CHAR_ALIEN_BULLET if self.speed > 0
                else settings.CHAR_PLAYER_BULLET)
    def update(self):
        '''Move the bullet one step; return False when it is off-screen.'''
        self.y += self.speed
        return 0 <= self.y < settings.GRID_HEIGHT
    def alive(self):
        '''True while the bullet is still inside the play field.'''
        return 0 <= self.y < settings.GRID_HEIGHT