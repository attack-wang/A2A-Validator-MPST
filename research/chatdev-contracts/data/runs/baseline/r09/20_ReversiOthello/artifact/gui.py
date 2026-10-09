'''
gui.py
Pygame graphical interface for Reversi (Othello). Renders the board, discs,
valid-move hints, live score and status messages, handles mouse clicks and
animates disc flips.
'''
import sys
import pygame
from constants import (EMPTY, BLACK, WHITE, BOARD_SIZE, CELL_SIZE,
                       BOARD_PIXEL, BG_COLOR, GRID_LINE_COLOR,
                       BLACK_DISC_COLOR, WHITE_DISC_COLOR, HINT_COLOR,
                       LAST_MOVE_COLOR, FONT_SIZE, SCORE_FONT_SIZE,
                       MESSAGE_FONT_SIZE, PLAYER_NAMES, INFO_PANEL_HEIGHT,
                       WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_CAPTION,
                       FLIP_FRAMES, FPS)
from game_logic import Game
class GameGUI:
    """Main application window: event handling, drawing and flip animations."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_CAPTION)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.score_font = pygame.font.SysFont(None, SCORE_FONT_SIZE)
        self.message_font = pygame.font.SysFont(None, MESSAGE_FONT_SIZE)
        self.game = Game()
        self.animations = []          # active disc-flip animations
        self.running = True
    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #
    def run(self):
        """Standard pygame application loop."""
        while self.running:
            self.clock.tick(FPS)
            self._handle_events()
            self._update_animations()
            self._draw()
        pygame.quit()
        sys.exit(0)
    # ------------------------------------------------------------------ #
    # Event handling
    # ------------------------------------------------------------------ #
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._on_click(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._restart()
    def _on_click(self, pos):
        """Translate a mouse click into a board move (if legal)."""
        x, y = pos
        if y >= BOARD_PIXEL:                       # click on the info panel
            return
        col, row = x // CELL_SIZE, y // CELL_SIZE
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        if self.game.game_over:
            return
        flipped = self.game.try_move(row, col)
        if flipped:
            new_value = self.game.board.grid[row][col]
            self._spawn_flip_animations(flipped, new_value)
    def _restart(self):
        """Start a fresh game (R key)."""
        self.game.restart()
        self.animations = []
    # ------------------------------------------------------------------ #
    # Flip animations
    # ------------------------------------------------------------------ #
    def _spawn_flip_animations(self, cells, new_value):
        """Queue a flip animation for every cell that just changed colour."""
        for row, col in cells:
            self._start_animation({'row': row, 'col': col,
                                   'frame': 0, 'to_value': new_value})
    def _start_animation(self, anim):
        """Replace any existing animation on the same cell and register the new one."""
        self.animations = [a for a in self.animations
                           if not (a['row'] == anim['row'] and a['col'] == anim['col'])]
        self.animations.append(anim)
    def _update_animations(self):
        """Advance all active animations and drop the finished ones."""
        still_running = []
        for anim in self.animations:
            anim['frame'] += 1
            if anim['frame'] <= FLIP_FRAMES:
                still_running.append(anim)
        self.animations = still_running
    # ------------------------------------------------------------------ #
    # Drawing
    # ------------------------------------------------------------------ #
    def _draw(self):
        self._draw_board()
        self._draw_discs()
        self._draw_hints()
        self._draw_last_move_marker()
        self._draw_info_panel()
        pygame.display.flip()
    def _cell_rect(self, row, col):
        return pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    def _draw_board(self):
        self.screen.fill(BG_COLOR)
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, GRID_LINE_COLOR,
                             (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_PIXEL), 2)
            pygame.draw.line(self.screen, GRID_LINE_COLOR,
                             (0, i * CELL_SIZE), (BOARD_PIXEL, i * CELL_SIZE), 2)
    def _draw_discs(self):
        animating = {(a['row'], a['col']): a for a in self.animations}
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                value = self.game.board.grid[row][col]
                if value == EMPTY:
                    continue
                center = self._cell_rect(row, col).center
                if (row, col) in animating:
                    self._draw_flipping_disc(animating[(row, col)], center)
                else:
                    self._draw_static_disc(value, center)
    def _draw_static_disc(self, value, center):
        color = BLACK_DISC_COLOR if value == BLACK else WHITE_DISC_COLOR
        outline = WHITE_DISC_COLOR if value == BLACK else BLACK_DISC_COLOR
        radius = CELL_SIZE // 2 - 6
        pygame.draw.circle(self.screen, color, center, radius)
        pygame.draw.circle(self.screen, outline, center, radius, 1)
    def _draw_flipping_disc(self, anim, center):
        """Draw a disc mid-flip: it squashes horizontally and changes colour halfway."""
        progress = anim['frame'] / FLIP_FRAMES
        scale = abs(1.0 - 2.0 * progress)          # 1 -> 0 -> 1
        if anim['frame'] > FLIP_FRAMES // 2:
            color = BLACK_DISC_COLOR if anim['to_value'] == BLACK else WHITE_DISC_COLOR
        else:
            color = WHITE_DISC_COLOR if anim['to_value'] == BLACK else BLACK_DISC_COLOR
        radius = CELL_SIZE // 2 - 6
        width = max(2, int(2 * radius * scale))
        pygame.draw.ellipse(self.screen, color,
                            (center[0] - width // 2, center[1] - radius,
                             width, 2 * radius))
    def _draw_hints(self):
        """Small dots on every legal cell for the player to move."""
        if self.game.game_over:
            return
        for row, col in self.game.get_valid_moves():
            center = self._cell_rect(row, col).center
            pygame.draw.circle(self.screen, HINT_COLOR, center, 8)
    def _draw_last_move_marker(self):
        if not self.game.last_move:
            return
        pygame.draw.rect(self.screen, LAST_MOVE_COLOR,
                         self._cell_rect(*self.game.last_move), 3)
    def _draw_info_panel(self):
        panel = pygame.Rect(0, BOARD_PIXEL, WINDOW_WIDTH, INFO_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, (20, 20, 20), panel)
        score = self.game.board.get_score()
        black_text = self.score_font.render(
            f"Black: {score[BLACK]}", True, WHITE_DISC_COLOR)
        white_text = self.score_font.render(
            f"White: {score[WHITE]}", True, WHITE_DISC_COLOR)
        self.screen.blit(black_text, (20, BOARD_PIXEL + 12))
        self.screen.blit(white_text, (220, BOARD_PIXEL + 12))
        if self.game.game_over:
            if self.game.winner is None:
                message = "Game over - it's a draw!  Press R to restart."
            else:
                message = (f"Game over - {PLAYER_NAMES[self.game.winner]} wins!  "
                           f"Press R to restart.")
        elif self.game.pass_message:
            message = self.game.pass_message
        else:
            message = f"{PLAYER_NAMES[self.game.current_player]}'s turn  (R = restart)"
        msg_text = self.message_font.render(message, True, (255, 255, 120))
        self.screen.blit(msg_text, (20, BOARD_PIXEL + 52))