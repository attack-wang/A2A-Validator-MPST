'''
gui.py
Provides a Tkinter-based graphical user interface for the Gomoku game,
rendering the board, handling mouse clicks, and displaying game status.
'''
import tkinter as tk
from constants import BOARD_SIZE, EMPTY, BLACK, WHITE, STAR_POINTS
from game import Game
class GomokuGUI:
    '''Tkinter interface for playing Gomoku.'''
    CELL_SIZE = 36
    MARGIN = 30
    STONE_RADIUS = 14
    def __init__(self, game=None):
        self.game = game if game is not None else Game()
        self.root = tk.Tk()
        self.root.title('Gomoku - Five in a Row')
        self.board_px = self.MARGIN * 2 + self.CELL_SIZE * (BOARD_SIZE - 1)
        self.canvas = tk.Canvas(self.root, width=self.board_px,
                                height=self.board_px, bg='#DCB35C')
        self.canvas.pack()
        self.status = tk.Label(self.root, text='', font=('Helvetica', 14))
        self.status.pack(pady=5)
        button = tk.Button(self.root, text='New Game', command=self.new_game)
        button.pack(pady=5)
        self.canvas.bind('<Button-1>', self.on_click)
        self.stone_ids = {}
        self.draw_board()
        self.update_status()
    def run(self):
        self.root.mainloop()
    def new_game(self):
        self.game.reset()
        self.canvas.delete('all')
        self.stone_ids = {}
        self.draw_board()
        self.update_status()
    def draw_board(self):
        '''Draw grid lines and star (hoshi) points.'''
        for i in range(BOARD_SIZE):
            x = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(x, self.MARGIN, x,
                                    self.board_px - self.MARGIN, fill='black')
            y = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(self.MARGIN, y,
                                    self.board_px - self.MARGIN, y, fill='black')
        for (r, c) in STAR_POINTS:
            x = self.MARGIN + c * self.CELL_SIZE
            y = self.MARGIN + r * self.CELL_SIZE
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                                    fill='black', outline='black')
    def draw_stone(self, row, col, color):
        '''Draw a stone of the given color at the given intersection.'''
        x = self.MARGIN + col * self.CELL_SIZE
        y = self.MARGIN + row * self.CELL_SIZE
        fill = 'black' if color == BLACK else 'white'
        self.stone_ids[(row, col)] = self.canvas.create_oval(
            x - self.STONE_RADIUS, y - self.STONE_RADIUS,
            x + self.STONE_RADIUS, y + self.STONE_RADIUS,
            fill=fill, outline='black')
    def update_status(self):
        '''Refresh the status label with the current game state.'''
        if self.game.game_over:
            if self.game.winner_color is not None:
                winner = self.game.players[self.game.winner_color]
                self.status.config(text=f'{winner.name} wins! Press "New Game" to replay.')
            else:
                self.status.config(text='Draw! Press "New Game" to replay.')
        else:
            player = self.game.current_player
            self.status.config(text=f"{player.name}'s turn ({player.symbol})")
    def highlight_win(self):
        '''Outline the stones forming the winning line in red.'''
        if not self.game.winning_line:
            return
        for (r, c) in self.game.winning_line:
            x = self.MARGIN + c * self.CELL_SIZE
            y = self.MARGIN + r * self.CELL_SIZE
            self.canvas.create_oval(
                x - self.STONE_RADIUS - 2, y - self.STONE_RADIUS - 2,
                x + self.STONE_RADIUS + 2, y + self.STONE_RADIUS + 2,
                outline='red', width=2, tags='win')
    def on_click(self, event):
        if self.game.game_over:
            return
        col = round((event.x - self.MARGIN) / self.CELL_SIZE)
        row = round((event.y - self.MARGIN) / self.CELL_SIZE)
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        # tolerance check: click must be near the intersection
        x = self.MARGIN + col * self.CELL_SIZE
        y = self.MARGIN + row * self.CELL_SIZE
        if abs(event.x - x) > self.CELL_SIZE / 2 or abs(event.y - y) > self.CELL_SIZE / 2:
            return
        if not self.game.play_turn(row, col):
            return
        self.draw_stone(row, col, self.game.board.get_cell(row, col))
        self.update_status()
        if self.game.game_over:
            self.highlight_win()