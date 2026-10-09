'''
exceptions.py
Custom exception types for the checkers game.
'''
class CheckersError(Exception):
    '''Base class for all checkers game errors.'''
class NotationError(CheckersError):
    '''Raised when the player's input cannot be parsed as move notation.'''
class IllegalMoveError(CheckersError):
    '''Raised when a syntactically valid move violates the rules.'''