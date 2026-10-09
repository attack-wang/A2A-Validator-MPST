    def execute_move(self, positions, ask_next_hop=None):
        """
        Validate and apply a complete move path incrementally.
        Each segment is validated against the live board and applied immediately
        (validate → apply → continue), so continuation jumps see the true board
        state. A snapshot is taken first; any MoveError rolls the board back.
        positions: list of (row, col) starting with the mover's square.
        ask_next_hop: optional callable (from_name, targets) -> (row, col) used to
            interactively request continuation jumps when the given path ends
            mid-chain. If omitted, an incomplete capture chain raises MoveError.
        Returns a human-readable description of the executed move.
        """
        if not positions or len(positions) < 2:
            raise MoveError("A move needs a 'from' and a 'to' square.")
        snap = self.board.snapshot()
        try:
            cur = positions[0]
            piece = self.board.get_piece(*cur)
            if piece is None:
                raise MoveError(f"There is no piece on {square_name(*cur)}.")
            if piece.color != self.current_player:
                raise MoveError(f"It is {self.current_player}'s turn; the piece on {square_name(*cur)} belongs to {piece.color}.")
            steps = []
            crowned = False
            for i, to_pos in enumerate(positions[1:]):
                if i == 0:
                    legal = self.piece_moves(cur)
                else:
                    if crowned:
                        raise MoveError("A move must end when the piece is crowned.")
                    legal = self.capture_targets(*cur)
                    if not legal:
                        raise MoveError(f"No capture available from {square_name(*cur)}; the chain cannot continue there.")
                if to_pos not in legal:
                    expected = ", ".join(square_name(*t) for t in legal) or "none"
                    raise MoveError(f"Illegal step {square_name(*cur)} -> {square_name(*to_pos)}. Legal destinations: {expected}.")
                captured, crowned = self.apply_move(cur, to_pos)
                steps.append((cur, to_pos, captured))
                cur = to_pos
            # Mandatory continuation: a jump that can capture again must continue.
            while steps and steps[-1][2] is not None and self.can_continue_jumping(cur, crowned):
                if ask_next_hop is None:
                    raise MoveError(
                        f"Capture chain must be completed: {square_name(*cur)} can capture again "
                        f"(e.g. include every jump, like b3-d5-f7)."
                    )
                targets = self.capture_targets(*cur)
                nxt = ask_next_hop(square_name(*cur), targets)
                if nxt not in targets:
                    raise MoveError("Invalid continuation square.")
                captured, crowned = self.apply_move(cur, nxt)
                steps.append((cur, nxt, captured))
                cur = nxt
            self.last_move_desc = self.describe_move(steps, crowned)
            # Switch turns, then evaluate game-over for the side that must now move.
            self.current_player = BLACK if self.current_player == RED else RED
            self.check_game_over()
            return self.last_move_desc
        except MoveError:
            self.board.restore(snap)
            raise