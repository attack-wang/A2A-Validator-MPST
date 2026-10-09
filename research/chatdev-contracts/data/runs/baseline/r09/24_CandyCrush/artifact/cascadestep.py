'''
cascadestep.py
Shared data structures describing the outcome of a move.
MoveResult is returned by Game.make_move and consumed by the GUI;
CascadeStep describes one clear -> fall -> spawn cycle within a move
(the "chain" field is the 1-based cascade depth used for scoring and
animation pacing).
'''
from collections import namedtuple
# cleared: set of (r, c) cells removed this step
# falls:   list of (from_r, from_c, to_r, to_c) gravity movements
# spawns:  list of (r, c, candy_type) newly spawned candies
# points:  points awarded for this step (chain multiplier already applied)
# chain:   1-based cascade depth (1 = the initial match)
CascadeStep = namedtuple("CascadeStep", ["cleared", "falls", "spawns", "points", "chain"])
MoveResult = namedtuple("MoveResult",
    ["valid", "swap", "cascades", "total_points", "level_up",
     "game_over", "out_of_moves", "board_shuffled"])