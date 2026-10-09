'''
Game class implementing the Snake game loop, rendering and UI with tkinter.
'''
import tkinter as tk
from config import (
    CELL_SIZE,
    GRID_WIDTH,
    GRID_HEIGHT,
    COLOR_BACKGROUND,
    COLOR_GRID,
    COLOR_SNAKE_HEAD,
    COLOR_SNAKE_BODY,
    COLOR_FOOD,
    COLOR_TEXT,
    COLOR_BORDER,
    DIFFICULTY_LEVELS,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)
from snake import Snake
from food import Food
from scoreboard import ScoreBoard
class Game:
    '''Tkinter-based Snake game: menu, loop, rendering and game-over flow.'''
    def __init__(self, master):
        '''Build the window, canvas, status bar and show the main menu.'''
        self.master = master
        self.master.title("Classic Snake")
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self._on_close)
        self.board_width = GRID_WIDTH * CELL_SIZE
        self.board_height = GRID_HEIGHT * CELL_SIZE
        self.canvas = tk.Canvas(
            master,
            width=self.board_width,
            height=self.board_height,
            bg=COLOR_BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.status_bar = tk.Label(
            master,
            text="",
            font=("Consolas", 12),
            fg=COLOR_TEXT,
            bg="#11111b",
            anchor="w",
        )
        self.status_bar.pack(fill=tk.X)
        self.scoreboard = ScoreBoard()
        # Game state machine: "menu" | "playing" | "paused" | "game_over"
        self.state = "menu"
        self.difficulty = None
        self.move_interval = None
        self.score_per_food = None
        self.snake = None
        self.food = None
        self.score = 0
        self._loop_job = None
        self._canvas_widgets = []  # tk widgets embedded in the canvas
        self.master.bind("<KeyPress>", self.on_key_press)
        self.show_menu()
    # ------------------------------------------------------------- menu flow
    def show_menu(self):
        '''Display the main menu with difficulty selection buttons.'''
        self._cancel_loop()
        self._clear_canvas_widgets()
        self.state = "menu"
        self.score = 0
        self._update_status("Main Menu - select a difficulty")
        self.canvas.create_text(
            self.board_width // 2,
            self.board_height // 4,
            text="CLASSIC SNAKE",
            font=("Consolas", 28, "bold"),
            fill=COLOR_SNAKE_HEAD,
        )
        self.canvas.create_text(
            self.board_width // 2,
            self.board_height // 4 + 40,
            text="Select difficulty",
            font=("Consolas", 14),
            fill=COLOR_TEXT,
        )
        for index, (name, (interval, points)) in enumerate(DIFFICULTY_LEVELS.items()):
            high = self.scoreboard.get_high_score(name)
            button = tk.Button(
                self.canvas,
                text=f"{name}  (speed {interval} ms, +{points}/food)  High: {high}",
                font=("Consolas", 12),
                command=lambda n=name: self.start_game(n),
            )
            self.canvas.create_window(
                self.board_width // 2,
                self.board_height // 2 + index * 40,
                window=button,
            )
            self._canvas_widgets.append(button)
        self.canvas.create_text(
            self.board_width // 2,
            self.board_height - 30,
            text="Arrow keys or WASD to move  •  P to pause  •  Esc to menu",
            font=("Consolas", 11),
            fill=COLOR_GRID,
        )
    # ------------------------------------------------------------- game flow
    def start_game(self, difficulty):
        '''Start (or restart) a run with the chosen difficulty level.'''
        if difficulty not in DIFFICULTY_LEVELS:
            return
        self._cancel_loop()
        self._clear_canvas_widgets()
        self.difficulty = difficulty
        self.move_interval, self.score_per_food = DIFFICULTY_LEVELS[difficulty]
        self.score = 0
        self.snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2, initial_length=3)
        self.food = Food(GRID_WIDTH, GRID_HEIGHT, self.snake.body)
        self.state = "playing"
        self._draw_grid()
        self._draw()
        self._update_status()
        self._loop_job = self.master.after(self.move_interval, self._game_loop)
    def _game_loop(self):
        '''Advance the simulation one tick, then schedule the next tick.'''
        if self.state != "playing":
            return
        self.snake.move()
        # Collision checks: boundary first, then self overlap.
        if (self.snake.check_boundary_collision(GRID_WIDTH, GRID_HEIGHT)
                or self.snake.check_self_collision()):
            self._game_over()
            return
        # Food eaten: score, grow and respawn (None means board is full).
        if self.food.position is not None and self.snake.head == self.food.position:
            self.score += self.score_per_food
            self.snake.grow()
            self.food.respawn(self.snake.body)
            if self.food.position is None:
                self._draw()
                self._victory()
                return
        self._draw()
        self._update_status()
        self._loop_job = self.master.after(self.move_interval, self._game_loop)
    def _toggle_pause(self):
        '''Pause or resume the running game.'''
        if self.state == "playing":
            self.state = "paused"
            self._cancel_loop()
            self._update_status("Paused - press P to resume")
        elif self.state == "paused":
            self.state = "playing"
            self._update_status()
            self._loop_job = self.master.after(self.move_interval, self._game_loop)
    def _game_over(self):
        '''Stop the loop, record the score and show the game-over screen.'''
        self.state = "game_over"
        self._cancel_loop()
        is_record = self.scoreboard.record_score(self.difficulty, self.score)
        # Keep the final board visible under a translucent overlay.
        self._draw()
        self.canvas.create_rectangle(
            0, 0, self.board_width, self.board_height,
            fill="#000000", stipple="gray50", outline="",
        )
        self.canvas.create_text(
            self.board_width // 2,
            self.board_height // 2 - 40,
            text="GAME OVER",
            font=("Consolas", 28, "bold"),
            fill=COLOR_BORDER,
        )
        self.canvas.create_text(
            self.board_width // 2,
            self.board_height // 2,
            text=(f"Score: {self.score}    "
                  f"High: {self.scoreboard.get_high_score(self.difficulty)}"),
            font=("Consolas", 14),
            fill=COLOR_TEXT,
        )
        if is_record:
            self.canvas.create_text(
                self.board_width // 2,
                self.board_height // 2 + 35,
                text="NEW HIGH SCORE!",
                font=("Consolas", 14, "bold"),
                fill=COLOR_SNAKE_HEAD,
            )
        self.canvas.create_text(
            self.board_width // 2,
            self.board_height // 2 + 70,
            text="Space/Enter: play again   •   Esc: main menu",
            font=("Consolas", 12),
            fill=COLOR_TEXT,
        )
        self._update_status("Game Over")
    def _victory(self):
        '''Handle the rare case where the snake fills the entire board.'''
        self.state = "game_over"
        self._cancel_loop()
        is_record = self.scoreboard.record_score(self.difficulty, self.score)
        self.canvas.create_text(
            self.board_width // 2,
            self.board_height // 2 - 40,
            text="YOU WIN!",
            font=("Consolas", 28, "bold"),
            fill=COLOR_SNAKE_HEAD,
        )
        self.canvas.create_text(
            self.board_width // 2,
            self.board_height // 2,
            text=(f"Score: {self.score}    "
                  f"High: {self.scoreboard.get_high_score(self.difficulty)}"),
            font=("Consolas", 14),
            fill=COLOR_TEXT,
        )
        if is_record:
            self.canvas.create_text(
                self.board_width // 2,
                self.board_height // 2 + 35,
                text="NEW HIGH SCORE!",
                font=("Consolas", 14, "bold"),
                fill=COLOR_SNAKE_HEAD,
            )
        self.canvas.create_text(
            self.board_width // 2,
            self.board_height // 2 + 70,
            text="Space/Enter: play again   •   Esc: main menu",
            font=("Consolas", 12),
            fill=COLOR_TEXT,
        )
        self._update_status("Victory!")
    def _cancel_loop(self):
        '''Cancel any scheduled loop callback, if one is pending.'''
        if self._loop_job is not None:
            try:
                self.master.after_cancel(self._loop_job)
            except Exception:
                pass  # Callback already fired or window is closing.
            self._loop_job = None
    # ------------------------------------------------------------- rendering
    def _draw_grid(self):
        '''Draw the background grid lines and the board border.'''
        self.canvas.delete("grid")
        for x in range(0, self.board_width, CELL_SIZE):
            self.canvas.create_line(
                x, 0, x, self.board_height, fill=COLOR_GRID, tags="grid"
            )
        for y in range(0, self.board_height, CELL_SIZE):
            self.canvas.create_line(
                0, y, self.board_width, y, fill=COLOR_GRID, tags="grid"
            )
        self.canvas.create_rectangle(
            0, 0, self.board_width - 1, self.board_height - 1,
            outline=COLOR_BORDER, width=2, tags="grid",
        )
    def _draw_food(self):
        '''Draw the food item as a small circle.'''
        if self.food is not None and self.food.position is not None:
            x, y = self.food.position
            self.canvas.create_oval(
                x * CELL_SIZE + 5, y * CELL_SIZE + 5,
                (x + 1) * CELL_SIZE - 5, (y + 1) * CELL_SIZE - 5,
                fill=COLOR_FOOD, outline="", tags="food",
            )
    def _draw_snake(self):
        '''Draw the snake body, highlighting the head.'''
        if self.snake is None:
            return
        for index, (x, y) in enumerate(self.snake.body):
            color = COLOR_SNAKE_HEAD if index == 0 else COLOR_SNAKE_BODY
            self.canvas.create_rectangle(
                x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                (x + 1) * CELL_SIZE - 1, (y + 1) * CELL_SIZE - 1,
                fill=color, outline="", tags="snake",
            )
    def _draw(self):
        '''Redraw food and snake for the current tick.'''
        self.canvas.delete("food", "snake")
        self._draw_food()
        self._draw_snake()
    def _update_status(self, message=None):
        '''Update the status bar with score info or a custom message.'''
        if message is not None:
            self.status_bar.config(text=message)
            return
        if self.difficulty is not None:
            high = self.scoreboard.get_high_score(self.difficulty)
            self.status_bar.config(
                text=(f"Difficulty: {self.difficulty}   |   "
                      f"Score: {self.score}   |   High: {high}")
            )
        else:
            self.status_bar.config(text="")
    # ----------------------------------------------------------- interaction
    def on_key_press(self, event):
        '''Handle keyboard input for movement, pause and navigation.'''
        key = event.keysym.lower()
        direction_map = {
            "up": UP, "w": UP,
            "down": DOWN, "s": DOWN,
            "left": LEFT, "a": LEFT,
            "right": RIGHT, "d": RIGHT,
        }
        if self.state == "playing":
            if key in direction_map:
                self.snake.set_direction(direction_map[key])
            elif key == "p":
                self._toggle_pause()
            elif key == "escape":
                self.show_menu()
        elif self.state == "paused":
            if key == "p":
                self._toggle_pause()
            elif key == "escape":
                self.show_menu()
        elif self.state == "game_over":
            if key in ("space", "return") and self.difficulty is not None:
                self.start_game(self.difficulty)
            elif key == "escape":
                self.show_menu()
    # ------------------------------------------------------------- utilities
    def _clear_canvas_widgets(self):
        '''Destroy any tk widgets embedded in the canvas and clear the canvas.'''
        for widget in self._canvas_widgets:
            widget.destroy()
        self._canvas_widgets = []
        self.canvas.delete("all")
    def _on_close(self):
        '''Cleanly stop the loop and close the window.'''
        self._cancel_loop()
        self.master.destroy()