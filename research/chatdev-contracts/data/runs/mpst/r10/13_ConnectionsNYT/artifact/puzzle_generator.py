'''
puzzle_generator.py
Puzzle data and daily-puzzle selection for ChatDev Connections.
Each puzzle is hand-crafted so that every word belongs to exactly one
hidden category (a unique solution), while words are deliberately chosen
so that several of them plausibly fit more than one category — creating
the misdirection that makes the game challenging.
The daily puzzle is chosen deterministically from the puzzle bank using
the calendar date as a random seed, so every player sees the same puzzle
on a given day and a fresh one appears at midnight.
'''
import random
from datetime import date
from constants import DIFFICULTY_ORDER, WORDS_PER_GROUP
class Puzzle:
    """A single Connections puzzle: four categories of four words each."""
    def __init__(self, categories, puzzle_id=""):
        ...