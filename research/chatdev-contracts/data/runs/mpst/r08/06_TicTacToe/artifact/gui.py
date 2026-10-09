'''
gui.py
This module contains the TicTacToeGUI class, a tkinter-based graphical user
interface for the tic-tac-toe game. It renders the 3x3 grid as clickable
buttons, displays the current player's turn, highlights winning cells, shows
a detailed move-history panel, and provides a "New Game" button.
'''
import tkinter as tk
from tkinter import messagebox
from game_controller import GameController
class TicTacToeGUI:
    """Tkinter GUI for the two-player tic-tac-toe game."""
    def __init__(self, root, player_x_name="Player 1", player_o_name="Player 2"):
        """Build the main window, board buttons, status bar, and controls."""
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e2749")
        self.controller = GameController(player_x_name, player_o_name)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self._build_header()
        self._build_board()
        self._build_controls()
        self._update_status()
        self._update_history()
    def _build_header(self):
        """Create the title label and the status label."""
        title = tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#1e2749",
        )
        title.pack(pady=(15, 5))
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 14),
            fg="#ffd166",
            bg="#1e2749",
        )
        self.status_label.pack(pady=(0, 10))
    def _build_board(self):
        """Create the 3x3 grid of clickable buttons."""
        board_frame = tk.Frame(self.root, bg="#1e2749")
        board_frame.pack(padx=10, pady=5)
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    board_frame,
                    text=" ",
                    width=6,
                    height=3,
                    font=("Helvetica", 26, "bold"),
                    bg="#3b4a6b",
                    fg="white",
                    activebackground="#4a5b82",
                    relief="ridge",
                    bd=3,
                    command=lambda row=r, col=c: self.on_cell_click(row, col),
                )
                btn.grid(row=r, column=c, padx=4, pady=4)
                self.buttons[r][c] = btn
    def _build_controls(self):
        """Create the 'New Game' button and the detailed move-history panel."""
        controls_frame = tk.Frame(self.root, bg="#1e2749")
        controls_frame.pack(pady=(5, 15))
        new_game_btn = tk.Button(
            controls_frame,
            text="New Game",
            font=("Helvetica", 12, "bold"),
            bg="#ef476f",
            fg="white",
            activebackground="#ff6b8a",
            relief="flat",
            padx=15,
            pady=5,
            command=self.reset_game,
        )
        new_game_btn.pack()
        history_title = tk.Label(
            controls_frame,
            text="Move History",
            font=("Helvetica", 11, "bold"),
            fg="#a8b3d6",
            bg="#1e2749",
        )
        history_title.pack(pady=(8, 2))
        self.history_text = tk.Text(
            controls_frame,
            width=36,
            height=6,
            font=("Courier", 9),
            fg="#a8b3d6",
            bg="#141b33",
            relief="flat",
            state="disabled",
        )
        self.history_text.pack()
    def on_cell_click(self, row, col):
        """Handle a click on the cell at (row, col)."""
        result = self.controller.take_turn(row, col)
        if not result["success"]:
            messagebox.showwarning("Invalid Move", result["reason"])
            return
        self._refresh_board()
        self._update_history()
        if result["game_over"]:
            self._handle_game_over(result)
        else:
            self._update_status()
    def _refresh_board(self):
        """Sync the button labels/colors with the board state."""
        grid = self.controller.board.grid
        for r in range(3):
            for c in range(3):
                symbol = grid[r][c]
                btn = self.buttons[r][c]
                btn.config(text=symbol)
                if symbol == "X":
                    btn.config(
                        fg="#4cc9f0",
                        state="disabled" if self.controller.game_over else "normal",
                    )
                elif symbol == "O":
                    btn.config(
                        fg="#f72585",
                        state="disabled" if self.controller.game_over else "normal",
                    )
    def _update_status(self):
        """Update the status label with the current player's turn."""
        player = self.controller.get_current_player()
        self.status_label.config(
            text=f"{player.get_name()}'s turn ({player.get_symbol()})"
        )
    def _update_history(self):
        """Refresh the detailed move-history panel."""
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        history = self.controller.get_move_history()
        if not history:
            self.history_text.insert(tk.END, "No moves yet.")
        for i, (symbol, row, col) in enumerate(history, start=1):
            player = self.controller.players[symbol]
            self.history_text.insert(
                tk.END,
                f"{i}. {player.get_name()} ({symbol}) -> row {row + 1}, col {col + 1}\n",
            )
        self.history_text.config(state="disabled")
    def _handle_game_over(self, result):
        """Disable the board and announce the outcome."""
        self._disable_board()
        if result["draw"]:
            self.status_label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw! The board is full.")
        else:
            winner = self.controller.players[result["winner"]]
            self.status_label.config(
                text=f"{winner.get_name()} ({winner.get_symbol()}) wins!"
            )
            self._highlight_winning_line(result["winner"])
            messagebox.showinfo(
                "Game Over",
                f"{winner.get_name()} ({winner.get_symbol()}) wins!",
            )
    def _highlight_winning_line(self, winner_symbol):
        """Highlight the three cells that form the winning line."""
        grid = self.controller.board.grid
        lines = []
        # Rows
        for r in range(3):
            lines.append([(r, 0), (r, 1), (r, 2)])
        # Columns
        for c in range(3):
            lines.append([(0, c), (1, c), (2, c)])
        # Diagonals
        lines.append([(0, 0), (1, 1), (2, 2)])
        lines.append([(0, 2), (1, 1), (2, 0)])
        for line in lines:
            symbols = [grid[r][c] for (r, c) in line]
            if symbols[0] == symbols[1] == symbols[2] == winner_symbol:
                for (r, c) in line:
                    self.buttons[r][c].config(bg="#06d6a0", fg="white")
                break
    def _disable_board(self):
        """Disable all board buttons."""
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(state="disabled")
    def reset_game(self):
        """Reset the game state and the GUI."""
        self.controller.reset()
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(
                    text=" ", bg="#3b4a6b", fg="white", state="normal"
                )
        self._update_status()
        self._update_history()
    def run(self):
        """Start the tkinter main loop."""
        self.root.mainloop()