'''The fleet of aliens: formation movement, descent, and firing.'''
import random
import pygame
from settings import (ALIEN_ROWS, ALIEN_COLUMNS, ALIEN_HORIZONTAL_SPACING,
                      ALIEN_VERTICAL_SPACING, FLEET_TOP_MARGIN,
                      FLEET_SIDE_MARGIN, FLEET_BASE_SPEED, FLEET_DROP_SPEED,
                      FLEET_SPEED_INCREMENT, ALIEN_FIRE_CHANCE, SCREEN_WIDTH,
                      SCREEN_HEIGHT)
from alien import Alien
class AlienFleet:
    '''Manages the grid of aliens as a single moving formation.'''
    def __init__(self):
        self.aliens = pygame.sprite.Group()
        self.direction = 1  # 1 = right, -1 = left
        self.speed = FLEET_BASE_SPEED
        self.drop_pending = False
    def create(self):
        '''Build the rectangular formation of aliens.'''
        self.aliens.empty()
        self.direction = 1
        self.speed = FLEET_BASE_SPEED
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLUMNS):
                x = FLEET_SIDE_MARGIN + col * ALIEN_HORIZONTAL_SPACING
                y = FLEET_TOP_MARGIN + row * ALIEN_VERTICAL_SPACING
                self.aliens.add(Alien(x, y, row))
    def update(self):
        '''Move the formation; drop down and reverse at screen edges.'''
        if not self.aliens:
            return
        self.drop_pending = False
        # Determine whether any alien would cross an edge this frame
        for alien in self.aliens:
            new_left = alien.rect.left + self.direction * self.speed
            new_right = alien.rect.right + self.direction * self.speed
            if new_left <= 0 or new_right >= SCREEN_WIDTH:
                self.drop_pending = True
                break
        if self.drop_pending:
            self.direction *= -1
            for alien in self.aliens:
                alien.rect.y += FLEET_DROP_SPEED
        else:
            for alien in self.aliens:
                alien.rect.x += self.direction * self.speed
    def speed_up(self):
        '''Make the fleet faster after an alien is destroyed.'''
        self.speed += FLEET_SPEED_INCREMENT
    def fire(self):
        '''Randomly have a bottom-most alien drop a bullet.
        Returns the (x, y) launch position or None.
        '''
        if not self.aliens or random.random() > ALIEN_FIRE_CHANCE:
            return None
        # Pick a random column, find the lowest alien in it
        columns = {}
        for alien in self.aliens:
            col_key = alien.rect.centerx
            # group by approximate column using centerx
            ...