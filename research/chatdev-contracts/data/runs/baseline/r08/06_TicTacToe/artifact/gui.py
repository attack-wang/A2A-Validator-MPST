'''
gui.py
Tkinter-based graphical interface for the Tic-Tac-Toe game. Renders
the 3x3 board, X/O marks, status messages, a restart button, and a
bottom hint bar, and handles mouse and keyboard input for placing
marks and starting a new game. Uses only the Python standard library,
so the game runs without installing third-party packages such as
pygame (which caused the ModuleNotFoundError in the test report).
'''
import tkinter as tk
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    GRID_SIZE,
    CELL_SIZE,
    BOARD_PIXEL_SIZE,
    GRID_LEFT,
    GRID_TOP,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BUTTON_MARGIN_TOP,
    COLOR_BACKGROUND,
    COLOR_GRID,
    COLOR_TEXT,
    COLOR_X,
    COLOR_O,
    COLOR_HOVER,
    COLOR_WIN_CELL,
    COLOR_BUTTON,
    COLOR_BUTTON_HOVER,
    COLOR_HINT,
    FONT_NAME,
    FONT_SIZE_STATUS,
    FONT_SIZE_MARK,
    FONT_SIZE_BUTTON,
    FONT_SIZE_HINT,
)
from game_logic import TicTacToe
def rgb_to_hex(color):
    '''Convert an (R, G, B) tuple into a '#RRGGBB' string for tkinter.'''
    return '#{:02x}{:02x}{:02x}'.format(*color)
