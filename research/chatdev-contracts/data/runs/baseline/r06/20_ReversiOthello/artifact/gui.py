'''
gui.py
Tkinter front-end for Reversi (Othello).
The Gui class owns the Tkinter window: it renders the 8x8 board,
highlights the legal moves for the player on turn, shows the live
score and status messages, and forwards board clicks and the
"New Game" button to the Game object.  It implements the full
interface expected by Game:
    bind_game, run, draw_board, update_score, show_message, announce.
'''
import tkinter as tk
import tkinter.messagebox as messagebox
from board import Board
COLORS = {
    "bg": "#0b6623",
    "line": "#04531b",
    "header_bg": "#1f2a36",
    "header_fg": "#ffffff",
    "message_bg": "#e8e8e8",
    "black": "#111111",
    "white": "#f5f5f5",
    "hint": "#7adf7a",
}
CELL = 64
MARGIN = 24
class Gui:
    """Tkinter window that renders the board and forwards clicks to Game."""
    def __init__(self):
        """Build the window, board canvas, score bar and message area."""
        self.game = None
        self.root = tk.Tk()
        self.root.title("Reversi (Othello)")
        self.root.resizable(False, False)
        # Header bar with title and restart button.
        top = tk.Frame(self.root, bg=COLORS["header_bg"])
        top.pack(fill=tk.BOTH)
        self.header = tk.Label(
            top, text="Reversi (Othello)",
            font=("Helvetica", 14, "bold"),
            bg=COLORS["header_bg"], fg=COLORS["header_fg"],
        )
        self.header.pack(side=tk.LEFT, padx=10, pady=8)
        self.restart_button = tk.Button(
            top, text="New Game", command=self.on_restart,
        )
        self.restart_button.pack(side=tk.RIGHT, padx=10, pady=8)
        # Live score / turn indicator.
        self.score_label = tk.Label(self.root, font=("Helvetica", 12))
        self.score_label.pack(fill=tk.BOTH, pady=4)
        # Board canvas.
        size = MARGIN * 2 + CELL * Board.BOARD_SIZE
        self.canvas = tk.Canvas(
            self.root, width=size, height=size,
            bg=COLORS["bg"], highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        # Status message area.
        self.message_label = tk.Label(
            self.root, font=("Helvetica", 11),
            bg=COLORS["message_bg"], wraplength=size, justify="left",
        )
        self.message_label.pack(fill=tk.BOTH, ipady=4)
    # ------------------------------------------------------------------
    # Wiring
    # ------------------------------------------------------------------
    def bind_game(self, game):
        """Attach the Game object that receives clicks and restarts."""
        self.game = game
    def run(self):
        """Start the Tkinter event loop."""
        self.root.mainloop()
    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def on_click(self, event):
        """Translate a canvas click into a board cell and forward it."""
        if self.game is None:
            return
        col = (event.x - MARGIN) // CELL
        row = (event.y - MARGIN) // CELL
        if 0 <= row < Board.BOARD_SIZE and 0 <= col < Board.BOARD_SIZE:
            self.game.handle_click(row, col)
    def on_restart(self):
        """Forward the 'New Game' button press to Game.reset()."""
        if self.game is not None:
            self.game.reset()
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw_board(self, board, valid_moves):
        """Repaint the grid, discs and legal-move hints."""
        self.canvas.delete(tk.ALL)
        for r in range(Board.BOARD_SIZE):
            for c in range(Board.BOARD_SIZE):
                x0 = MARGIN + c * CELL
                y0 = MARGIN + r * CELL
                self.canvas.create_rectangle(
                    x0, y0, x0 + CELL, y0 + CELL,
                    outline=COLORS["line"], width=2,
                )
                disc = board.get_disc(r, c)
                if disc in (Board.BLACK, Board.WHITE):
                    color = COLORS["black" if disc == Board.BLACK else "white"]
                    self.canvas.create_oval(
                        x0 + 8, y0 + 8, x0 + CELL - 8, y0 + CELL - 8,
                        fill=color, outline="#666666",
                    )
                elif (r, c) in valid_moves:
                    self.canvas.create_oval(
                        x0 + CELL // 2 - 6, y0 + CELL // 2 - 6,
                        x0 + CELL // 2 + 6, y0 + CELL // 2 + 6,
                        fill=COLORS["hint"], outline="",
                    )
    def update_score(self, black, white, current_player):
        """Show the live score and, during play, whose turn it is."""
        turn = ""
        if current_player is not None:
            turn = (f"   —   {current_player.name}'s turn "
                    f"({current_player.color_name})")
        self.score_label.config(text=f"Black {black}  :  {white} White{turn}")
    def show_message(self, text):
        """Display a status message under the board."""
        self.message_label.config(text=text)
    def announce(self, text):
        """Pop up a dialog announcing the final result."""
        messagebox.showinfo("Reversi — Game Over", text, parent=self.root)