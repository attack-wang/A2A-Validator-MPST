'''
gui.py
Graphical user interface for the tic-tac-toe game, built with tkinter
(part of the Python standard library). Provides a clickable 3x3 grid,
turn indicators, score tracking, win highlighting, and round management.
'''
import tkinter as tk
from tkinter import messagebox, simpledialog
from game import Game
CELL_FONT = ("Helvetica", 32, "bold")
LABEL_FONT = ("Helvetica", 13)
STATUS_FONT = ("Helvetica", 14, "bold")
BUTTON_FONT = ("Helvetica", 11)
X_COLOR = "#1f6fb2"    # blue for X marks
O_COLOR = "#d1495b"    # red for O marks
WIN_COLOR = "#b7e4c7"  # highlight for winning cells
BG_COLOR = "#f0f4f8"
class TicTacToeGUI:
    """Tkinter window that renders the board and drives the Game controller."""
    def __init__(self, root, player1_name="Player 1", player2_name="Player 2"):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.game = Game(player1_name, player2_name)
        self.cells = []
        self._build_widgets()
        self._refresh()
    # ------------------------------------------------------------------ UI setup
    def _build_widgets(self):
        """Create and lay out every widget in the main window."""
        self.root.configure(bg=BG_COLOR)
        self.status_label = tk.Label(
            self.root, text="", font=STATUS_FONT, bg=BG_COLOR, fg="#222222", pady=8
        )
        self.status_label.grid(row=0, column=0, columnspan=3, sticky="ew")
        for r in range(3):
            row_buttons = []
            for c in range(3):
                button = tk.Button(
                    self.root,
                    text=" ",
                    width=4,
                    height=2,
                    font=CELL_FONT,
                    bg="white",
                    activebackground="#e2e8f0",
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda r=r, c=c: self._on_cell_click(r, c),
                )
                button.grid(row=r + 1, column=c, padx=6, pady=6)
                row_buttons.append(button)
            self.cells.append(row_buttons)
        self.score_label = tk.Label(
            self.root, text="", font=LABEL_FONT, bg=BG_COLOR, fg="#444444", pady=6
        )
        self.score_label.grid(row=4, column=0, columnspan=3, sticky="ew")
        controls = tk.Frame(self.root, bg=BG_COLOR)
        controls.grid(row=5, column=0, columnspan=3, pady=(0, 12))
        self.new_round_button = tk.Button(
            controls, text="New Round", font=BUTTON_FONT,
            bg="#4c9f70", fg="white", activebackground="#3d8259",
            activeforeground="white", relief=tk.FLAT, padx=12, pady=4,
            command=self._on_new_round,
        )
        self.new_round_button.pack(side=tk.LEFT, padx=6)
        self.reset_scores_button = tk.Button(
            controls, text="Reset Scores", font=BUTTON_FONT,
            bg="#8d99ae", fg="white", activebackground="#6c7689",
            activeforeground="white", relief=tk.FLAT, padx=12, pady=4,
            command=self._on_reset_scores,
        )
        self.reset_scores_button.pack(side=tk.LEFT, padx=6)
    # ------------------------------------------------------------------ event handlers
    def _on_cell_click(self, row, col):
        """Handle a click on board cell (row, col)."""
        if self.game.make_move(row, col):
            self._refresh()
            if self.game.game_over:
                self._announce_result()
    def _on_new_round(self):
        """Start a fresh round, keeping the running score."""
        self.game.reset()
        self._refresh()
    def _on_reset_scores(self):
        """Zero both players' win counters."""
        for player in self.game.players:
            player.wins = 0
        self._refresh()
    # ------------------------------------------------------------------ rendering
    def _refresh(self):
        """Synchronize every widget with the current game state."""
        winning_cells = set(self.game.winning_line or [])
        for r in range(3):
            for c in range(3):
                symbol = self.game.board.grid[r][c]
                playable = symbol == " " and not self.game.game_over
                if (r, c) in winning_cells:
                    background = WIN_COLOR
                else:
                    background = "white"
                if symbol == "X":
                    foreground = X_COLOR
                elif symbol == "O":
                    foreground = O_COLOR
                else:
                    foreground = "#333333"
                self.cells[r][c].config(
                    text=symbol,
                    state=tk.NORMAL if playable else tk.DISABLED,
                    bg=background,
                    fg=foreground,
                )
        self.status_label.config(text=self.game.get_status())
        self.score_label.config(text=self.game.get_score_text())
    def _announce_result(self):
        """Show a pop-up describing the round outcome."""
        if self.game.winner is not None:
            message = f"{self.game.winner.name} ({self.game.winner.symbol}) wins this round!"
        else:
            message = "The board is full — it's a draw!"
        messagebox.showinfo("Round Over", message, parent=self.root)
def _ask_player_name(default_name, symbol):
    """Ask for a player's name, falling back to the default on cancel/blank."""
    name = simpledialog.askstring(
        "Player Registration",
        f"{default_name}, please enter your name.\n(You will play as '{symbol}')",
        initialvalue=default_name,
    )
    if name is None or not name.strip():
        return default_name
    return name.strip()[:20]
def launch():
    """Create the application window and start the tkinter event loop."""
    root = tk.Tk()
    root.withdraw()  # hide the empty window while gathering player names
    name1 = _ask_player_name("Player 1", "X")
    name2 = _ask_player_name("Player 2", "O")
    root.deiconify()
    TicTacToeGUI(root, name1, name2)
    root.mainloop()