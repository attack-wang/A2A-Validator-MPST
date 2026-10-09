'''
input_handler.py
Keyboard input translation for the Classic Snake game using tkinter.
...
'''
import tkinter as tk
from settings import DIRECTION_KEYS, DIFFICULTY_KEYS
class InputHandler:
    def __init__(self, root):
        self.root = root
        self._actions = []
        for keysym in list(DIRECTION_KEYS) + list(DIFFICULTY_KEYS) + ["Escape", "p", "P", "Return", "space"]:
            self.root.bind(f"<Key-{keysym}>", self._on_key)
        self.root.bind("<Key>", self._on_any_key)  # hmm, careful about double handling