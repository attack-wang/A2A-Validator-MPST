'''
gui.py
Pygame-based graphical front-end for the Reversi (Othello) game.
Renders the 8x8 board, the discs, highlights for all valid moves, a
live scoreboard and status messages, and translates mouse clicks into
game moves. Also provides a game-over overlay and a restart button.
'''
import sys
import pygame
from constants import (
    BOARD_SIZE, EMPTY, BLACK, WHITE, PLAYER_NAMES,
    FPS, CELL_SIZE, BOARD_PIXEL_SIZE, MARGIN,
    WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_X, BOARD_Y, SIDEBAR_X,
    COLOR_BACKGROUND, COLOR_BOARD, COLOR_GRID_LINE, COLOR_TEXT,
    COLOR_TEXT_DIM, COLOR_HIGHLIGHT, COLOR_BUTTON, COLOR_BUTTON_HOVER,
    COLOR_BLACK_DISC, COLOR_WHITE_DISC,
)
class Button:
    '''A simple clickable rectangular button.'''
    def __init__(self, rect, text, font):
        self.rect = rect
        self.text = text
        self.font = font
    def draw(self, surface, mouse_pos):
        '''Render the button, brightening it when the mouse hovers over it.'''
        hovered = self.rect.collidepoint(mouse_pos)
        color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_TEXT_DIM, self.rect, 2, border_radius=8)
        label = self.font.render(self.text, True, COLOR_TEXT)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)
    def was_clicked(self, event_pos):
        '''Return True if the given click position is inside the button.'''
        return self.rect.collidepoint(event_pos)
