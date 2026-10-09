import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
_BTN_W, _BTN_H = 300, 64
_center_x = WINDOW_WIDTH // 2 - _BTN_W // 2
MENU_BUTTONS = {
    "moves": pygame.Rect(_center_x, 330, _BTN_W, _BTN_H),
    "timed": pygame.Rect(_center_x, 430, _BTN_W, _BTN_H),
}