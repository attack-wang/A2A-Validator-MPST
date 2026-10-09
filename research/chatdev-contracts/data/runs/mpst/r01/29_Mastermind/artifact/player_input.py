'''
player_input.py
Reads and validates the player's guesses from stdin.
- parse_guess(raw_text, palette, code_length): parses free-form text (names,
  letters, or compact letter strings) into a list of palette labels.
- get_player_guess(palette, code_length): interactive loop; converts
  quit commands, EOF and Ctrl-C into QuitGame.
'''
import re
import sys
SEPARATOR_RE = re.compile(r"[,\s]+")
QUIT_WORDS = {"quit", "exit", "q"}
class QuitGame(Exception):
    """Raised when the player asks to abandon the current game."""
def _build_maps(palette):
    token_map = {entry["label"].lower(): entry["label"] for entry in palette}
    letter_map = {entry["letter"].lower(): entry["label"] for entry in palette}
    return token_map, letter_map
def parse_guess(raw_text, palette, code_length):
    token_map, letter_map = _build_maps(palette)
    text = raw_text.strip().lower()
    if not text:
        raise ValueError("Empty input — please enter your guess.")
    if text in QUIT_WORDS:
        raise QuitGame()
    tokens = SEPARATOR_RE.split(text)
    # Allow compact form like "rgbp" when every char is a palette letter
    if len(tokens) == 1 and len(tokens[0]) > 1:
        compact = tokens[0]
        if len(compact) == code_length and all(ch in letter_map for ch in compact):
            tokens = list(compact)
    guess = []
    for tok in tokens:
        if tok in token_map:
            guess.append(token_map[tok])
        elif tok in letter_map:
            guess.append(letter_map[tok])
        else:
            raise ValueError(f"Unknown symbol '{tok}'...")
    if len(guess) != code_length:
        raise ValueError(f"Expected {code_length} symbols, got {len(guess)}.")
    return guess
def get_player_guess(palette, code_length, prompt=None):
    ...
    while True:
        try:
            raw = input(prompt)
        except EOFError:
            raise QuitGame()
        except KeyboardInterrupt:
            raise QuitGame()
        try:
            return parse_guess(raw, palette, code_length)
        except QuitGame:
            raise
        except ValueError as exc:
            print(f"  Invalid guess: {exc}")