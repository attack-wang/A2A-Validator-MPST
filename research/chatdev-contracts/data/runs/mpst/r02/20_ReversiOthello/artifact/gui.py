'''
gui.py
This module provides the graphical user interface for the Reversi game
using tkinter. It renders the board, highlights valid moves, handles
mouse input, and displays live scores and game status.
'''
import tkinter as tk
from tkinter import messagebox
from board import BLACK, WHITE, EMPTY
from game import Game
CELL_SIZE = 64          # pixels per board cell
BOARD_PIXELS = CELL_SIZE * 8
PADDING = 20            # margin around the board inside the canvas
CANVAS_SIZE = BOARD_PIXELS + PADDING * 2
COLORS = {
    BLACK: "black",
    WHITE: "white",
}
PLAYER_NAMES = {
    BLACK: "Black",
    WHITE: "White",
}
class ReversiGUI:
    """Tkinter-based graphical interface for Reversi."""
    def __init__(self, root):
        '''Initialize the game state and build the whole interface.'''
        self.root = root
        self.root.title("Reversi (Othello)")
        self.root.resizable(False, False)
        self.game = Game()
        self._build_layout()
        self._bind_events()
        self.refresh()
    # ------------------------------------------------------------------
    # Layout construction
    # ------------------------------------------------------------------
    def _build_layout(self):
        '''Create the score panel, board canvas, status bar and restart button.'''
        # Top panel: live scores and the turn indicator.
        top = tk.Frame(self.root)
        top.pack(pady=5)
        self.black_score_label = tk.Label(top, text="Black: 2",
                                          font=("Arial", 14, "bold"))
        self.black_score_label.pack(side=tk.LEFT, padx=15)
        self.turn_label = tk.Label(top, text="Turn: Black", font=("Arial", 14))
        self.turn_label.pack(side=tk.LEFT, padx=15)
        self.white_score_label = tk.Label(top, text="White: 2",
                                          font=("Arial", 14, "bold"))
        self.white_score_label.pack(side=tk.LEFT, padx=15)
        # Board canvas (green felt with an 8x8 grid drawn on it).
        self.canvas = tk.Canvas(self.root, width=CANVAS_SIZE,
                                height=CANVAS_SIZE, bg="green")
        self.canvas.pack(padx=10, pady=5)
        # Bottom panel: status message and a restart button.
        bottom = tk.Frame(self.root)
        bottom.pack(pady=5)
        self.status_label = tk.Label(bottom, text="", font=("Arial", 12))
        self.status_label.pack(side=tk.LEFT, padx=10)
        self.restart_button = tk.Button(bottom, text="New Game",
                                        command=self._restart)
        self.restart_button.pack(side=tk.LEFT, padx=10)
    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def _bind_events(self):
        '''Bind left mouse clicks on the canvas to the move handler.'''
        self.canvas.bind("<Button-1>", self._on_click)
    def _on_click(self, event):
        '''Convert a canvas click into a board move and refresh the view.'''
        if self.game.is_game_over():
            return
        col = (event.x - PADDING) // CELL_SIZE
        row = (event.y - PADDING) // CELL_SIZE
        if 0 <= row < 8 and 0 <= col < 8:
            if self.game.make_move(row, col):
                self.refresh()
                if self.game.is_game_over():
                    self._show_game_over()
    def _restart(self):
        '''Start a brand-new match and redraw the interface.'''
        self.game = Game()
        self.refresh()
    def _show_game_over(self):
        '''Pop up a dialog announcing the final result.'''
        black, white = self.game.get_score()
        if self.game.winner is None:
            message = "It's a tie!  (Black %d - %d White)" % (black, white)
        else:
            message = "%s wins!  (Black %d - %d White)" % (
                PLAYER_NAMES[self.game.winner], black, white)
        messagebox.showinfo("Game Over", message)
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def refresh(self):
        '''Redraw the board, discs, valid-move hints, scores and status.'''
        self.canvas.delete("all")
        # 1) Grid cells and discs.
        for row in range(8):
            for col in range(8):
                x1 = PADDING + col * CELL_SIZE
                y1 = PADDING + row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green",
                                             outline="dark green", width=2)
                disc = self.game.board.get_disc(row, col)
                if disc != EMPTY:
                    cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
                    radius = CELL_SIZE / 2.0 - 6
                    self.canvas.create_oval(cx - radius, cy - radius,
                                            cx + radius, cy + radius,
                                            fill=COLORS[disc],
                                            outline="grey", width=1)
        # 2) Valid-move hints (small dots in the current player's colour).
        if not self.game.is_game_over():
            hint_color = COLORS[self.game.current_player]
            for row, col in self.game.get_valid_moves():
                cx = PADDING + col * CELL_SIZE + CELL_SIZE / 2.0
                cy = PADDING + row * CELL_SIZE + CELL_SIZE / 2.0
                radius = 6
                self.canvas.create_oval(cx - radius, cy - radius,
                                        cx + radius, cy + radius,
                                        fill=hint_color, outline="")
        # 3) Score panel, turn indicator and status message.
        black, white = self.game.get_score()
        self.black_score_label.config(text="Black: %d" % black)
        self.white_score_label.config(text="White: %d" % white)
        if self.game.is_game_over():
            self.turn_label.config(text="Game Over")
            if self.game.winner is None:
                self.status_label.config(text="It's a tie!")
            else:
                self.status_label.config(
                    text="%s wins!" % PLAYER_NAMES[self.game.winner])
        else:
            self.turn_label.config(
                text="Turn: %s" % PLAYER_NAMES[self.game.current_player])
            if self.game.passed_player is not None:
                self.status_label.config(
                    text="%s had no valid move and passed!"
                         % PLAYER_NAMES[self.game.passed_player])
            else:
                self.status_label.config(
                    text="Click a highlighted square to place your disc.")