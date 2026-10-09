'''
renderer.py
All drawing code for the Classic Snake game, implemented with tkinter.
...
'''
import tkinter as tk
from settings import (...)
class Renderer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=COLOR_BACKGROUND, highlightthickness=0)
        self.canvas.pack()
        self.font_large = ("Arial", 32, "bold")
        self.font_medium = ("Arial", 18, "bold")
        self.font_small = ("Arial", 12)
    def render_frame(self, game):
        self.canvas.delete("all")
        self._draw_score_bar(game)
        self._draw_board()
        self._draw_food(game.food)
        self._draw_snake(game.snake)
        if game.state == game.MENU:
            self._draw_menu_overlay(game)
        elif game.state == game.PAUSED:
            self._draw_pause_overlay()
        elif game.state == game.GAME_OVER:
            self._draw_game_over_overlay(game)