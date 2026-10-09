def main():
    # choose puzzle
    print header
    list puzzles with themes
    let user pick (or default 1)
    puzzle = Puzzle(theme, targets)
    engine = GameEngine(puzzle)
    loop:
        render board
        read command
        dispatch
        print feedback
        if complete: victory banner, break