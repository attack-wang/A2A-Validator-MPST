'''
Tkinter-based graphical front end for the 2048 game.
Renders the 4x4 board, the current score, the highest tile reached and a
"New Game" button. Arrow keys (and WASD) slide the tiles. When no moves
remain, an overlay appears offering a restart.
'''
import tkinter as tk
from constants import (
    WINDOW_TITLE, WINDOW_BG, GRID_BG, CELL_PADX, CELL_PADY, GRID_PAD, HEADER_PAD,
    TITLE_FONT, SCORE_LABEL_FONT, SCORE_VALUE_FONT,
    TILE_FONT_LARGE, TILE_FONT_MEDIUM, TILE_FONT_SMALL,
    INSTRUCTION_FONT, GAME_OVER_FONT,
    TEXT_COLOR, EMPTY_CELL_BG, SCORE_BOX_BG, SCORE_LABEL_FG, SCORE_VALUE_FG,
    BUTTON_BG, BUTTON_FG, GAME_OVER_BG, GAME_OVER_TEXT_FG,
    TILE_COLORS, DEFAULT_TILE_COLORS,
)
class Game2048GUI:
    '''Tkinter view + controller for a Game2048 model.'''
    def __init__(self, master, game):
        self.master = master
        self.game = game
        self._overlay = None  # Reference to the game-over overlay frame.
        master.title(WINDOW_TITLE)
        master.resizable(False, False)
        master.configure(bg=WINDOW_BG)
        self._build_header()
        self._build_board()
        self._build_footer()
        self._bind_keys()
        self.update_display()
        master.focus_set()
    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_header(self):
        '''Build the title, score boxes and New Game button.'''
        header = tk.Frame(self.master, bg=WINDOW_BG)
        header.pack(fill="x", padx=HEADER_PAD, pady=(HEADER_PAD, 5))
        tk.Label(header, text="2048", font=TITLE_FONT,
                 bg=WINDOW_BG, fg=TEXT_COLOR).pack(side="left")
        score_area = tk.Frame(header, bg=WINDOW_BG)
        score_area.pack(side="right")
        self.score_var = tk.StringVar(value="0")
        self.highest_var = tk.StringVar(value="0")
        self._make_score_box(score_area, "SCORE", self.score_var)
        self._make_score_box(score_area, "BEST TILE", self.highest_var)
        tk.Button(header, text="New Game", command=self.restart,
                  font=SCORE_VALUE_FONT, bg=BUTTON_BG, fg=BUTTON_FG,
                  activebackground=BUTTON_BG, activeforeground=BUTTON_FG,
                  relief="flat", padx=10, pady=5, cursor="hand2"
                  ).pack(side="right", padx=(0, 10))
    def _make_score_box(self, parent, caption, text_var):
        '''Create one labelled score box bound to a StringVar.'''
        box = tk.Frame(parent, bg=SCORE_BOX_BG, padx=15, pady=5)
        box.pack(side="left", padx=5)
        tk.Label(box, text=caption, font=SCORE_LABEL_FONT,
                 bg=SCORE_BOX_BG, fg=SCORE_LABEL_FG).pack()
        tk.Label(box, textvariable=text_var, font=SCORE_VALUE_FONT,
                 bg=SCORE_BOX_BG, fg=SCORE_VALUE_FG).pack()
    def _build_board(self):
        '''Build the 4x4 grid of cell labels.'''
        self.grid_frame = tk.Frame(self.master, bg=GRID_BG)
        self.grid_frame.pack(padx=GRID_PAD, pady=GRID_PAD)
        self.cell_labels = []
        for r in range(self.game.size):
            row_labels = []
            for c in range(self.game.size):
                cell = tk.Label(self.grid_frame, text="", width=4, height=2,
                                font=TILE_FONT_LARGE, bg=EMPTY_CELL_BG)
                cell.grid(row=r, column=c, padx=CELL_PADX, pady=CELL_PADY)
                row_labels.append(cell)
            self.cell_labels.append(row_labels)
    def _build_footer(self):
        '''Build the instruction line under the board.'''
        tk.Label(self.master,
                 text="Use arrow keys (or WASD) to slide tiles. "
                      "Merge equal tiles to reach 2048!",
                 font=INSTRUCTION_FONT, bg=WINDOW_BG, fg=TEXT_COLOR
                 ).pack(pady=(0, HEADER_PAD))
    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------
    def _bind_keys(self):
        '''Bind all keyboard input to the key handler.'''
        self.master.bind("<Key>", self._on_key)
    def _on_key(self, event):
        '''Map arrow/WASD keys to game moves; ignore keys when game over.'''
        direction_map = {
            "Up": "up", "Down": "down", "Left": "left", "Right": "right",
            "w": "up", "s": "down", "a": "left", "d": "right",
            "W": "up", "S": "down", "A": "left", "D": "right",
        }
        direction = direction_map.get(event.keysym)
        if direction and not self.game.game_over:
            if self.game.move(direction):
                self.update_display()
                if self.game.game_over:
                    self.master.after(100, self.show_game_over)
            return "break"
    # ------------------------------------------------------------------
    # Display updates
    # ------------------------------------------------------------------
    def update_display(self):
        '''Refresh all cells, the score and the highest tile.'''
        for r in range(self.game.size):
            for c in range(self.game.size):
                value = self.game.board[r][c]
                label = self.cell_labels[r][c]
                if value == 0:
                    label.config(text="", bg=EMPTY_CELL_BG, fg=EMPTY_CELL_BG,
                                 font=TILE_FONT_LARGE)
                else:
                    bg, fg = TILE_COLORS.get(value, DEFAULT_TILE_COLORS)
                    # Shrink font for 3-4 digit tiles so text fits the cell.
                    if value < 100:
                        font = TILE_FONT_LARGE
                    elif value < 1000:
                        font = TILE_FONT_MEDIUM
                    else:
                        font = TILE_FONT_SMALL
                    label.config(text=str(value), bg=bg, fg=fg, font=font)
        self.score_var.set(str(self.game.score))
        self.highest_var.set(str(self.game.highest_tile))
    def show_game_over(self):
        '''Show the game-over overlay with a restart button.'''
        if self._overlay is not None:
            return
        self._overlay = tk.Frame(self.grid_frame, bg=GAME_OVER_BG)
        self._overlay.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(self._overlay, text="Game Over!", font=GAME_OVER_FONT,
                 bg=GAME_OVER_BG, fg=GAME_OVER_TEXT_FG).pack(padx=20, pady=(20, 10))
        tk.Button(self._overlay, text="Try Again", command=self.restart,
                  bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", padx=10, pady=5,
                  cursor="hand2").pack(pady=(0, 20))
    def restart(self):
        '''Reset the model, remove the overlay and refresh the view.'''
        self.game.reset()
        if self._overlay is not None:
            self._overlay.destroy()
            self._overlay = None
        self.update_display()