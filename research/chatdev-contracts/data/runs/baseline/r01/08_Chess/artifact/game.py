PIECE_LETTERS = 'KQRBN'
def square_name(square):
    r, c = square
    return chr(ord('a') + c) + str(8 - r)
def parse_square(name):
    ...