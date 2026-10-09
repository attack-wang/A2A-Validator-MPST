'''
gui.py
Tkinter front-end for the 2048 game.
Renders the 4x4 board, handles arrow-key input, and displays the
current score and highest tile reached.
This module fixes the ImportError reported in the test run: the
Game2048GUI class was missing (the file previously contained only a
stray orphaned method). The full class is restored here.
'''
import tkinter as tk
from game_logic import Game2048
class Game2048GUI:
    """Tkinter front-end that renders the Game2048 engine and handles input."""
    BG_COLOR = "#bbada0"
    EMPTY_COLOR = "#cdc1b4"
    TEXT_COLOR = "#776e65"
    LIGHT_TEXT_COLOR = "#f9f6f2"
    TILE_COLORS = {
        2:    ("#eee4da", TEXT_COLOR),
        4:    ("#ede0c8", TEXT_COLOR),
        8:    ("#f2b179", LIGHT_TEXT_COLOR),
        16:   ("#f59563", LIGHT_TEXT_COLOR),
        32:   ("#f67c5f", LIGHT_TEXT_COLOR),
        64:   ("#f65e3b", LIGHT_TEXT_COLOR),
        128:  ("#edcf72", LIGHT_TEXT_COLOR),
        256:  ("#edcc61", LIGHT_TEXT_COLOR),
        512:  ("#edc850", LIGHT_TEXT_COLOR),
        1024: ("#edc53f", LIGHT_TEXT_COLOR),
        2048: ("#edc22e", LIGHT_TEXT_COLOR),
    }
    DEFAULT_TILE_COLOR = ("#3c3a32", LIGHT_TEXT_COLOR)
    def __init__(self, master):
        self.master = master
        master.title("2048")
        master.resizable(False, False)
        self.game = Game2048()
        # ----- Header: title, score, highest tile -----
        header = tk.Frame(master, bg=self.BG_COLOR)
        header.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(header, text="2048", font=("Helvetica", 32, "bold"),
                 bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(side="left", padx=10)
        self.score_var = tk.StringVar(value="Score: 0")
        self.highest_var = tk.StringVar(value="Highest: 0")
        tk.Label(header, textvariable=self.highest_var, font=("Helvetica", 14, "bold"),
                 bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(side="right", padx=10)
        tk.Label(header, textvariable=self.score_var, font=("Helvetica", 14, "bold"),
                 bg=self.BG_COLOR, fg=self.TEXT_COLOR).pack(side="right", padx=10)
        # ----- Board: 4x4 grid of labels -----
        self.board_frame = tk.Frame(master, bg=self.BG_COLOR)
        self.board_frame.pack(padx=10, pady=5)
        self.cells = []
        for r in range(self.game.size):
            row = []
            for c in range(self.game.size):
                cell = tk.Label(self.board_frame, text="", width=6, height=3,
                                font=("Helvetica", 20, "bold"),
                                bg=self.EMPTY_COLOR, fg=self.TEXT_COLOR)
                cell.grid(row=r, column=c, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)
        # ----- Footer: instructions + new game button -----
        footer = tk.Frame(master, bg=self.BG_COLOR)
        footer.pack(fill="x", padx=10, pady=(5, 10))
        tk.Label(footer, text="Arrow keys to move  •  R to restart",
                 font=("Helvetica", 11), bg=self.BG_COLOR,
                 fg=self.TEXT_COLOR).pack(side="left", padx=10)
        tk.Button(footer, text="New Game", command=self.new_game).pack(side="right", padx=10)
        # ----- Game-over overlay -----
        self.overlay = None
        # ----- Keyboard bindings -----
        master.bind("<Left>",  lambda e: self.handle_move("left"))
        master.bind("<Right>", lambda e: self.handle_move("right"))
        master.bind("<Up>",    lambda e: self.handle_move("up"))
        master.bind("<Down>",  lambda e: self.handle_move("down"))
        master.bind("r", lambda e: self.new_game())
        master.bind("R", lambda e: self.new_game())
        self.refresh()
    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def handle_move(self, direction):
        """Apply a move, refresh the display, and check for game over."""
        if self.game.is_game_over():
            return
        if self.game.move(direction):
            self.refresh()
            if self.game.is_game_over():
                self.show_game_over()
    def new_game(self):
        """Reset the game and clear the game-over overlay."""
        self.game.reset()
        self.hide_game_over()
        self.refresh()
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def refresh(self):
        """Redraw the board, score and highest tile from the game state."""
        board = self.game.get_board()
        for r in range(self.game.size):
            for c in range(self.game.size):
                value = board[r][c]
                cell = self.cells[r][c]
                if value == 0:
                    cell.config(text="", bg=self.EMPTY_COLOR, fg=self.TEXT_COLOR)
                else:
                    bg, fg = self.TILE_COLORS.get(value, self.DEFAULT_TILE_COLOR)
                    cell.config(text=str(value), bg=bg, fg=fg)
        self.score_var.set(f"Score: {self.game.get_score()}")
        self.highest_var.set(f"Highest: {self.game.get_highest_tile()}")
    def show_game_over(self):
        """Display a semi-transparent 'Game Over' overlay on the board."""
        if self.overlay is not None:
            return
        self.overlay = tk.Frame(self.board_frame, bg="#8f7a66")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Label(self.overlay, text="Game Over!", font=("Helvetica", 28, "bold"),
                 bg="#8f7a66", fg=self.LIGHT_TEXT_COLOR).pack(expand=True)
        tk.Button(self.overlay, text="Try Again", command=self.new_game).pack(pady=10)
    def hide_game_over(self):
        """Remove the game-over overlay if present."""
        if self.overlay is not None:
            self.overlay.destroy()
            self.overlay = None