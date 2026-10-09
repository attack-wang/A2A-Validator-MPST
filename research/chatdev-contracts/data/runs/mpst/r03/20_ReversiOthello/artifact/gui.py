'''
gui.py
Tkinter front-end for Reversi (Othello). Renders the 8x8 board, highlights
valid moves, handles mouse clicks, shows live scores/status, and provides
a "New Game" restart button.
'''
import tkinter as tk
from tkinter import messagebox
from board import Board
from game import Game
class ReversiGUI:
    CELL_SIZE = 64
    MARGIN = 40
    BG_COLOR = "#0b6e4f"
    LINE_COLOR = "#053d26"
    HINT_COLOR = "#ffd54a"
    LAST_MOVE_COLOR = "#ff8c42"
    TEXT_COLOR = "#e8f5ee"
    PANEL_BG = "#123d2b"
    DISC_COLORS = {Board.BLACK: "#111111", Board.WHITE: "#f5f5f5"}
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.last_move = None
        self.last_flips = []
        self.board_px = self.CELL_SIZE * Board.SIZE
        self.canvas_px = self.board_px + 2 * self.MARGIN
        root.title("Reversi (Othello)")
        root.resizable(False, False)
        self._build_widgets()
        self.redraw()
    def _build_widgets(self):
        """Create the score bar, board canvas, status label and restart button."""
        score_frame = tk.Frame(self.root, bg=self.PANEL_BG, padx=10, pady=8)
        score_frame.pack(fill=tk.X)
        self.black_label = tk.Label(score_frame, text="", font=("Helvetica", 14, "bold"),
                                    fg="white", bg=self.PANEL_BG)
        self.black_label.pack(side=tk.LEFT, expand=True)
        self.white_label = tk.Label(score_frame, text="", font=("Helvetica", 14, "bold"),
                                    fg="white", bg=self.PANEL_BG)
        self.white_label.pack(side=tk.RIGHT, expand=True)
        self.canvas = tk.Canvas(self.root, width=self.canvas_px, height=self.canvas_px,
                                bg=self.BG_COLOR, highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 12),
                                     fg=self.TEXT_COLOR, anchor="w")
        self.status_label.pack(fill=tk.X, padx=12)
        tk.Button(self.root, text="New Game", font=("Helvetica", 12, "bold"),
                  command=self.restart).pack(pady=8)
        self.canvas.bind("<Button-1>", self.on_click)
    # ---------- coordinate helpers ----------
    def cell_top_left(self, row, col):
        """Pixel coordinates of a cell's top-left corner."""
        return self.MARGIN + col * self.CELL_SIZE, self.MARGIN + row * self.CELL_SIZE
    def cell_center(self, row, col):
        """Pixel coordinates of a cell's centre."""
        x, y = self.cell_top_left(row, col)
        return x + self.CELL_SIZE // 2, y + self.CELL_SIZE // 2
    def _cell_from_event(self, event):
        """Convert a mouse event to a (row, col) board position, or None."""
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        row = (event.y - self.MARGIN) // self.CELL_SIZE
        if 0 <= row < Board.SIZE and 0 <= col < Board.SIZE:
            return int(row), int(col)
        return None
    # ---------- drawing ----------
    def redraw(self):
        """Redraw the entire board, hints, scores and status message."""
        self.canvas.delete("all")
        self._draw_board()
        self._draw_discs()
        self._draw_move_hints()
        self._draw_last_move()
        self._update_score_bar()
        self._update_status()
    def _draw_board(self):
        """Draw grid lines, star points and A–H / 1–8 coordinate labels."""
        for i in range(Board.SIZE + 1):
            x = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(x, self.MARGIN, x, self.MARGIN + self.board_px, fill=self.LINE_COLOR)
            y = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(self.MARGIN, y, self.MARGIN + self.board_px, y, fill=self.LINE_COLOR)
        for r, c in [(2, 2), (2, 6), (6, 2), (6, 6)]:
            cx, cy = self.cell_center(r, c)
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3,
                                    fill=self.LINE_COLOR, outline=self.LINE_COLOR)
        for col in range(Board.SIZE):
            x, _ = self.cell_top_left(0, col)
            self.canvas.create_text(x + self.CELL_SIZE // 2, self.MARGIN - 20,
                                    text=chr(ord('A') + col), fill=self.TEXT_COLOR,
                                    font=("Helvetica", 10, "bold"))
        for row in range(Board.SIZE):
            _, y = self.cell_top_left(row, 0)
            self.canvas.create_text(self.MARGIN - 20, y + self.CELL_SIZE // 2,
                                    text=str(row + 1), fill=self.TEXT_COLOR,
                                    font=("Helvetica", 10, "bold"))
    def _draw_discs(self):
        """Draw every black/white disc currently on the board."""
        radius = self.CELL_SIZE // 2 - 6
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                disc = self.game.board.get_disc(row, col)
                if disc in (Board.BLACK, Board.WHITE):
                    cx, cy = self.cell_center(row, col)
                    self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                                            fill=self.DISC_COLORS[disc],
                                            outline="#555555" if disc == Board.BLACK else "#888888")
    def _draw_move_hints(self):
        """Mark every legal move for the current player with a yellow dot."""
        if self.game.game_over:
            return
        for row, col in self.game.valid_moves():
            cx, cy = self.cell_center(row, col)
            r = 7
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                    fill=self.HINT_COLOR, outline=self.HINT_COLOR)
    def _draw_last_move(self):
        """Outline the most recently placed disc."""
        if self.last_move:
            row, col = self.last_move
            x, y = self.cell_top_left(row, col)
            self.canvas.create_rectangle(x, y, x + self.CELL_SIZE, y + self.CELL_SIZE,
                                         outline=self.LAST_MOVE_COLOR, width=3)
    def _update_score_bar(self):
        """Refresh the live black/white disc counts."""
        scores = self.game.scores()
        self.black_label.config(text=f"● Black: {scores['Black']}")
        self.white_label.config(text=f"White: {scores['White']} ○")
    def _update_status(self):
        """Show the turn message, or the final result when the game ends."""
        if self.game.game_over:
            s = self.game.scores()
            if s["Black"] > s["White"]:
                result = f"Black wins {s['Black']}–{s['White']}!"
            elif s["White"] > s["Black"]:
                result = f"White wins {s['White']}–{s['Black']}!"
            else:
                result = f"It's a draw, {s['Black']}–{s['White']}!"
            self.status_label.config(text=f"Game over. {result}", fg=self.TEXT_COLOR)
        else:
            self.status_label.config(text=self.game.status_message, fg=self.TEXT_COLOR)
    # ---------- interaction ----------
    def on_click(self, event):
        """Handle a board click: attempt the move, redraw, or flash invalid."""
        cell = self._cell_from_event(event)
        if cell is None or self.game.game_over:
            return
        row, col = cell
        flipped = self.game.make_move(row, col)
        if flipped is None:
            self._flash_invalid()
            return
        self.last_move = (row, col)
        self.last_flips = flipped
        self.redraw()
        if self.game.game_over:
            self._show_game_over()
    def _flash_invalid(self):
        """Temporarily show an error message for an illegal click."""
        self.status_label.config(text="Invalid move! Please click one of the highlighted squares.",
                                 fg="#b3202e")
        self.root.after(1600, self._restore_status)
    def _restore_status(self):
        """Restore the normal status message after an invalid-move flash."""
        self.status_label.config(text=self.game.status_message, fg=self.TEXT_COLOR)
    def _show_game_over(self):
        """Pop up a dialog announcing the final result."""
        s = self.game.scores()
        if s["Black"] > s["White"]:
            msg = f"Black wins {s['Black']}–{s['White']}!"
        elif s["White"] > s["Black"]:
            msg = f"White wins {s['White']}–{s['Black']}!"
        else:
            msg = f"It's a draw, {s['Black']}–{s['White']}!"
        messagebox.showinfo("Game Over", msg)
    def restart(self):
        """Start a fresh match and clear highlights."""
        self.game.restart()
        self.last_move = None
        self.last_flips = []
        self.redraw()