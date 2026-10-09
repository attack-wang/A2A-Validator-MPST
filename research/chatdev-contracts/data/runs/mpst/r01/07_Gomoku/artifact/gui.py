'''
gui.py
Graphical user interface for the Gomoku game.
Renders a 15x15 board, handles alternating black/white player moves,
detects five-in-a-row wins in all four directions (horizontal, vertical,
and both diagonals), highlights the winning line and the most recent
move, detects draws, and supports game restarts.
'''
import tkinter as tk
from tkinter import messagebox
# Board configuration
BOARD_SIZE = 15      # Standard Gomoku board: 15x15 intersections
CELL_SIZE = 40       # Pixel distance between intersections
MARGIN = 30          # Pixel margin around the board
STONE_RADIUS = 16    # Pixel radius of a stone
# Player constants
EMPTY = 0
BLACK = 1
WHITE = 2
class GomokuGUI:
    '''Encapsulates the Tkinter window, board rendering, and game flow.'''
    def __init__(self, root):
        '''Initialize window, canvas, game state, and mouse bindings.'''
        self.root = root
        self.root.title("Gomoku - Five in a Row")
        self.root.resizable(False, False)
        # 2D grid: 0 = empty, 1 = black, 2 = white
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK  # Black moves first by convention
        self.game_over = False
        self.last_move = None        # (row, col) of the most recent stone
        self.win_line = None         # List of (row, col) positions forming the winning line
        canvas_size = MARGIN * 2 + CELL_SIZE * (BOARD_SIZE - 1)
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="#DEB887")
        self.canvas.pack()
        self.status = tk.Label(root, text="Black's turn - click an intersection to place a stone",
                               font=("Arial", 12))
        self.status.pack(pady=5)
        tk.Button(root, text="Restart Game", command=self.restart).pack(pady=5)
        self.canvas.bind("<Button-1>", self.on_click)
        self.refresh_board()
    def refresh_board(self):
        '''Redraw the grid, all placed stones, the win highlight, and the last-move marker.'''
        self.draw_board()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] != EMPTY:
                    self.draw_stone(r, c, self.board[r][c])
        if self.win_line:
            for r, c in self.win_line:
                x, y = MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE
                self.canvas.create_oval(x - STONE_RADIUS - 2, y - STONE_RADIUS - 2,
                                        x + STONE_RADIUS + 2, y + STONE_RADIUS + 2,
                                        outline="red", width=2)
        if self.last_move:
            r, c = self.last_move
            x, y = MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red", outline="red")
    def draw_board(self):
        '''Draw the 15x15 grid lines and star reference points.'''
        self.canvas.delete("all")
        end = MARGIN + CELL_SIZE * (BOARD_SIZE - 1)
        for i in range(BOARD_SIZE):
            pos = MARGIN + i * CELL_SIZE
            self.canvas.create_line(MARGIN, pos, end, pos, fill="black")
            self.canvas.create_line(pos, MARGIN, pos, end, fill="black")
        for r, c in [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]:
            x, y = MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
    def on_click(self, event):
        '''Convert a click to the nearest intersection and place a stone if valid.'''
        if self.game_over:
            return
        col = round((event.x - MARGIN) / CELL_SIZE)
        row = round((event.y - MARGIN) / CELL_SIZE)
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        if self.board[row][col] != EMPTY:
            return  # Intersection already occupied
        self.place_stone(row, col)
    def place_stone(self, row, col):
        '''Place the stone, check win/draw, switch turns, and refresh the display.'''
        self.board[row][col] = self.current_player
        self.last_move = (row, col)
        win_line = self.check_win(row, col)
        if win_line:
            self.game_over = True
            self.win_line = win_line
            winner = "Black" if self.current_player == BLACK else "White"
            self.status.config(text=f"{winner} wins! Click 'Restart Game' to play again.")
            self.refresh_board()
            messagebox.showinfo("Game Over", f"{winner} wins!")
            return
        if all(cell != EMPTY for line in self.board for cell in line):
            self.game_over = True
            self.status.config(text="It's a draw! Board is full.")
            self.refresh_board()
            messagebox.showinfo("Game Over", "It's a draw!")
            return
        self.current_player = WHITE if self.current_player == BLACK else BLACK
        name = "Black" if self.current_player == BLACK else "White"
        self.status.config(text=f"{name}'s turn")
        self.refresh_board()
    def draw_stone(self, row, col, player):
        '''Render a black or white stone centered on the intersection.'''
        x, y = MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE
        if player == BLACK:
            self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                    x + STONE_RADIUS, y + STONE_RADIUS,
                                    fill="black", outline="black")
            # Subtle highlight for a polished, three-dimensional look
            self.canvas.create_oval(x - STONE_RADIUS + 4, y - STONE_RADIUS + 4,
                                    x - 2, y - 2, fill="#4a4a4a", outline="")
        else:
            self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                    x + STONE_RADIUS, y + STONE_RADIUS,
                                    fill="white", outline="black")
    def check_win(self, row, col):
        '''Return the list of positions forming five-or-more in a row through (row, col), else None.'''
        player = self.board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, both diagonals
        for dr, dc in directions:
            positions = [(row, col)]
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                positions.append((r, c))
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                positions.append((r, c))
                r -= dr
                c -= dc
            if len(positions) >= 5:
                return positions
        return None
    def restart(self):
        '''Reset board and state for a fresh match.'''
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK
        self.game_over = False
        self.last_move = None
        self.win_line = None
        self.refresh_board()
        self.status.config(text="Black's turn - click an intersection to place a stone")
def launch_gui():
    '''Create the root window, start the game, and enter the Tkinter main loop.'''
    root = tk.Tk()
    GomokuGUI(root)
    root.mainloop()