'''
gui.py
Tkinter-based graphical interface for the Gomoku game.
This module renders the 15x15 board, converts mouse clicks into board
moves, alternates turns between Black and White, detects and highlights
the winning line, and provides New Game / Undo controls.
'''
import tkinter as tk
from board import Board
class GomokuGUI:
    """Main application window for the Gomoku game."""
    CELL_SIZE = 36      # pixels between two adjacent grid intersections
    STONE_RADIUS = 15   # radius of a drawn stone
    MARGIN = 30         # padding around the playing grid
    def __init__(self, root):
        """Build the window layout and initialise a fresh game."""
        self.root = root
        self.root.title("Gomoku - Five in a Row")
        self.root.resizable(False, False)
        self.board = Board(15)
        self.move_history = []   # list of (row, col, player) tuples
        self.game_over = False
        board_px = self.MARGIN * 2 + self.CELL_SIZE * (self.board.size - 1)
        # Status bar: shows whose turn it is or the final result.
        self.status_var = tk.StringVar(
            value="Black's turn - click an intersection to place a stone"
        )
        tk.Label(
            self.root, textvariable=self.status_var,
            font=("Helvetica", 12, "bold"), pady=6
        ).pack()
        # Canvas that renders the board.
        self.canvas = tk.Canvas(
            self.root, width=board_px, height=board_px,
            bg="#DCB35C", highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        # Control buttons.
        button_frame = tk.Frame(self.root, pady=6)
        button_frame.pack()
        tk.Button(
            button_frame, text="New Game", width=12, command=self.reset_game
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            button_frame, text="Undo", width=12, command=self.undo
        ).pack(side=tk.LEFT, padx=5)
        self.draw_board()
    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw_board(self):
        """Redraw the entire board: grid, star points, labels and stones."""
        self.canvas.delete("all")
        size = self.board.size
        grid_end = self.MARGIN + (size - 1) * self.CELL_SIZE
        # Grid lines.
        for i in range(size):
            pos = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(pos, self.MARGIN, pos, grid_end, fill="#000000")
            self.canvas.create_line(self.MARGIN, pos, grid_end, pos, fill="#000000")
        # Outer border for emphasis.
        self.canvas.create_rectangle(
            self.MARGIN - 1, self.MARGIN - 1,
            grid_end + 1, grid_end + 1,
            outline="#000000", width=2
        )
        # Traditional star points of a 15x15 board.
        for r, c in [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]:
            cx = self.MARGIN + c * self.CELL_SIZE
            cy = self.MARGIN + r * self.CELL_SIZE
            self.canvas.create_oval(
                cx - 3, cy - 3, cx + 3, cy + 3,
                fill="#000000", outline="#000000"
            )
        # Coordinate labels: A-O across the top, 1-15 down the left.
        for i in range(size):
            pos = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_text(
                pos, self.MARGIN - 16, text=chr(ord("A") + i),
                font=("Helvetica", 9)
            )
            self.canvas.create_text(
                self.MARGIN - 16, pos, text=str(i + 1),
                font=("Helvetica", 9)
            )
        # Stones.
        for r in range(size):
            for c in range(size):
                player = self.board.grid[r][c]
                if player != Board.EMPTY:
                    self.draw_stone(r, c, player)
        # Marker on the most recent move.
        if self.board.last_move:
            r, c = self.board.last_move
            cx = self.MARGIN + c * self.CELL_SIZE
            cy = self.MARGIN + r * self.CELL_SIZE
            self.canvas.create_rectangle(
                cx - 4, cy - 4, cx + 4, cy + 4,
                outline="#FF0000", width=2
            )
        # Ring around every stone of the winning line.
        for r, c in self.board.winning_line:
            cx = self.MARGIN + c * self.CELL_SIZE
            cy = self.MARGIN + r * self.CELL_SIZE
            self.canvas.create_oval(
                cx - self.STONE_RADIUS - 3, cy - self.STONE_RADIUS - 3,
                cx + self.STONE_RADIUS + 3, cy + self.STONE_RADIUS + 3,
                outline="#FF4500", width=3
            )
    def draw_stone(self, row, col, player):
        """Draw a single black or white stone at board cell (row, col)."""
        cx = self.MARGIN + col * self.CELL_SIZE
        cy = self.MARGIN + row * self.CELL_SIZE
        r = self.STONE_RADIUS
        fill = "#000000" if player == Board.BLACK else "#FFFFFF"
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=fill, outline="#000000", width=1
        )
    # ------------------------------------------------------------------
    # Game flow
    # ------------------------------------------------------------------
    def on_click(self, event):
        """Translate a canvas click into a board move and play it."""
        if self.game_over:
            return
        col = round((event.x - self.MARGIN) / self.CELL_SIZE)
        row = round((event.y - self.MARGIN) / self.CELL_SIZE)
        if not (0 <= row < self.board.size and 0 <= col < self.board.size):
            return
        player = self.board.current_player
        success, winner, winning_line = self.board.place_stone(row, col)
        if not success:
            return
        self.move_history.append((row, col, player))
        # Redraw exactly once per move. The winning line (if any) is
        # already stored on the board by check_win(), so a single
        # redraw covers stones, last-move marker and win highlight.
        self.draw_board()
        if winner in (Board.BLACK, Board.WHITE):
            self.game_over = True
            self.status_var.set(
                "{} wins! Press 'New Game' to play again.".format(
                    self.board.player_name(winner)
                )
            )
            return
        if self.board.is_full():
            self.game_over = True
            self.status_var.set("It's a draw! Press 'New Game' to play again.")
            return
        self.status_var.set(
            "{}'s turn - click an intersection to place a stone".format(
                self.board.player_name(self.board.current_player)
            )
        )
    def reset_game(self):
        """Start a brand new game."""
        self.board.reset()
        self.move_history = []
        self.game_over = False
        self.status_var.set(
            "Black's turn - click an intersection to place a stone"
        )
        self.draw_board()
    def undo(self):
        """Undo the most recent move, even one that ended the game."""
        if not self.move_history:
            return
        row, col, player = self.move_history.pop()
        self.board.grid[row][col] = Board.EMPTY
        self.board.current_player = player
        self.board.last_move = self.move_history[-1][:2] if self.move_history else None
        self.board.winning_line = []
        self.game_over = False
        self.draw_board()
        self.status_var.set(
            "{}'s turn - click an intersection to place a stone".format(
                self.board.player_name(self.board.current_player)
            )
        )