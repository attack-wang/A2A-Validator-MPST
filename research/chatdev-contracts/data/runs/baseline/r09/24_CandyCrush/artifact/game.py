'''
game.py
Game state management: score, level, move budget, and the cascade
resolution pipeline that turns a player swap into a MoveResult the
GUI can animate.
'''
from game_logic import Board
from cascadestep import MoveResult, CascadeStep
class Game:
    """Manages game state: score, moves, level, and move resolution."""
    def __init__(self, rows=8, cols=8, num_types=6,
                 moves_per_level=20, base_target=1000, target_step=1500, seed=None):
        self.board = Board(rows, cols, num_types, seed=seed)
        self.score = 0
        self.level = 1
        self.moves_left = moves_per_level
        self.moves_per_level = moves_per_level
        self._base_target = base_target
        self._target_step = target_step
        self.game_over = False
        self.victory = False  # True when the final level's target is reached
    @property
    def target(self):
        """Score needed to clear the current level."""
        return self._base_target + (self.level - 1) * self._target_step
    def peek_move(self, r1, c1, r2, c2):
        """Non-mutating validity check used by the GUI before animating."""
        if not (self.board.in_bounds(r1, c1) and self.board.in_bounds(r2, c2)):
            return False
        if not self.board.are_adjacent(r1, c1, r2, c2):
            return False
        return bool(self.board.swap_creates_match(r1, c1, r2, c2))
    def make_move(self, r1, c1, r2, c2):
        """Attempt a move; returns a MoveResult for GUI animation, or None if invalid."""
        if not self.peek_move(r1, c1, r2, c2):
            return None
        self.board.swap(r1, c1, r2, c2)  # commit swap
        self.moves_left -= 1
        cascades, total_points, chain = [], 0, 0
        while True:  # resolve cascades until stable
            matches = self.board.find_matches()
            if not matches:
                break
            chain += 1
            points = len(matches) * 10 * chain  # chain-reaction multiplier
            for (r, c) in matches:
                self.board.grid[r][c] = 0  # clear phase
            falls, spawns = self.board.apply_gravity()
            cascades.append(CascadeStep(matches, falls, spawns, points, chain))
            total_points += points
        self.score += total_points
        level_up = self.score >= self.target
        if level_up:
            self.level += 1
            self.moves_left = self.moves_per_level  # target recomputed by property
        out_of_moves = self.moves_left <= 0 and not level_up
        if out_of_moves:
            self.game_over = True
        board_shuffled = False
        if not self.board.has_possible_moves():  # deadlock guard
            self.board.shuffle()
            board_shuffled = True
        return MoveResult(True, (r1, c1, r2, c2), cascades, total_points,
                          level_up, self.game_over, out_of_moves, board_shuffled)