"""Game: pygame main loop, input handling, cascade state machine, scoring, UI."""
import sys
import pygame
from settings import (WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
                      BOARD_X, BOARD_Y, BOARD_PIXELS, CELL_SIZE,
                      PANEL_X, PANEL_WIDTH,
                      STARTING_MOVES, BASE_MATCH_SCORE, SCORE_PER_EXTRA_CANDY,
                      COMBO_MULTIPLIER_STEP, SHUFFLE_PENALTY,
                      COLOR_BG, COLOR_PANEL, COLOR_TEXT, COLOR_SELECTED)
from board import Board
class Game:
    """Owns the window, input, game state machine and rendering."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 26)
        self.big_font = pygame.font.SysFont(None, 44, bold=True)
        self.board = Board()
        self.score = 0
        self.moves_left = STARTING_MOVES
        self.combo = 0
        self.shuffle_count = 0
        # states: playing | resolving | resolving_back | game_over
        self.state = "playing"
        self.selected = None
        self.press_cell = None
        self.pending_swap = None  # (x1, y1, x2, y2, created_match)
    # ------------------------------------------------------------ main loop
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self.update(dt)
            self._draw()
            pygame.display.flip()
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_mousedown(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.on_mouseup(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._restart()
    # ---------------------------------------------------------------- input
    def on_mousedown(self, pos):
        if self.state != "playing":
            return
        cell = self.board.grid_from_pixel(*pos)
        if cell is None:
            self.selected = None
            self.press_cell = None
            return
        if (self.selected is not None and self.selected != cell
                and self._are_adjacent(self.selected, cell)):
            self._attempt_swap(self.selected, cell)  # click-click swap
            self.selected = None
            self.press_cell = None
            return
        self.selected = cell
        self.press_cell = cell
    def on_mouseup(self, pos):
        if self.state != "playing" or self.press_cell is None:
            self.press_cell = None
            return
        start = self.press_cell
        self.press_cell = None
        cell = self.board.grid_from_pixel(*pos)
        if cell is not None and cell != start and self._are_adjacent(start, cell):
            self.selected = None
            self._attempt_swap(start, cell)  # drag swap
    @staticmethod
    def _are_adjacent(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
    def _attempt_swap(self, a, b):
        x1, y1 = a
        x2, y2 = b
        created_match = self.board.try_swap(x1, y1, x2, y2)
        if created_match:
            self.moves_left -= 1
            self.combo = 0
        self.pending_swap = (x1, y1, x2, y2, created_match)
        self.state = "resolving"
    # --------------------------------------------------------------- update
    def update(self, dt):
        self.board.update(dt)
        if self.state in ("resolving", "resolving_back") and not self.board.all_animating():
            self._continue_resolution()
    def _continue_resolution(self):
        x1, y1, x2, y2, created_match = self.pending_swap
        if self.state == "resolving_back":
            # swap-back animation finished -> resume play
            self.pending_swap = None
            self.state = "playing"
            return
        if created_match:
            matches = self.board.find_matches()
            if matches:
                self._clear_and_score(matches)
                self.board.apply_gravity()
                self.combo += 1
                return  # wait for falling animation, then cascade again
            # cascade finished
            if self.board.find_valid_move() is None:
                self.board.shuffle()
                self.shuffle_count += 1
                self.score = max(0, self.score - SHUFFLE_PENALTY)
            self.combo = 0
            self.pending_swap = None
            self.state = "playing"
            self._check_end_conditions()
        else:
            # invalid swap: animate candies back, then resume
            self.board.swap_back(x1, y1, x2, y2)
            self.state = "resolving_back"
    def _clear_and_score(self, matches):
        n = len(matches)
        base = BASE_MATCH_SCORE + max(0, n - 3) * SCORE_PER_EXTRA_CANDY
        multiplier = 1.0 + self.combo * COMBO_MULTIPLIER_STEP
        self.score += int(base * multiplier)
        self.board.clear_matches(matches)
    def _check_end_conditions(self):
        if self.moves_left <= 0:
            self.state = "game_over"
    def _restart(self):
        self.board = Board()
        self.score = 0
        self.moves_left = STARTING_MOVES
        self.combo = 0
        self.shuffle_count = 0
        self.selected = None
        self.press_cell = None
        self.pending_swap = None
        self.state = "playing"
    # ----------------------------------------------------------------- draw
    def _draw(self):
        self.screen.fill(COLOR_BG)
        self.board.draw(self.screen)
        self._draw_selection()
        self._draw_panel()
        if self.state == "game_over":
            self._draw_game_over()
    def _draw_selection(self):
        if self.selected is None:
            return
        x, y = self.selected
        rect = pygame.Rect(BOARD_X + x * CELL_SIZE, BOARD_Y + y * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_SELECTED, rect, 3, border_radius=10)
    def _draw_panel(self):
        panel = pygame.Rect(PANEL_X, BOARD_Y, PANEL_WIDTH, BOARD_PIXELS)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel, border_radius=12)
        combo_mult = 1.0 + self.combo * COMBO_MULTIPLIER_STEP
        lines = [
            f"Score: {self.score}",
            f"Moves left: {self.moves_left}",
            f"Combo: x{combo_mult:.1f}",
            f"Shuffles: {self.shuffle_count}",
            "",
            "Click two adjacent",
            "candies or drag to",
            "swap them. Match 3+",
            "to score. R = restart",
        ]
        for i, text in enumerate(lines):
            surf = self.font.render(text, True, COLOR_TEXT)
            self.screen.blit(surf, (PANEL_X + 16, BOARD_Y + 18 + i * 30))
    def _draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        msg = self.big_font.render(
            f"Game Over!  Score: {self.score}  —  press R to restart",
            True, (255, 255, 255))
        rect = msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(msg, rect)