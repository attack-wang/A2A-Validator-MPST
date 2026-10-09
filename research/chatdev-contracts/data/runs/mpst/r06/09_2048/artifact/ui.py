'''
ui.py
Tkinter-based graphical user interface for the 2048 game.
Features:
    * 4x4 board of coloured tiles drawn on a Canvas
    * Live score and highest-tile displays
    * Arrow-key (and WASD) controls, N for a new game
    * "New Game" button
    * Game-over overlay with final stats and restart prompt
'''
import tkinter as tk
from game_logic import Game2048, UP, DOWN, LEFT, RIGHT
# Classic 2048 colour palette: tile value -> (background, foreground)
TILE_STYLES = {
    0:    ('#cdc1b4', '#cdc1b4'),
    2:    ('#eee4da', '#776e65'),
    4:    ('#ede0c8', '#776e65'),
    8:    ('#f2b179', '#f9f6f2'),
    16:   ('#f59563', '#f9f6f2'),
    32:   ('#f67c5f', '#f9f6f2'),
    64:   ('#f65e3b', '#f9f6f2'),
    128:  ('#edcf72', '#f9f6f2'),
    256:  ('#edcc61', '#f9f6f2'),
    512:  ('#edc850', '#f9f6f2'),
    1024: ('#edc53f', '#f9f6f2'),
    2048: ('#edc22e', '#f9f6f2'),
}
DEFAULT_TILE_STYLE = ('#3c3a32', '#f9f6f2')   # tiles above 2048
BG_COLOR = '#faf8ef'
BOARD_COLOR = '#bbada0'
TEXT_COLOR = '#776e65'
LIGHT_TEXT_COLOR = '#f9f6f2'
SCORE_BOX_BG = '#bbada0'
SCORE_LABEL_COLOR = '#eee4da'
SCORE_VALUE_COLOR = '#ffffff'
OVERLAY_COLOR = '#cdc1b4'
class GameUI:
    """Tkinter view + controller for the 2048 game."""
    CELL_SIZE = 90
    CELL_GAP = 10
    BOARD_PADDING = 10
    def __init__(self, master=None):
        self.root = tk.Tk() if master is None else master
        self.root.title('2048')
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)
        self.game = Game2048()
        self._build_header()
        self._build_board()
        self._bind_keys()
        self.redraw()
    # ------------------------------------------------------------------ #
    # Widget construction
    # ------------------------------------------------------------------ #
    def _build_header(self):
        """Build the title, the score boxes and the 'New Game' button."""
        header = tk.Frame(self.root, bg=BG_COLOR)
        header.pack(fill='x', padx=16, pady=(16, 8))
        tk.Label(header, text='2048', bg=BG_COLOR, fg=TEXT_COLOR,
                 font=('Helvetica', 32, 'bold')).pack(side='left')
        scores = tk.Frame(header, bg=BG_COLOR)
        scores.pack(side='right')
        self.score_value_label = self._make_score_box(scores, 'SCORE')
        self.highest_value_label = self._make_score_box(scores, 'HIGHEST TILE')
        tk.Button(self.root, text='New Game', command=self.new_game,
                  bg=SCORE_BOX_BG, fg=LIGHT_TEXT_COLOR, relief='flat',
                  activebackground=TEXT_COLOR, activeforeground=LIGHT_TEXT_COLOR,
                  font=('Helvetica', 11, 'bold')).pack(padx=16, pady=(0, 4), anchor='e')
    def _make_score_box(self, parent, label_text):
        """Create one score box; returns the label that holds the value."""
        box = tk.Frame(parent, bg=SCORE_BOX_BG, padx=12, pady=6)
        box.pack(side='left', padx=(8, 0))
        tk.Label(box, text=label_text, bg=SCORE_BOX_BG, fg=SCORE_LABEL_COLOR,
                 font=('Helvetica', 10, 'bold')).pack()
        value_label = tk.Label(box, text='0', bg=SCORE_BOX_BG, fg=SCORE_VALUE_COLOR,
                               font=('Helvetica', 16, 'bold'), width=6)
        value_label.pack()
        return value_label
    def _build_board(self):
        """Build the canvas that renders the 4x4 board."""
        board_px = (self.BOARD_PADDING * 2
                    + self.game.size * self.CELL_SIZE
                    + (self.game.size - 1) * self.CELL_GAP)
        self.canvas = tk.Canvas(self.root, width=board_px, height=board_px,
                                bg=BOARD_COLOR, highlightthickness=0)
        self.canvas.pack(padx=16, pady=(4, 16))
        self.canvas.bind('<Button-1>', self._on_canvas_click)
    def _bind_keys(self):
        """Bind arrow keys, WASD for moves and N for a new game."""
        bindings = {
            '<Up>': UP, '<w>': UP, '<W>': UP,
            '<Down>': DOWN, '<s>': DOWN, '<S>': DOWN,
            '<Left>': LEFT, '<a>': LEFT, '<A>': LEFT,
            '<Right>': RIGHT, '<d>': RIGHT, '<D>': RIGHT,
        }
        for sequence, direction in bindings.items():
            self.root.bind(sequence, lambda event, d=direction: self._on_key(d))
        self.root.bind('<n>', lambda event: self.new_game())
        self.root.bind('<N>', lambda event: self.new_game())
    # ------------------------------------------------------------------ #
    # Event handlers / game flow
    # ------------------------------------------------------------------ #
    def _on_key(self, direction):
        """Handle one directional key press."""
        if self.game.game_over:
            return
        if self.game.move(direction):
            self.redraw()
            if self.game.is_game_over():
                self._draw_game_over_overlay()
    def new_game(self):
        """Restart the game with a fresh board."""
        self.game.reset()
        self.redraw()
    def _on_canvas_click(self, event):
        """Clicking the board after game over starts a new game."""
        if self.game.game_over:
            self.new_game()
    # ------------------------------------------------------------------ #
    # Drawing
    # ------------------------------------------------------------------ #
    def redraw(self):
        """Redraw the whole board and refresh the score displays."""
        self.canvas.delete('all')
        grid = self.game.get_grid()
        for r in range(self.game.size):
            for c in range(self.game.size):
                self._draw_cell(r, c, grid[r][c])
        self.score_value_label.config(text=str(self.game.get_score()))
        self.highest_value_label.config(text=str(self.game.get_highest_tile()))
    def _draw_cell(self, row, col, value):
        """Draw a single cell of the board."""
        x0 = self.BOARD_PADDING + col * (self.CELL_SIZE + self.CELL_GAP)
        y0 = self.BOARD_PADDING + row * (self.CELL_SIZE + self.CELL_GAP)
        x1, y1 = x0 + self.CELL_SIZE, y0 + self.CELL_SIZE
        bg, fg = TILE_STYLES.get(value, DEFAULT_TILE_STYLE)
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg, outline='', width=0)
        if value != 0:
            size = 34 if value < 128 else (28 if value < 1024 else 22)
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(value),
                                    fill=fg, font=('Helvetica', size, 'bold'))
    def _draw_game_over_overlay(self):
        """Draw the semi-transparent game-over overlay with final stats."""
        w, h = int(self.canvas['width']), int(self.canvas['height'])
        self.canvas.create_rectangle(0, 0, w, h, fill=OVERLAY_COLOR,
                                     stipple='gray50', outline='')
        cx, cy = w / 2, h / 2
        self.canvas.create_text(cx, cy - 40, text='Game Over!', fill=TEXT_COLOR,
                                font=('Helvetica', 36, 'bold'))
        self.canvas.create_text(cx, cy + 10, text=f'Final score: {self.game.get_score()}',
                                fill=TEXT_COLOR, font=('Helvetica', 16))
        self.canvas.create_text(cx, cy + 40, text=f'Highest tile: {self.game.get_highest_tile()}',
                                fill=TEXT_COLOR, font=('Helvetica', 16))
        self.canvas.create_text(cx, cy + 80, text='Press N or click "New Game" to play again',
                                fill=TEXT_COLOR, font=('Helvetica', 12))