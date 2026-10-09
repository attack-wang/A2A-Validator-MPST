'''
main.py
Entry point for the Mastermind code-breaking game.
Wires together the board, the game engine and the difficulty
selection, and offers to replay after each round.
'''
import sys
from board import Board
from constants import DEFAULT_DIFFICULTY_KEY, DIFFICULTIES
from game import Game
BANNER = r"""
+==========================================================+
|                                                          |
|            M A S T E R M I N D                           |
|            Crack the hidden color code!                  |
|                                                          |
+==========================================================+
"""