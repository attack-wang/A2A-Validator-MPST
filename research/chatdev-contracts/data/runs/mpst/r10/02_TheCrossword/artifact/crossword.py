def _entry_letters(grid_state, entry):
    r, c, n = entry['row'], entry['col'], entry['length']
    if entry['direction'] == 'A':
        return ''.join(grid_state[r][c + i] for i in range(n))
    return ''.join(grid_state[r + i][c] for i in range(n))