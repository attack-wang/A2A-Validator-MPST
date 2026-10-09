'''
ui.py
Rendering layer...
'''
import math
import pygame
from settings import (
    CELL_SIZE, HUD_HEIGHT, BOARD_MARGIN, FOOTER_HEIGHT, MAX_TIMER,
    COLOR_BACKGROUND, COLOR_COVERED, COLOR_COVERED_LIGHT, COLOR_COVERED_DARK,
    COLOR_UNCOVERED, COLOR_UNCOVERED_BORDER, COLOR_HUD,
    COLOR_BLACK, COLOR_WHITE, COLOR_RED,
    COLOR_LED_BG, COLOR_LED_DIGIT, COLOR_FLAG_POLE, COLOR_FLAG_BANNER,
    COLOR_MINE, COLOR_EXPLODED_BG, COLOR_WRONG_FLAG_X,
    COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT, COLOR_TITLE,
    NUMBER_COLORS,
)
class Button:
    '''Clickable menu button.'''
    def __init__(self, rect, label, difficulty_name):
        self.rect = rect
        self.label = label
        self.difficulty_name = difficulty_name
    def draw(self, surface, font, hovered):
        color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 2)
        text = font.render(self.label, True, COLOR_TEXT)
        surface.blit(text, text.get_rect(center=self.rect.center))
class Renderer:
    def __init__(self):
        pygame.font.init()
        self.cell_font = pygame.font.SysFont("arial", 20, bold=True)
        self.hud_font = pygame.font.SysFont("consolas", 30, bold=True)
        self.menu_font = pygame.font.SysFont("arial", 24, bold=True)
        self.title_font = pygame.font.SysFont("arial", 44, bold=True)
        self.footer_font = pygame.font.SysFont("arial", 15)
    # ----- top-level screens -----
    def draw_menu(self, surface, buttons, hovered_name=None):
        surface.fill(COLOR_BACKGROUND)
        title = self.title_font.render("MINESWEEPER", True, COLOR_TITLE)
        surface.blit(title, title.get_rect(centerx=surface.get_rect().centerx, y=70))
        subtitle = self.menu_font.render("Select a difficulty", True, COLOR_TEXT)
        surface.blit(subtitle, subtitle.get_rect(centerx=surface.get_rect().centerx, y=130))
        for btn in buttons:
            btn.draw(surface, self.menu_font, btn.difficulty_name == hovered_name)
        hint = self.footer_font.render("Click a button or press 1 / 2 / 3. Esc quits.", True, COLOR_TEXT)
        surface.blit(hint, hint.get_rect(centerx=surface.get_rect().centerx, bottom=surface.get_rect().bottom - 16))
    def draw_game(self, surface, board, board_rect, hud_rect, face_rect,
                  mines_left, seconds, face_state, hover_cell=None,
                  mouse_down=False, face_pressed=False):
        surface.fill(COLOR_BACKGROUND)
        self.draw_hud(surface, hud_rect, mines_left, seconds, face_state, face_rect, face_pressed)
        self.draw_board(surface, board, board_rect, hover_cell, mouse_down)
        self.draw_footer(surface, ...)