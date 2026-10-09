'''
Legal-move generation and standard Checkers (English draughts) rules:
mandatory captures, multi-jump chains, and kinging.
'''
from dataclasses import dataclass, field
from piece import Color
from board import Board
DIRECTIONS_ALL = ((-1, -1), (-1, 1), (1, -1), (1, 1))
FORWARD = {Color.RED: (-1,), Color.BLACK: (1,)}  # hmm