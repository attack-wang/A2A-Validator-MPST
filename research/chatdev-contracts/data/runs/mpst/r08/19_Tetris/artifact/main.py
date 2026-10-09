'''
main.py
Entry point for the Tetris game.
Uses tkinter from the Python standard library for the window and input so
the game runs without any third-party dependencies (the previous pygame
version failed with ModuleNotFoundError when pygame was not installed).
Initialises the window, creates the Game/Renderer objects, binds the
keyboard (move, rotate, soft/hard drop, pause, restart) and drives the
game loop with a fixed timer tick.
'''
import tkinter as tk
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, FRAME_INTERVAL_MS,
    COLOR_BACKGROUND,
)
from game import Game
from renderer import Renderer
KEY_ACTIONS = {
    "Left": "move_left",
    "Right": "move_right",
    "Up": "rotate",
    "Down": "soft_drop",
    "space": "hard_drop",
}
class TetrisApp:
    """Wires the tkinter window, keyboard input, game logic and renderer."""
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                                bg=COLOR_BACKGROUND, highlightthickness=0)
        self.canvas.pack()
        self.game = Game()
        self.renderer = Renderer(self.canvas)
        self.paused = False
        root.bind("<Key>", self._on_key)
        self._tick()
    def _on_key(self, event):
        key = event.keysym
        if key in ("p", "P"):
            self.paused = not self.paused
        elif key in ("r", "R"):
            self.game.restart()
            self.paused = False
        elif not self.paused and not self.game.game_over:
            action = KEY_ACTIONS.get(key)
            if action is not None:
                getattr(self.game, action)()
    def _tick(self):
        if not self.paused and not self.game.game_over:
            self.game.update(FRAME_INTERVAL_MS / 1000.0)
        self.renderer.draw(self.game, self.paused)
        self.root.after(FRAME_INTERVAL_MS, self._tick)
def main():
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.resizable(False, False)
    TetrisApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()