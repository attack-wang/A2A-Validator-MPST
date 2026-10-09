    def run_loop(self, state):
        """Core loop: enter node -> show text -> choices -> advance -> repeat."""
        node = self.engine.enter_node(state, state.current_node)
        while True:
            self.ui.show_divider()
            self.ui.show_text(node.get_text(state))
            if node.is_ending:
                self.handle_ending(node, state)
                return
            available, locked = self.engine.get_available_choices(node, state)
            if not available:
                # Dead end safety net: every non-ending node should have
                # choices, but if all are locked we must not soft-lock.
                self.ui.show_text("No choices remain available...")
                self.maybe_save(state)
                return
            self.ui.show_choices(
                [(c.index + 1, c.text) for c in available],
                [(None, c.text, c.lock_reason(state)) for c in locked],
            )
            kind, num = self.ui.get_command({c.index + 1 for c in available})
            if kind == "status":
                self.ui.show_status(state)
                continue
            if kind == "quit":
                if self.ui.confirm("Save before quitting?"):
                    self.maybe_save(state)
                return
            choice = next(c for c in available if c.index + 1 == num)
            next_id = self.engine.advance(state, node, choice)
            node = self.engine.enter_node(state, next_id)