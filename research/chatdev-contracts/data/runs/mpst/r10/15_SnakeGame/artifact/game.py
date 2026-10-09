'''
game.py
Core game controller for the Classic Snake game.
Owns the tkinter window, the game-state machine (menu, playing,
paused, game over), timer-driven movement, collision resolution,
scoring, and difficulty handling. Implemented with the Python
standard library only (tkinter) so no third-party packages are
required.
'''
import tkinter as tk
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    GRID_WIDTH, GRID_HEIGHT,
    INITIAL_SNAKE_LENGTH, GROWTH_PER_FOOD,
    START_POSITION, START_DIRECTION,
    DIFFICULTIES, DEFAULT_DIFFICULTY_INDEX,
    SPEED_UP_EVERY_N_FOODS, SPEED_UP_INCREMENT, MAX_MOVES_PER_SECOND,
    MIN_MOVE_INTERVAL_MS,
)
from snake import Snake
from food import Food
from scoreboard import Scoreboard
from renderer import Renderer
from input_handler import InputHandler
class Game:
    """State machine + timer-driven loop for the Snake game."""
    MENU, PLAYING, PAUSED, GAME_OVER = range(4)
    RENDER_INTERVAL_MS = 33  # ~30 FPS UI refresh
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        self.root.configure(bg="#12121a")
        self.renderer = Renderer(self.root)
        self.input_handler = InputHandler(self.root)
        self.snake = Snake(START_POSITION, INITIAL_SNAKE_LENGTH, START_DIRECTION)
        self.food = Food(GRID_WIDTH, GRID_HEIGHT)
        self.scoreboard = Scoreboard()
        self.difficulties = DIFFICULTIES
        self.menu_index = DEFAULT_DIFFICULTY_INDEX
        self.difficulty = self.difficulties[self.menu_index]
        self.moves_per_second = float(self.difficulty["moves_per_second"])
        self.move_interval_ms = self._interval_from_speed(self.moves_per_second)
        self.foods_eaten = 0
        self.victory = False
        self.new_high_score = False
        self.state = self.MENU
        self.running = True
        self._move_job = None
        self._render_job = None
    # ------------------------------------------------------------------ loop
    def run(self):
        """Main loop: tkinter mainloop with periodic render + move timers."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._schedule_render()
        self.root.mainloop()
    def _schedule_render(self):
        if not self.running:
            return
        try:
            self.renderer.render_frame(self)
        except tk.TclError:
            return  # window already destroyed
        self._render_job = self.root.after(self.RENDER_INTERVAL_MS, self._schedule_render)
    def _schedule_move(self):
        if not self.running or self.state != self.PLAYING:
            return
        self._move_job = self.root.after(self.move_interval_ms, self._move_step)
    def _move_step(self):
        if not self.running or self.state != self.PLAYING:
            return
        self._step_snake()
        self._schedule_move()
    def _cancel_move_job(self):
        if self._move_job is not None:
            try:
                self.root.after_cancel(self._move_job)
            except Exception:
                pass
            self._move_job = None
    @staticmethod
    def _interval_from_speed(moves_per_second):
        return max(20, int(round(1000.0 / max(moves_per_second, 0.001))))