'''
player.py
Simple Player value object holding a display name and piece color.
'''
from piece import Piece
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
    @property
    def is_red(self):
        return self.color == Piece.RED
    def __str__(self):
        return f"{self.name} ({'Red' if self.is_red else 'Black'})"