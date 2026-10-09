'''
game.py
Core module containing the Game class that implements Reversi (Othello) rules
and the console interaction loop for two local players.
'''
class Game:
    '''Implements Reversi game logic and console I/O for two local players.'''
    EMPTY, BLACK, WHITE = '.', 'B', 'W'
    SIZE = 8
    # All 8 directions: up-left, up, up-right, left, right, down-left, down, down-right
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]
    def __init__(self):
        '''Initialize an 8x8 board with the standard 4-disc starting position.'''
        self.board = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.board[3][3] = self.WHITE
        self.board[4][4] = self.WHITE
        self.board[3][4] = self.BLACK
        self.board[4][3] = self.BLACK
        self.current_player = self.BLACK  # Black always moves first
    def _in_bounds(self, row, col):
        '''Return True if (row, col) lies within the 8x8 board.'''
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    def _opponent(self, player):
        '''Return the disc color of the opposing player.'''
        return self.WHITE if player == self.BLACK else self.BLACK
    def _flips_for_move(self, row, col, player):
        '''Return the list of (row, col) discs that would be flipped if `player`
        places a disc at (row, col). Empty list means the move is illegal.'''
        if not self._in_bounds(row, col) or self.board[row][col] != self.EMPTY:
            return []
        opponent = self._opponent(player)
        flips = []
        for dr, dc in self.DIRECTIONS:
            line = []
            r, c = row + dr, col + dc
            # Walk outward over consecutive opponent discs.
            while self._in_bounds(r, c) and self.board[r][c] == opponent:
                line.append((r, c))
                r += dr
                c += dc
            # Legal only if the line is anchored by one of the player's own discs.
            if line and self._in_bounds(r, c) and self.board[r][c] == player:
                flips.extend(line)
        return flips
    def is_valid_move(self, row, col, player):
        '''Return True if placing a disc at (row, col) flips at least one opponent disc.'''
        return len(self._flips_for_move(row, col, player)) > 0
    def valid_moves(self, player):
        '''Return a list of all valid (row, col) moves for the given player.'''
        return [(r, c) for r in range(self.SIZE) for c in range(self.SIZE)
                if self.is_valid_move(r, c, player)]
    def apply_move(self, row, col, player):
        '''Place a disc at (row, col) and flip all captured discs.
        Return True if the move was legal, False otherwise.'''
        flips = self._flips_for_move(row, col, player)
        if not flips:
            return False
        self.board[row][col] = player
        for r, c in flips:
            self.board[r][c] = player
        return True
    def score(self):
        '''Return a tuple (black_count, white_count) of discs currently on the board.'''
        black = sum(row.count(self.BLACK) for row in self.board)
        white = sum(row.count(self.WHITE) for row in self.board)
        return black, white
    def _board_full(self):
        '''Return True if every cell of the board is occupied.'''
        return all(cell != self.EMPTY for row in self.board for cell in row)
    def _display(self):
        '''Print the board with column letters, row numbers, '*' markers on legal
        moves, the current score, and whose turn it is.'''
        move_set = set(self.valid_moves(self.current_player))
        print()
        print('   ' + ' '.join(chr(ord('a') + c) for c in range(self.SIZE)))
        for r in range(self.SIZE):
            cells = []
            for c in range(self.SIZE):
                if self.board[r][c] == self.EMPTY and (r, c) in move_set:
                    cells.append('*')  # marker for a legal move
                else:
                    cells.append(self.board[r][c])
            print(f'{r + 1}  ' + ' '.join(cells))
        black, white = self.score()
        print(f'Score -> Black (B): {black}  White (W): {white}')
        name = 'Black (B)' if self.current_player == self.BLACK else 'White (W)'
        print(f'Turn: {name}')
    def _parse_input(self, text):
        '''Convert input like "d3" into (row, col) indices; return None if malformed.'''
        text = text.strip().lower()
        if len(text) != 2 or not ('a' <= text[0] <= 'h') or not ('1' <= text[1] <= '8'):
            return None
        col = ord(text[0]) - ord('a')
        row = int(text[1]) - 1
        return row, col
    def _read_input(self):
        '''Read a move from the console; return None on EOF or interrupt.'''
        try:
            return input('Your move: ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
    def run(self):
        '''Main game loop: alternate turns, handle passes, and print the final result.
        The game ends when the board is full or neither player has a valid move.'''
        print('=== Reversi (Othello) ===')
        print('Enter moves as column+row, e.g. "d3". Enter "q" to quit.')
        while True:
            if self._board_full():
                break  # board is full -> game over
            moves = self.valid_moves(self.current_player)
            if not moves:
                opponent = self._opponent(self.current_player)
                if not self.valid_moves(opponent):
                    break  # neither side can move -> game over
                name = 'Black' if self.current_player == self.BLACK else 'White'
                print(f'{name} has no valid moves; turn passes.')
                self.current_player = opponent
                continue
            self._display()
            choice = self._read_input()
            if choice is None or choice == 'q':
                print('Game aborted by player.')
                return
            pos = self._parse_input(choice)
            if pos is None or not self.is_valid_move(pos[0], pos[1], self.current_player):
                print('Invalid move, try again.')
                continue
            self.apply_move(pos[0], pos[1], self.current_player)
            self.current_player = self._opponent(self.current_player)
        # Final board and result
        self._display()
        black, white = self.score()
        if black > white:
            result = 'Black wins!'
        elif white > black:
            result = 'White wins!'
        else:
            result = "It's a draw!"
        print(f'Game over. Final score -> Black: {black}, White: {white}. {result}')