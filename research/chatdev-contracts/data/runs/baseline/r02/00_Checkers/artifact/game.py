class CheckersGame:
    def __init__(self)
    def current_player
    def get_all_moves(player) -> dict of from_pos -> list of paths
    def get_moves_for_piece(r, c) -> list of paths (each path is list of positions)
    def get_simple_moves(r, c) -> list of single-step destinations
    def get_jump_moves(r, c) -> list of (destination, captured_pos)
    def get_jump_chains(r, c) -> list of full capture paths (recursive)
    def is_valid_path(path) -> bool
    def apply_move(path) -> executes, handles capture, kinging, promotion stop
    def has_any_move(player) -> bool
    def check_game_over() -> winner or None
    def switch_turn()