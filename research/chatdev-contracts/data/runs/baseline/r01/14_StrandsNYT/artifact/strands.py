'''
Strands - a word search puzzle game inspired by the NYT Strands.
...
'''
import tkinter as tk
import random
import os
import sys
# ---------- Puzzle data ----------
PUZZLE = {
    "theme": "Breakfast",
    "clue": "Rise and shine! The most important meal of the day.",
    "spangram": "BREAKFAST",
    "words": {
        "PANCAKE": [(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1)],
        "CEREAL": [(0,2),(1,2),(2,2),(3,2),(4,2),(5,2)],
        "WAFFLE": [(0,3),(1,3),(2,3),(3,3),(4,3),(5,3)],
        "OMELET": [(0,4),(1,4),(2,4),(3,4),(4,4),(5,4)],
        "TOAST": [(0,5),(1,5),(2,5),(3,5),(4,5)],
        "BACON": [(5,5),(6,5),(7,5),(7,4),(7,3)],
        "EGGS": [(6,2),(7,2),(6,3),(6,4)],
    },
}