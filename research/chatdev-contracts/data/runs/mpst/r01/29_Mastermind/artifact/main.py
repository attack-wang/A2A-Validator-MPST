'''
main.py
Entry point for the Mastermind game. Parses optional command-line arguments
(mode and difficulty), builds a MastermindGame session and starts it.
Run with no arguments for an interactive prompt; run
`python main.py --selftest` to execute the feedback scorer self-test.
'''
import sys
from game import MastermindGame
from game_config import MODES, DIFFICULTY_PRESETS
from feedback import _run_self_test
VALID_MODES = sorted(MODES)
VALID_DIFFICULTIES = sorted({d for presets in DIFFICULTY_PRESETS.values() for d in presets})
USAGE = ...
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--selftest" in argv:
        _run_self_test()
        return 0
    # defaults / prompt
    ...
    mode, difficulty = parse args or prompt
    game = MastermindGame(mode, difficulty)
    game.start()
    return 0
if __name__ == "__main__":
    raise SystemExit(main())