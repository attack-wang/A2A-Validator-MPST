    def parse_input(self, raw):
        """Parse a command line.
        Returns one of:
            ('quit', None)
            ('show', what)   with what in {'grid', 'clues', 'help', 'all'}
            ('entry', (number, direction, word))
            ('invalid', message)
        """
        text = raw.strip()
        if not text:
            return ('invalid', "Empty command. Type 'help' for usage.")
        low = text.lower()
        if low in ('q', 'quit', 'exit'):
            return ('quit', None)
        if low in ('g', 'grid'):
            return ('show', 'grid')
        if low in ('c', 'clues'):
            return ('show', 'clues')
        if low in ('h', 'help'):
            return ('show', 'help')
        if low == 'all':
            return ('show', 'all')
        parts = text.split()
        if len(parts) != 3:
            return ('invalid', "Usage: <number> <across|down> <word>  (or 'help')")
        number_text, direction_text, word = parts
        if not number_text.isdigit():
            return ('invalid', f"'{number_text}' is not a clue number.")
        direction = direction_text.lower()
        if direction in ('a', 'ac'):
            direction = ACROSS
        elif direction in ('d', 'dn'):
            direction = DOWN
        if direction not in (ACROSS, DOWN):
            return ('invalid', "Direction must be 'across' or 'down'.")
        return ('entry', (int(number_text), direction, word))