'''
game.py
Main application class...
'''
import time
import pygame
from settings import (
    CELL_SIZE, HUD_HEIGHT, BOARD_MARGIN, FPS, MAX_TIMER,
    COLOR_BACKGROUND, DIFFICULTIES, DIFFICULTY_ORDER,
)
from board import Board
from ui import Renderer, Button
class Game:
    def __init__(self):
        pygame.init()
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.board = None
        self.difficulty = None
        self.start_time = None
        self.elapsed = 0
        self.hover_cell = None
        self.mouse_down = False
        self.face_pressed = False
        self.screen = None
        self.board_rect = None
        self.hud_rect = None
        self.face_rect = None
        self.menu_buttons = []
        self._build_menu_window()
        self._build_menu_buttons()
    def _build_menu_window(self):
        self.screen = pygame.display.set_mode((560, 480))
        pygame.display.set_caption("Minesweeper")
    def _build_menu_buttons(self):
        self.menu_buttons = []
        btn_w, btn_h, gap = 300, 56, 26
        cx = self.screen.get_rect().centerx
        start_y = 190
        for i, name in enumerate(DIFFICULTY_ORDER):
            cols, rows, mines = DIFFICULTIES[name]
            label = f"{name}  ({cols} x {rows}, {mines} mines)"
            rect = pygame.Rect(0, 0, btn_w, btn_h)
            rect.centerx = cx
            rect.y = start_y + i * (btn_h + gap)
            self.menu_buttons.append(Button(rect, label, name))
    def _setup_playing_window(self):
        cols, rows, mines = DIFFICULTIES[self.difficulty]
        width = cols * CELL_SIZE + 2 * BOARD_MARGIN
        height = HUD_HEIGHT + rows * CELL_SIZE + 3 * BOARD_MARGIN
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Minesweeper - {self.difficulty}")
        self.hud_rect = pygame.Rect(BOARD_MARGIN, BOARD_MARGIN,
                                    width - 2 * BOARD_MARGIN, HUD_HEIGHT)
        self.board_rect = pygame.Rect(BOARD_MARGIN, HUD_HEIGHT + 2 * BOARD_MARGIN,
                                      cols * CELL_SIZE, rows * CELL_SIZE)
        self.face_rect = pygame.Rect(0, 0, 48, 48)
        self.face_rect.center = self.hud_rect.center
    def start(self, difficulty_name):
        self.difficulty = difficulty_name
        cols, rows, mines = DIFFICULTIES[difficulty_name]
        self.board = Board(rows, cols, mines)
        self._setup_playing_window()
        self.state = "playing"
        self.start_time = None
        self.elapsed = 0
        self.hover_cell = None
        self.mouse_down = False
        self.face_pressed = False
    def restart(self):
        if self.difficulty is not None:
            self.start(self.difficulty)
    def to_menu(self):
        self.state = "menu"
        self.board = None
        self.difficulty = None
        self.start_time = None
        self.elapsed = 0
        self._build_menu_window()
        self._build_menu_buttons()
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()
    def handle_event(self, event):
        if self.state == "menu":
            self._handle_menu_event(event)
        else:
            self._handle_playing_event(event)
    def _handle_menu_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            pass  # hover handled in render via mouse pos
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.menu_buttons:
                if btn.rect.collidepoint(event.pos):
                    self.start(btn.difficulty_name)
                    break
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE,):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.key == pygame.K_1:
                self.start(DIFFICULTY_ORDER[0])
            elif event.key == pygame.K_2:
                self.start(DIFFICULTY_ORDER[1])
            elif event.key == pygame.K_3:
                self.start(DIFFICULTY_ORDER[2])
    def _handle_playing_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover_cell = self.cell_at(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.face_rect.collidepoint(event.pos):
                    self.face_pressed = True
                else:
                    self.mouse_down = True
            elif event.button == 3:
                # right click: flag
                cell_pos = self.cell_at(event.pos)
                if cell_pos is not None and not self.board.game_over:
                    self.board.toggle_flag(*cell_pos)
                    if self.start_time is None:
                        # flagging doesn't start the timer in classic; keep None
                        pass
            elif event.button == 2:
                # middle click: chord
                cell_pos = self.cell_at(event.pos)
                if cell_pos is not None:
                    self.board.chord(*cell_pos)
                    self._ensure_timer_started()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.face_pressed and self.face_rect.collidepoint(event.pos):
                    self.restart()
                self.face_pressed = False
                self.mouse_down = False
                if not self.board.game_over:
                    cell_pos = self.cell_at(event.pos)
                    if cell_pos is not None:
                        outcome = self.board.reveal(*cell_pos)
                        if outcome in ("revealed", "mine"):
                            self._ensure_timer_started()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.to_menu()
            elif event.key == pygame.K_r:
                self.restart()
            elif event.key == pygame.K_f:
                # flag at hover
                if self.hover_cell is not None and not self.board.game_over:
                    self.board.toggle_flag(*self.hover_cell)