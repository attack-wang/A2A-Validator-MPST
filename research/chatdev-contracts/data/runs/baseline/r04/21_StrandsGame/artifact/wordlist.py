main.py          — entry point; parses args (--gui/--console), starts game
strand.py        — Strand dataclass
puzzle.py        — Puzzle, MergeResult classes
puzzle_data.py   — BUILT_IN_PUZZLES list
wordlist.py      — COMMON_WORDS set for off-theme feedback
game_engine.py   — StrandsGame: game state machine, validation, feedback
console_ui.py    — ConsoleUI: text interface loop
gui.py           — StrandsGUI: Tkinter interface