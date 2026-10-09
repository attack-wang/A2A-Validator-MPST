'''
gui.py
This module implements the graphical user interface for the Reversi game
using tkinter. It renders:
- The 8x8 board with grid lines and colored discs
- Green markers on every legal move for the current player
- A live scoreboard for both players, with the active player's label
  highlighted so it is always clear whose turn it is
- Status messages (whose turn, passes, game result)
Mouse clicks on the board are translated into game moves.
'''
import tkinter as tk
from tkinter import messagebox
from board import BLACK, WHITE, EMPTY
from game import Game
CELL_SIZE = 64          # Pixels per board cell
BOARD_PX = CELL_SIZE * 8
PADDING = 24            # Margin around the board inside the canvas
CANVAS_SIZE = BOARD_PX + PADDING * 2
BOARD_GREEN = "#1e7a34"
GRID_COLOR = "#0d3d1a"
HINT_COLOR = "#7fd48a"
DISC_BLACK = "#111111"
DISC_WHITE = "#f5f5f5"
DISC_OUTLINE = "#333333"
ACTIVE_BG = "#ffe08a"   # Highlight color for the active player's score label
PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}
class ReversiGUI:
    """Tkinter front-end for a Reversi Game instance."""
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Reversi (Othello)")
        self.root.resizable(False, False)
        # --- Score panel -------------------------------------------------
        self.score_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
        self.score_frame.pack(padx=10, pady=(10, 4), fill=tk.X)
        self.black_label = tk.Label(
            self.score_frame, text="Black: 2", font=("Helvetica", 14, "bold"),
            fg=DISC_BLACK)
        self.black_label.pack(side=tk.LEFT, padx=12, pady=6)
        self.status_label = tk.Label(
            self.score_frame, text="Black's turn", font=("Helvetica", 14),
            fg="#0b5d1e")
        self.status_label.pack(side=tk.TOP, pady=2)
        self.white_label = tk.Label(
            self.score_frame, text="White: 2", font=("Helvetica", 14, "bold"),
            fg="#444444")
        self.white_label.pack(side=tk.RIGHT, padx=12, pady=6)
        # Remember each platform's default label background so the active
        # player highlight can be restored safely on any OS.
        self.default_label_bg = self.black_label.cget("bg")
        # --- Board canvas ------------------------------------------------
        self.canvas = tk.Canvas(
            root, width=CANVAS_SIZE, height=CANVAS_SIZE,
            bg=BOARD_GREEN, highlightthickness=0)
        self.canvas.pack(padx=10, pady=(4, 10))
        self.canvas.bind("<Button-1>", self.on_click)
        # --- Restart button ----------------------------------------------
        self.restart_button = tk.Button(
            root, text="New Game", font=("Helvetica", 12, "bold"),
            command=self.restart)
        self.restart_button.pack(pady=(0, 10))
        self.game_over_shown = False
        self.refresh()
    # ------------------------------------------------------------------ #
    # Drawing helpers
    # ------------------------------------------------------------------ #
    def cell_top_left(self, row, col):
        """Return the pixel coordinates of a cell's top-left corner."""
        x = PADDING + col * CELL_SIZE
        y = PADDING + row * CELL_SIZE
        return x, y
    def draw_board(self):
        """Render grid lines, discs and legal-move hints."""
        self.canvas.delete(tk.ALL)
        # Outer border
        self.canvas.create_rectangle(
            PADDING, PADDING, PADDING + BOARD_PX, PADDING + BOARD_PX,
            outline=GRID_COLOR, width=3)
        # Grid lines
        for i in range(1, 8):
            pos = PADDING + i * CELL_SIZE
            self.canvas.create_line(
                pos, PADDING, pos, PADDING + BOARD_PX,
                fill=GRID_COLOR, width=1)
            self.canvas.create_line(
                PADDING, pos, PADDING + BOARD_PX, pos,
                fill=GRID_COLOR, width=1)
        # Small reference dots at the four star points (classic Othello look)
        for r in (2, 6):
            for c in (2, 6):
                x, y = self.cell_top_left(r, c)
                self.canvas.create_oval(
                    x - 3, y - 3, x + 3, y + 3,
                    fill=GRID_COLOR, outline=GRID_COLOR)
        # Legal move hints for the current player
        if not self.game.is_game_over():
            for (row, col) in self.game.get_valid_moves():
                x, y = self.cell_top_left(row, col)
                cx = x + CELL_SIZE / 2
                cy = y + CELL_SIZE / 2
                self.canvas.create_oval(
                    cx - 6, cy - 6, cx + 6, cy + 6,
                    fill=HINT_COLOR, outline="")
        # Discs
        for row in range(self.game.board.size):
            for col in range(self.game.board.size):
                disc = self.game.board.get_disc(row, col)
                if disc == EMPTY:
                    continue
                self.draw_disc(row, col, disc)
        # Highlight the most recent move with a thin ring
        if self.game.last_move is not None:
            row, col = self.game.last_move
            x, y = self.cell_top_left(row, col)
            self.canvas.create_rectangle(
                x + 1, y + 1, x + CELL_SIZE - 1, y + CELL_SIZE - 1,
                outline="#ffd54d", width=2)
    def draw_disc(self, row, col, disc):
        """Draw a single disc centered in the given cell."""
        x, y = self.cell_top_left(row, col)
        margin = 7
        color = DISC_BLACK if disc == BLACK else DISC_WHITE
        self.canvas.create_oval(
            x + margin, y + margin,
            x + CELL_SIZE - margin, y + CELL_SIZE - margin,
            fill=color, outline=DISC_OUTLINE, width=2)
    # ------------------------------------------------------------------ #
    # UI updates
    # ------------------------------------------------------------------ #
    def update_score(self):
        """Refresh the scoreboard labels and highlight the active player."""
        score = self.game.get_score()
        over = self.game.is_game_over()
        current = self.game.current_player
        self.black_label.config(
            text="Black: {}".format(score['black']),
            bg=ACTIVE_BG if (current == BLACK and not over) else self.default_label_bg)
        self.white_label.config(
            text="White: {}".format(score['white']),
            bg=ACTIVE_BG if (current == WHITE and not over) else self.default_label_bg)
    def update_status(self):
        """Refresh the status line (turn info, pass notices, result)."""
        if self.game.is_game_over():
            winner = self.game.get_winner()
            score = self.game.get_score()
            if winner is None:
                text = "Game over — it's a draw! ({} - {})".format(
                    score['black'], score['white'])
            else:
                text = "Game over — {} wins! ({} - {})".format(
                    PLAYER_NAMES[winner], score['black'], score['white'])
            self.status_label.config(text=text)
        elif self.game.passed_last_turn:
            previous = -self.game.current_player
            text = "{} has no valid moves — pass! {}'s turn".format(
                PLAYER_NAMES[previous], PLAYER_NAMES[self.game.current_player])
            self.status_label.config(text=text)
        else:
            text = "{}'s turn".format(PLAYER_NAMES[self.game.current_player])
            self.status_label.config(text=text)
    def refresh(self):
        """Redraw the whole interface from the current game state."""
        self.draw_board()
        self.update_score()
        self.update_status()
    # ------------------------------------------------------------------ #
    # Event handling
    # ------------------------------------------------------------------ #
    def on_click(self, event):
        """Translate a canvas click into a board move when legal."""
        if self.game.is_game_over():
            return
        col = (event.x - PADDING) // CELL_SIZE
        row = (event.y - PADDING) // CELL_SIZE
        if not self.game.board.is_valid_position(row, col):
            return
        if self.game.make_move(row, col):
            self.game_over_shown = False
            self.refresh()
            self.check_game_over()
        else:
            # Illegal click: brief feedback without disturbing the layout.
            self.status_label.config(
                text="Invalid move — {} must flip at least one disc".format(
                    PLAYER_NAMES[self.game.current_player]))
    def check_game_over(self):
        """Show a dialog announcing the final result once the game ends."""
        if self.game.is_game_over() and not self.game_over_shown:
            self.game_over_shown = True
            winner = self.game.get_winner()
            score = self.game.get_score()
            if winner is None:
                message = "The game ended in a draw!\n\nFinal score — Black: {}, White: {}".format(
                    score['black'], score['white'])
            else:
                message = "{} wins!\n\nFinal score — Black: {}, White: {}".format(
                    PLAYER_NAMES[winner], score['black'], score['white'])
            messagebox.showinfo("Game Over", message)
    def restart(self):
        """Start a fresh game and redraw the interface."""
        self.game = Game()
        self.game_over_shown = False
        self.refresh()
    def run(self):
        """Start the tkinter main loop."""
        self.root.mainloop()