class GameGUI:
    '''Encapsulates all rendering and input handling for the game.'''
    def __init__(self):
        '''Initialize tkinter, the window, fonts, and the game state.'''
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=rgb_to_hex(COLOR_BACKGROUND),
            highlightthickness=0,
        )
        self.canvas.pack()
        self.game = TicTacToe()
        # Pre-convert palette colors to tkinter hex strings.
        self.color_bg = rgb_to_hex(COLOR_BACKGROUND)
        self.color_grid = rgb_to_hex(COLOR_GRID)
        self.color_text = rgb_to_hex(COLOR_TEXT)
        self.color_x = rgb_to_hex(COLOR_X)
        self.color_o = rgb_to_hex(COLOR_O)
        self.color_hover = rgb_to_hex(COLOR_HOVER)
        self.color_win = rgb_to_hex(COLOR_WIN_CELL)
        self.color_button = rgb_to_hex(COLOR_BUTTON)
        self.color_button_hover = rgb_to_hex(COLOR_BUTTON_HOVER)
        self.color_hint = rgb_to_hex(COLOR_HINT)
        # Restart button geometry: (x1, y1, x2, y2).
        button_top = GRID_TOP + BOARD_PIXEL_SIZE + BUTTON_MARGIN_TOP
        self.button_rect = (
            (WINDOW_WIDTH - BUTTON_WIDTH) // 2,
            button_top,
            (WINDOW_WIDTH - BUTTON_WIDTH) // 2 + BUTTON_WIDTH,
            button_top + BUTTON_HEIGHT,
        )
        self.mouse_pos = (0, 0)
        self._last_hover_key = None
        # Bind user input events.
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Motion>', self.on_motion)
        self.root.bind('r', self.on_restart_key)
        self.root.bind('R', self.on_restart_key)
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.draw()
    # ----- Input handling -------------------------------------------------
    def get_cell_from_mouse(self, pos):
        '''Map a mouse position to a (row, col) grid cell, or None if outside.'''
        x, y = pos
        col = (x - GRID_LEFT) // CELL_SIZE
        row = (y - GRID_TOP) // CELL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return int(row), int(col)
        return None
    def in_button(self, pos):
        '''Return True if the given position lies inside the restart button.'''
        x1, y1, x2, y2 = self.button_rect
        return x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2
    def current_hover_key(self):
        '''Return a hashable key describing the current hover highlight.'''
        if self.game.game_over:
            return ('none',)
        if self.in_button(self.mouse_pos):
            return ('button',)
        cell = self.get_cell_from_mouse(self.mouse_pos)
        if cell is not None and self.game.board[cell[0]][cell[1]] == ' ':
            return ('cell', cell[0], cell[1])
        return ('none',)
    def on_click(self, event):
        '''Respond to a left mouse click: restart the game or place a mark.'''
        pos = (event.x, event.y)
        if self.in_button(pos):
            self.game.reset()
        else:
            cell = self.get_cell_from_mouse(pos)
            if cell is not None:
                row, col = cell
                self.game.make_move(row, col)
        self._last_hover_key = None  # Force a redraw with fresh state.
        self.draw()
    def on_motion(self, event):
        '''Track mouse movement and redraw only when the hover target changes.'''
        self.mouse_pos = (event.x, event.y)
        hover_key = self.current_hover_key()
        if hover_key != self._last_hover_key:
            self._last_hover_key = hover_key
            self.draw()
    def on_restart_key(self, event):
        '''Reset the game when the R key is pressed.'''
        self.game.reset()
        self._last_hover_key = None
        self.draw()
    def on_close(self):
        '''Close the window and end the application.'''
        self.root.destroy()
    # ----- Rendering ------------------------------------------------------
    def get_winning_cells(self):
        '''Return the set of (row, col) cells that form the winning line.'''
        line = self.game.get_winning_line()
        if line is None:
            return set()
        (r1, c1), (r2, c2) = line
        step_row = (r2 - r1) // 2
        step_col = (c2 - c1) // 2
        return {(r1, c1), (r1 + step_row, c1 + step_col), (r2, c2)}
    def draw_board(self, winning_cells):
        '''Draw the cell backgrounds (with hover/win highlights) and grid lines.'''
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1 = GRID_LEFT + col * CELL_SIZE
                y1 = GRID_TOP + row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                if (row, col) in winning_cells:
                    fill = self.color_win
                elif (
                    self.game.board[row][col] == ' '
                    and not self.game.game_over
                    and x1 <= self.mouse_pos[0] <= x2
                    and y1 <= self.mouse_pos[1] <= y2
                ):
                    fill = self.color_hover
                else:
                    fill = self.color_bg
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill, outline=self.color_grid, width=2,
                )
    def draw_marks(self):
        '''Render the X and O symbols inside their cells.'''
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                mark = self.game.board[row][col]
                if mark == ' ':
                    continue
                color = self.color_x if mark == 'X' else self.color_o
                cx = GRID_LEFT + col * CELL_SIZE + CELL_SIZE // 2
                cy = GRID_TOP + row * CELL_SIZE + CELL_SIZE // 2
                # Negative font size => size in pixels, matching the pygame look.
                self.canvas.create_text(
                    cx, cy, text=mark, fill=color,
                    font=(FONT_NAME, -FONT_SIZE_MARK, 'bold'),
                )
    def draw_status(self):
        '''Show whose turn it is, or the winner / draw result.'''
        if self.game.game_over:
            if self.game.winner is not None:
                message = "Player {} wins!".format(self.game.winner)
                color = self.color_x if self.game.winner == 'X' else self.color_o
            else:
                message = "It's a draw!"
                color = self.color_text
        else:
            message = "Player {}'s turn".format(self.game.current_player)
            color = self.color_x if self.game.current_player == 'X' else self.color_o
        self.canvas.create_text(
            WINDOW_WIDTH // 2, 55, text=message, fill=color,
            font=(FONT_NAME, -FONT_SIZE_STATUS, 'bold'),
        )
    def draw_restart_button(self):
        '''Draw the restart button with a hover highlight.'''
        x1, y1, x2, y2 = self.button_rect
        color = self.color_button_hover if self.in_button(self.mouse_pos) else self.color_button
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color, outline=self.color_grid, width=1,
        )
        self.canvas.create_text(
            (x1 + x2) // 2, (y1 + y2) // 2,
            text="Restart Game", fill=self.color_text,
            font=(FONT_NAME, -FONT_SIZE_BUTTON, 'bold'),
        )
    def draw_hint(self):
        '''Render the bottom hint bar with usage instructions.'''
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT - 18,
            text="Click a cell to play  |  Press R or click Restart for a new game",
            fill=self.color_hint,
            font=(FONT_NAME, -FONT_SIZE_HINT),
        )
    def draw(self):
        '''Render one complete frame of the game.'''
        self.canvas.delete('all')
        self.draw_status()
        self.draw_board(self.get_winning_cells())
        self.draw_marks()
        self.draw_restart_button()
        self.draw_hint()
    # ----- Main loop ------------------------------------------------------
    def run(self):
        '''Run the tkinter main loop until the window is closed.'''
        self.root.mainloop()