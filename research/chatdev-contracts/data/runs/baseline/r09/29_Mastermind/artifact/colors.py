'''
colors.py
Definition of the color palette used by the Mastermind game.
Each color is identified by a single-character symbol that the
player types as part of a guess (e.g. "1234"). This module maps
those symbols to human-readable color names for display purposes.
'''
# Mapping of guess symbols to color names.
# The keys are exactly the characters the player may use in a guess.
COLORS = {
    '1': 'Red',
    '2': 'Blue',
    '3': 'Green',
    '4': 'Yellow',
    '5': 'Orange',
    '6': 'Purple',
}
# Feedback peg symbols used on the board.
EXACT_PEG = 'X'   # right color in the right position
PARTIAL_PEG = 'O' # right color in the wrong position
EMPTY_PEG = '-'   # unused feedback slot
def get_valid_symbols():
    '''Return the list of valid guess symbols (the keys of COLORS).'''
    return list(COLORS.keys())
def get_color_name(symbol):
    '''Return the human-readable color name for a guess symbol.'''
    return COLORS.get(symbol, symbol)
def describe_code(code):
    '''Return a readable description of a code, e.g. "1(Red) 2(Blue) ...".'''
    return ' '.join('{}({})'.format(sym, get_color_name(sym)) for sym in code)