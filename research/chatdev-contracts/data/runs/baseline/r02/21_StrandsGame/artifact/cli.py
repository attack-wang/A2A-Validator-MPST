'''cli.py — command loop for the Strands game.'''
import sys
from game import StrandsGame
from ui import UI
HELP = ...
def process_command(game, ui, raw):
    tokens = raw.strip().split()
    if not tokens:
        return None  # no state change; maybe re-render
    cmd = tokens[0].lower()
    if cmd in ('s', 'submit'): return game.submit()
    elif cmd in ('u', 'undo'): return game.undo()
    elif cmd in ('c', 'clear'): game.clear_selection(); return ('INFO', 'Selection cleared.')
    elif cmd in ('sh', 'shuffle'): game.shuffle(); return ('INFO', 'Strands shuffled.')
    elif cmd in ('h', 'hint'): return game.hint()
    elif cmd in ('f', 'found'): return ('INFO', found summary)  # hmm, found is rendered anyway
    elif cmd in ('?', 'help'): return ('HELP', ui.help_text())
    elif cmd in ('q', 'quit'): return ('QUIT', 'Thanks for playing!')
    elif cmd in ('r', 'restart'): return ('RESTART', 'Restarting puzzle...')
    else:
        # numeric tokens: select each
        try numbers...