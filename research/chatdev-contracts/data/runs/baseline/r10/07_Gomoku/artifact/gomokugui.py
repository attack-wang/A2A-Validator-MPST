import tkinter as tk
from board import Board, EMPTY, BLACK, WHITE, PLAYER_NAMES
from game import GomokuGame
class GomokuGUI:
    CELL_SIZE = 36
    MARGIN = 40
    STONE_RADIUS = 14
    def __init__(self, root):
        self.root = root
        self.game = GomokuGame()
        self.root.title("Gomoku - Five in a Row")
        self.root.resizable(False, False)
        board_pixels = self.MARGIN * 2 + self.CELL_SIZE * (Board.SIZE - 1)
        # Status bar
        self.status_var = tk.StringVar(value="Black's turn - click a intersection to place a stone")
        status_label = tk.Label(root, textvariable=self.status_var, font=("Arial", 12))
        status_label.pack(pady=5)
        # Canvas
        self.canvas = tk.Canvas(root, width=board_pixels, height=board_pixels, bg="#DCB35C")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        # Buttons frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        new_button = tk.Button(button_frame, text="New Game", command=self.new_game)
        new_button.pack(side=tk.LEFT, padx=5)
        undo_button = tk.Button(button_frame, text="Undo", command=self.undo)
        undo_button.pack(side=tk.LEFT, padx=5)
        quit_button = tk.Button(button_frame, text="Quit", command=root.destroy)
        quit_button.pack(side=tk.LEFT, padx=5)
        self.draw_board()
    def draw_board(self):
        self.canvas.delete("all")
        size = self.game.board.size
        # grid lines
        for i in range(size):
            x = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(x, self.MARGIN, x, self.MARGIN + (size - 1) * self.CELL_SIZE, fill="black")
            y = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(self.MARGIN, y, self.MARGIN + (size - 1) * self.CELL_SIZE, y, fill="black")
        # star points (hoshi) at traditional positions for 15x15: (3,3), (3,11), (11,3), (11,11), (7,7)
        for r, c in [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]:
            x = self.MARGIN + c * self.CELL_SIZE
            y = self.MARGIN + r * self.CELL_SIZE
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
        # coordinate labels
        for i in range(size):
            x = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_text(x, self.MARGIN - 22, text=chr(ord('A') + i), font=("Arial", 9))
            y = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_text(self.MARGIN - 24, y, text=str(i + 1), font=("Arial", 9))
        # stones
        for r in range(size):
            for c in range(size):
                stone = self.game.board.get_stone(r, c)
                if stone != EMPTY:
                    self.draw_stone(r, c, stone)
        # highlight last move
        if self.game.last_move and not self.game.game_over:
            r, c = self.game.last_move
            x = self.MARGIN + c * self.CELL_SIZE
            y = self.MARGIN + r * self.CELL_SIZE
            color = "white" if self.game.board.get_stone(r, c) == BLACK else "black"
            self.canvas.create_rectangle(x - 3, y - 3, x + 3, y + 3, outline=color, width=2)
        # highlight winning line
        if self.game.game_over and self.game.winner is not None:
            for (r, c) in self.game.winning_line:
                x = self.MARGIN + c * self.CELL_SIZE
                y = self.MARGIN + r * self.CELL_SIZE
                self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, outline="red", width=2)
    def draw_stone(self, row, col, player):
        x = self.MARGIN + col * self.CELL_SIZE
        y = self.MARGIN + row * self.CELL_SIZE
        fill = "black" if player == BLACK else "white"
        outline = "black"
        self.canvas.create_oval(x - self.STONE_RADIUS, y - self.STONE_RADIUS,
                                x + self.STONE_RADIUS, y + self.STONE_RADIUS,
                                fill=fill, outline=outline, width=1)
    def on_click(self, event):
        if self.game.game_over:
            return
        col = round((event.x - self.MARGIN) / self.CELL_SIZE)
        row = round((event.y - self.MARGIN) / self.CELL_SIZE)
        if not self.game.board.is_valid_position(row, col):
            return
        if not self.game.play_move(row, col):
            return  # occupied
        self.draw_board()
        self.update_status()
    def update_status(self):
        if self.game.game_over:
            if self.game.winner is not None:
                self.status_var.set(f"{PLAYER_NAMES[self.game.winner]} wins! Click 'New Game' to play again.")
            else:
                self.status_var.set("Draw! The board is full. Click 'New Game' to play again.")
        else:
            self.status_var.set(f"{PLAYER_NAMES[self.game.current_player]}'s turn")
    def new_game(self):
        self.game.reset()
        self.draw_board()
        self.update_status()
    def undo(self):
        if self.game.undo_move():
            self.draw_board()
            self.update_status()