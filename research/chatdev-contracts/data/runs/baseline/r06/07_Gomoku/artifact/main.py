'''
main.py
Main entry point for the Gomoku game.
Launches the graphical (pygame) version when pygame is available; if the
pygame module is missing, it prints installation instructions and falls
back to an interactive console version so the game remains playable.
'''
import sys
def run_gui():
    '''Initialize pygame, create the window, and run the GUI main loop.'''
    import pygame
    from game import GameController
    from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    controller = GameController(screen)
    controller.update_display()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = controller.gui.pixel_to_board(*event.pos)
                if cell is not None:
                    controller.handle_click(cell[0], cell[1])
                    controller.update_display()
            elif event.type == pygame.MOUSEMOTION:
                # Show a translucent preview stone under the cursor.
                if not controller.game_over:
                    cell = controller.gui.pixel_to_board(*event.pos)
                    controller.update_display(hover_cell=cell)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                controller.reset()
                controller.update_display()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
def run_console():
    '''Interactive console fallback playable without pygame installed.'''
    from board import Board
    from constants import BLACK, WHITE, EMPTY
    symbols = {EMPTY: '.', BLACK: 'X', WHITE: 'O'}
    board = Board()
    current = BLACK  # Black always moves first
    def render():
        '''Print the current board with row/column indices.'''
        header = '   ' + ' '.join(str(c % 10) for c in range(board.size))
        print(header)
        for r in range(board.size):
            row_text = ' '.join(symbols[board.grid[r][c]] for c in range(board.size))
            print(f'{r % 10:2d} {row_text}')
        print()
    print('Gomoku - Five in a Row (console mode)')
    print("Enter moves as 'row col' (0-14), e.g. '7 7'. Type 'q' to quit.")
    render()
    while True:
        player = 'Black (X)' if current == BLACK else 'White (O)'
        try:
            raw = input(f"{player}'s move: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print('\nGame aborted.')
            return
        if raw in ('q', 'quit', 'exit'):
            print('Game aborted.')
            return
        parts = raw.replace(',', ' ').split()
        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            print('Invalid input. Enter two numbers 0-14 separated by a space.')
            continue
        row, col = int(parts[0]), int(parts[1])
        if not board.place_stone(row, col, current):
            print('Invalid move: cell is occupied or out of bounds. Try again.')
            continue
        render()
        if board.check_win(row, col, current):
            print(f'{player} wins with five in a row!')
            return
        if board.is_full():
            print("The board is full - it's a draw!")
            return
        current = WHITE if current == BLACK else BLACK
def main():
    '''Prefer the GUI version; fall back to console mode without pygame.'''
    try:
        run_gui()
    except ImportError:
        print('pygame is not installed - switching to console mode.')
        print('To enable the graphical version, run:  pip install pygame\n')
        run_console()
if __name__ == '__main__':
    main()