class GameGUI:
    '''Main pygame application: event handling, rendering and the game loop.'''
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Reversi (Othello)")
        self.font_large = pygame.font.SysFont("arial", 34, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_tiny = pygame.font.SysFont("arial", 14)
        self.restart_button = Button(
            pygame.Rect(SIDEBAR_X, WINDOW_HEIGHT - 70, 200, 44),
            "Restart Game", self.font_medium)
        self.running = True
    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def handle_events(self):
        '''Process the pygame event queue.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)
    def handle_click(self, pos):
        '''React to a left mouse click (board cell or button).'''
        if self.restart_button.was_clicked(pos):
            self.game.reset()
            return
        if self.game.game_over:
            return
        cell = self.pixel_to_cell(pos)
        if cell is not None:
            row, col = cell
            self.game.make_move(row, col)
    def pixel_to_cell(self, pos):
        '''Convert window coordinates to a (row, col) board cell, or None.'''
        x, y = pos
        col = (x - BOARD_X) // CELL_SIZE
        row = (y - BOARD_Y) // CELL_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return int(row), int(col)
        return None
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw(self):
        '''Render one full frame.'''
        self.screen.fill(COLOR_BACKGROUND)
        self.draw_board()
        self.draw_valid_moves()
        self.draw_discs()
        self.draw_sidebar()
        if self.game.game_over:
            self.draw_game_over_overlay()
        pygame.display.flip()
    def draw_board(self):
        '''Draw the green board surface, grid lines and coordinates.'''
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE)
        pygame.draw.rect(self.screen, COLOR_BOARD, board_rect)
        # Grid lines
        for i in range(BOARD_SIZE + 1):
            start_h = (BOARD_X, BOARD_Y + i * CELL_SIZE)
            end_h = (BOARD_X + BOARD_PIXEL_SIZE, BOARD_Y + i * CELL_SIZE)
            pygame.draw.line(self.screen, COLOR_GRID_LINE, start_h, end_h, 2)
            start_v = (BOARD_X + i * CELL_SIZE, BOARD_Y)
            end_v = (BOARD_X + i * CELL_SIZE, BOARD_Y + BOARD_PIXEL_SIZE)
            pygame.draw.line(self.screen, COLOR_GRID_LINE, start_v, end_v, 2)
        # Column letters A-H on top, row numbers 1-8 on the left
        for col in range(BOARD_SIZE):
            label = self.font_tiny.render(chr(ord('A') + col), True, COLOR_TEXT_DIM)
            self.screen.blit(label, label.get_rect(
                midtop=(BOARD_X + col * CELL_SIZE + CELL_SIZE // 2, BOARD_Y - 14)))
        for row in range(BOARD_SIZE):
            label = self.font_tiny.render(str(row + 1), True, COLOR_TEXT_DIM)
            self.screen.blit(label, label.get_rect(
                midright=(BOARD_X - 8, BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2)))
        # The four centre star points, a classic Othello board detail
        for (r, c) in [(2, 2), (2, 6), (6, 2), (6, 6)]:
            center = (BOARD_X + c * CELL_SIZE, BOARD_Y + r * CELL_SIZE)
            pygame.draw.circle(self.screen, COLOR_GRID_LINE, center, 4)
    def cell_center(self, row, col):
        '''Pixel centre of a board cell.'''
        return (BOARD_X + col * CELL_SIZE + CELL_SIZE // 2,
                BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2)
    def draw_disc(self, row, col, player):
        '''Draw a single black or white disc centred in its cell.'''
        center = self.cell_center(row, col)
        radius = CELL_SIZE // 2 - 6
        if player == BLACK:
            pygame.draw.circle(self.screen, COLOR_BLACK_DISC, center, radius)
            pygame.draw.circle(self.screen, (80, 80, 80), center, radius, 1)
        else:
            pygame.draw.circle(self.screen, COLOR_WHITE_DISC, center, radius)
            pygame.draw.circle(self.screen, (120, 120, 120), center, radius, 1)
    def draw_discs(self):
        '''Draw every disc currently on the board.'''
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                disc = self.game.board.get_disc(row, col)
                if disc != EMPTY:
                    self.draw_disc(row, col, disc)
    def draw_valid_moves(self):
        '''Highlight every legal move for the current player.'''
        if self.game.game_over:
            return
        for (row, col) in self.game.get_valid_moves():
            center = self.cell_center(row, col)
            pygame.draw.circle(self.screen, COLOR_HIGHLIGHT, center, 7)
    def draw_sidebar(self):
        '''Draw the scoreboard, turn indicator and status message.'''
        score = self.game.get_score()
        x = SIDEBAR_X
        y = MARGIN
        title = self.font_large.render("REVERSI", True, COLOR_TEXT)
        self.screen.blit(title, (x, y))
        y += 52
        # Black player panel
        self.draw_player_panel(x, y, BLACK, score[BLACK],
                               self.game.current_player == BLACK and not self.game.game_over)
        y += 84
        self.draw_player_panel(x, y, WHITE, score[WHITE],
                               self.game.current_player == WHITE and not self.game.game_over)
        y += 96
        # Status message (wrapped over up to three lines)
        self.draw_wrapped_text(self.game.message, x, y, 210, self.font_small, COLOR_TEXT)
        y += 90
        hint = self.font_tiny.render("Yellow dots = valid moves", True, COLOR_TEXT_DIM)
        self.screen.blit(hint, (x, y))
        # Restart button (also used as "Play Again" after game over)
        self.restart_button.draw(self.screen, pygame.mouse.get_pos())
    def draw_player_panel(self, x, y, player, count, is_active):
        '''Draw one player's score panel with an active-turn border.'''
        panel = pygame.Rect(x, y, 200, 72)
        pygame.draw.rect(self.screen, (45, 45, 45), panel, border_radius=10)
        border = COLOR_HIGHLIGHT if is_active else (70, 70, 70)
        pygame.draw.rect(self.screen, border, panel, 3, border_radius=10)
        # Disc icon
        icon_center = (x + 34, y + 36)
        radius = 20
        if player == BLACK:
            pygame.draw.circle(self.screen, COLOR_BLACK_DISC, icon_center, radius)
            pygame.draw.circle(self.screen, (90, 90, 90), icon_center, radius, 2)
        else:
            pygame.draw.circle(self.screen, COLOR_WHITE_DISC, icon_center, radius)
            pygame.draw.circle(self.screen, (120, 120, 120), icon_center, radius, 2)
        name = self.font_medium.render(PLAYER_NAMES[player], True, COLOR_TEXT)
        self.screen.blit(name, (x + 66, y + 8))
        count_text = self.font_large.render(str(count), True, COLOR_TEXT)
        self.screen.blit(count_text, (x + 66, y + 32))
        if is_active:
            turn = self.font_tiny.render("Your turn", True, COLOR_HIGHLIGHT)
            self.screen.blit(turn, (x + 130, y + 40))
    def draw_wrapped_text(self, text, x, y, width, font, color):
        '''Render `text` word-wrapped to `width` pixels, up to 4 lines.'''
        words = text.split()
        lines = []
        current = ""
        for word in words:
            trial = (current + " " + word).strip()
            if font.size(trial)[0] <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        lines = lines[:4]
        for i, line in enumerate(lines):
            self.screen.blit(font.render(line, True, color), (x, y + i * 22))
    def draw_game_over_overlay(self):
        '''Semi-transparent overlay announcing the final result.'''
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        score = self.game.get_score()
        if self.game.winner is None:
            headline = "It's a draw!"
        else:
            headline = f"{PLAYER_NAMES[self.game.winner]} wins!"
        title = self.font_large.render(headline, True, COLOR_HIGHLIGHT)
        title_rect = title.get_rect(center=(BOARD_X + BOARD_PIXEL_SIZE // 2,
                                            BOARD_Y + BOARD_PIXEL_SIZE // 2 - 30))
        self.screen.blit(title, title_rect)
        final = self.font_medium.render(
            f"Black {score[BLACK]}  -  {score[WHITE]} White", True, COLOR_TEXT)
        final_rect = final.get_rect(center=(BOARD_X + BOARD_PIXEL_SIZE // 2,
                                            BOARD_Y + BOARD_PIXEL_SIZE // 2 + 16))
        self.screen.blit(final, final_rect)
        again = self.font_small.render("Click 'Restart Game' to play again", True, COLOR_TEXT_DIM)
        again_rect = again.get_rect(center=(BOARD_X + BOARD_PIXEL_SIZE // 2,
                                            BOARD_Y + BOARD_PIXEL_SIZE // 2 + 52))
        self.screen.blit(again, again_rect)
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        '''Run the application until the user closes the window.'''
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()