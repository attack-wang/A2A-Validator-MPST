"""Space Invaders — main game module..."""
import sys
import pygame
from settings import Settings
from ship import Ship
from alien import AlienFleet
from bullet import Bullet, Bomb  # Bullet used? We append ship.shoot() which returns Bullet. Import for clarity/type. Bomb not directly used but fine.
from scoreboard import Scoreboard