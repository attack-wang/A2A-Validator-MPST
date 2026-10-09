'''
main.py
Entry point of the Tetris game. Built on tkinter from the Python
standard library, so no third-party packages (such as pygame) are
required. Initializes the game state and renderer, binds keyboard
controls (move, rotate, soft/hard drop, pause, restart, quit) and runs
a periodic timer that advances gravity and refreshes the display.
'''
import tkinter as tk
from constants import TICK_MS
from game import Game
from renderer import Renderer
class TetrisApp:
    """Tkinter application shell handling input and the main loop."""
    def __init__(self, root):
        self.root = root
        root.title('Tetris')
        root.resizable(False, False)
        self.game = Game()
        self.renderer = Renderer(root)
        self.paused = False
        self._bind_keys()
        self._redraw()
        self._tick()
    def _bind_keys(self):
        bindings = {
            '<Left>': lambda e: self._move(-1, 0),
            '<Right>': lambda e: self._move(1, 0),
            '<Up>': lambda e: self._rotate(),
            '<Down>': lambda e: self._soft_drop(),
            '<space>': lambda e: self._hard_drop(),
            'p': lambda e: self._toggle_pause(),
            'P': lambda e: self._toggle_pause(),
            'r': lambda e: self._restart(),
            'R': lambda e: self._restart(),
            '<Escape>': lambda e: self.root.destroy(),
        }
        for sequence, handler in bindings.items():
            self.root.bind(sequence, handler)
    # --- player actions -------------------------------------------------
    def _active(self):
        return not self.paused and not self.game.game_over
    def _move(self, dx, dy):
        if self._active():
            self.game.move_piece(dx, dy)
        self._redraw()
    def _rotate(self):
        if self._active():
            self.game.rotate_piece()
        self._redraw()
    def _soft_drop(self):
        if self._active():
            self.game.soft_drop()
        self._redraw()
    def _hard_drop(self):
        if self._active():
            self.game.hard_drop()
        self._redraw()
    def _toggle_pause(self):
        if not self.game.game_over:
            self.paused = not self.paused
        self._redraw()
    def _restart(self):
        if self.game.game_over:
            self.game = Game()
            self.paused = False
        self._redraw()
    # --- main loop ------------------------------------------------------
    def _tick(self):
        """Advance gravity on a fixed timer and redraw."""
        if self._active():
            self.game.update(TICK_MS)
        self._redraw()
        self.root.after(TICK_MS, self._tick)
    def _redraw(self):
        self.renderer.draw(self.game, self.paused)
def main():
    root = tk.Tk()
    TetrisApp(root)
    root.mainloop()
if __name__ == '__main__':
    main()