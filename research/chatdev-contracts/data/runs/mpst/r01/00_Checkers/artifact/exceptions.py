'''
exceptions.py
Custom exceptions for the checkers game.
All errors raised by the checkers engine derive from CheckersError so
callers can catch every game-related failure with a single except clause.
'''
class CheckersError(Exception):
    '''Base exception for checkers game errors.'''
    def __init__(self, message=""):
        '''Initialise the error with an optional human-readable message.'''
        self.message = message
        super().__init__(message)
class InvalidMoveError(CheckersError):
    '''Raised when a move is invalid or illegal.'''
    def __init__(self, message="Illegal move."):
        '''Initialise the error with a descriptive reason.'''
        super().__init__(message)
class InvalidFormatError(CheckersError):
    '''Raised when move notation cannot be parsed.'''
    def __init__(self, message="Could not parse move notation."):
        '''Initialise the error with a descriptive reason.'''
        super().__init__(message)