'''
rules.py
Legal-move generation for English/American checkers (draughts).
Rules implemented:
  * Men move one square diagonally forward to an empty square.
  * Kings move one square diagonally in any direction.
  * A jump captures an adjacent enemy piece by leaping to the empty
    square directly beyond it (men jump forward only; kings jump in
    all four diagonal directions).
  * Captures are mandatory: if any jump exists, only jumps are legal.
  * After a jump, if the same piece can jump again it must do so
    (handled by the Game controller via the returned jump targets).
'''
from board import BOARD_SIZE
from move import Move
from pieces import PieceColor
# Diagonal directions as (drow, dcol). Row index grows toward the
# BLACK side's back rank... 