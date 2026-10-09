'''
gui.py
Graphical user interface module containing the GomokuGUI class.
Built with tkinter, this module renders the 15x15 Gomoku board,
draws black/white stones, converts mouse clicks into board
coordinates, shows the current turn / result in a status bar, and
provides Restart and Undo controls. It also highlights the winning
line and marks the most recent move.
'''
import tkinter as tk
from config import (CELL_SIZE, MARGIN, STONE_RADIUS, BOARD_PIXELS,
                    BOARD_COLOR, GRID_LINE_COLOR, BLACK_STONE_COLOR,
                    WHITE_STONE_COLOR, HIGHLIGHT_COLOR, STATUS_BG_COLOR,
                    TEXT_COLOR, WINDOW_TITLE, STATUS_FONT, BUTTON_FONT,
                    EMPTY, PLAYER_BLACK, PLAYER_WHITE)
class GomokuGUI:
    """Tkinter-based graphical interface for the Gomoku game."""
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        self._build_status_bar()
        self._build_canvas()
        self._build_controls()
        self.redraw()
        # Keyboard shortcut: Ctrl+Z for undo
        self.root.bind("<Control-z>", lambda event: self.undo())
        self._center_window()
    def _build_status_bar(self):
        """Create the status label showing turn info and results."""
        self.status_label = tk.Label(self.root, text="", font=STATUS_FONT,
                                     bg=STATUS_BG_COLOR, fg=TEXT_COLOR,
                                     anchor="w", padx=10)
        self.status_label.pack(side=tk.TOP, fill=tk.X)
    def _build_canvas(self):
        """Create the board canvas and bind mouse clicks."""
        self.canvas = tk.Canvas(self.root, width=BOARD_PIXELS,
                                height=BOARD_PIXELS, bg=BOARD_COLOR,
                                highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_canvas_click)
    def _draw_grid(self):
        """Draw the 15x15 grid lines on the canvas."""
        size = self.game.board_size
        end = MARGIN + (size - 1) * CELL_SIZE
        for i in range(size):
            pos = MARGIN + i * CELL_SIZE
            self.canvas.create_line(MARGIN, pos, end, pos, fill=GRID_LINE_COLOR)
            self.canvas.create_line(pos, MARGIN, pos, end, fill=GRID_LINE_COLOR)
    def _build_controls(self):
        """Create Restart and Undo buttons."""
        frame = tk.Frame(self.root)
        frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(frame, text="Undo", font=BUTTON_FONT,
                  command=self.undo).pack(side=tk.RIGHT, padx=10, pady=5)
        tk.Button(frame, text="Restart", font=BUTTON_FONT,
                  command=self.restart).pack(side=tk.RIGHT, padx=10, pady=5)
    def _on_canvas_click(self, event):
        """Convert a mouse click to the nearest intersection and play it."""
        if self.game.is_game_over():
            return
        col = round((event.x - MARGIN) / CELL_SIZE)
        row = round((event.y - MARGIN) / CELL_SIZE)
        size = self.game.board_size
        if 0 <= row < size and 0 <= col < size:
            if self.game.make_move(row, col):
                self.redraw()
    def redraw(self):
        """Redraw stones, last-move marker, winning highlight, and status."""
        self.canvas.delete("all")
        self._draw_grid()
        size = self.game.board_size
        winning = set(self.game.get_winning_line())
        last = (self.game.move_history[-1][:2]
                if self.game.get_move_count() > 0 else None)
        for row in range(size):
            for col in range(size):
                stone = self.game.board.get_stone(row, col)
                if stone == EMPTY:
                    continue
                x = MARGIN + col * CELL_SIZE
                y = MARGIN + row * CELL_SIZE
                fill = BLACK_STONE_COLOR if stone == PLAYER_BLACK else WHITE_STONE_COLOR
                outline = WHITE_STONE_COLOR if stone == PLAYER_BLACK else BLACK_STONE_COLOR
                self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                        x + STONE_RADIUS, y + STONE_RADIUS,
                                        fill=fill, outline=outline)
                if (row, col) in winning:
                    self.canvas.create_oval(x - STONE_RADIUS - 3, y - STONE_RADIUS - 3,
                                            x + STONE_RADIUS + 3, y + STONE_RADIUS + 3,
                                            outline=HIGHLIGHT_COLOR, width=2)
                elif last == (row, col):
                    self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4,
                                            fill=HIGHLIGHT_COLOR, outline="")
        self._update_status()
    def _update_status(self):
        """Refresh the status bar text based on game state."""
        if self.game.is_game_over():
            winner = self.game.get_winner()
            if winner == PLAYER_BLACK:
                text = "Game over - Black wins! Click Restart to play again."
            elif winner == PLAYER_WHITE:
                text = "Game over - White wins! Click Restart to play again."
            else:
                text = "Game over - It's a draw! Click Restart to play again."
        else:
            name = "Black" if self.game.get_current_player() == PLAYER_BLACK else "White"
            text = f"Turn: {name}   |   Moves: {self.game.get_move_count()}"
        self.status_label.config(text=text)
    def undo(self):
        """Undo the last move and refresh the display."""
        if self.game.undo_move():
            self.redraw()
    def restart(self):
        """Start a new game and refresh the display."""
        self.game.reset()
        self.redraw()
    def _center_window(self):
        """Center the window on the screen (recovered from lost fragment)."""
        self.root.update_idletasks()
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        x = max(0, (self.root.winfo_screenwidth() - w) // 2)
        y = max(0, (self.root.winfo_screenheight() - h) // 2)
        self.root.geometry(f"+{x}+{y}")