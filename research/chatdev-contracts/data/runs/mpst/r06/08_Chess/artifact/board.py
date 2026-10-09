def square_name(pos):
    row, col = pos
    return "abcdefgh"[col] + str(8 - row)
def parse_square(name):
    col = "abcdefgh".index(name[0])
    row = 8 - int(name[1])
    return (row, col)