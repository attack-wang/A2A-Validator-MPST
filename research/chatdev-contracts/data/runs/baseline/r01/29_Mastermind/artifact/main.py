'''
main.py
Entry point and game loop for the Mastermind code-breaking game.
The computer secretly generates a color code; the player has a limited
number of attempts to crack it. After every guess the game prints
exact/partial feedback pegs and announces a clear win/lose outcome.
Invalid input never consumes an attempt; the player may quit mid-game
with 'q' (the secret is then revealed). All prompts go through a
safe_input() wrapper so that EOF or Ctrl-C (e.g. non-interactive runs
with closed or redirected stdin) exits gracefully instead of raising
an unhandled EOFError.
'''
import random
import sys
from feedback import calculate_feedback, format_feedback
from colors import enable_colors, colorize, BOLD, GREEN, RED, RESET
# Playable color symbols (ASCII-safe so any terminal works).
COLOR_SYMBOLS = ["R", "O", "Y", "G", "B", "P", "W", "K"]
# Difficulty presets: code length, palette size, attempt budget, duplicate rule.
DIFFICULTY_PRESETS = {
    "easy":     {"code_length": 4, "num_colors": 4, "max_attempts": 12, "allow_duplicates": False},
    "standard": {"code_length": 4, "num_colors": 6, "max_attempts": 10, "allow_duplicates": True},
    "hard":     {"code_length": 5, "num_colors": 8, "max_attempts": 12, "allow_duplicates": True},
}
def safe_input(prompt):
    """input() wrapper that returns None on EOF/Ctrl-C instead of crashing."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return None
def choose_difficulty():
    """Prompt for a difficulty preset; Enter selects Standard; EOF exits cleanly."""
    print("Select difficulty:")
    names = list(DIFFICULTY_PRESETS)
    for i, (name, preset) in enumerate(DIFFICULTY_PRESETS.items(), start=1):
        print(f"  {i}) {name.capitalize():8s} - code length {preset['code_length']}, "
              f"{preset['num_colors']} colors, {preset['max_attempts']} attempts"
              f"{'' if preset['allow_duplicates'] else ', no repeats'}")
    choice = safe_input(f"Choose 1-{len(names)} [default: 2]: ")
    if choice is None:
        # EOF/Ctrl-C with no input available: exit gracefully, no traceback.
        print("\nNo input available - exiting.")
        sys.exit(0)
    choice = choice.strip()
    if choice == "":
        return DIFFICULTY_PRESETS["standard"]
    try:
        index = int(choice) - 1
    except ValueError:
        index = -1
    if 0 <= index < len(names):
        return DIFFICULTY_PRESETS[names[index]]
    print("Invalid choice - using Standard.")
    return DIFFICULTY_PRESETS["standard"]
def generate_secret(preset):
    """Generate the hidden code per the preset's palette and duplicate rule."""
    pool = COLOR_SYMBOLS[: preset["num_colors"]]
    if preset["allow_duplicates"]:
        return [random.choice(pool) for _ in range(preset["code_length"])]
    return random.sample(pool, preset["code_length"])
def parse_guess(raw, preset):
    """Validate raw input; return a list of color symbols, or None when invalid."""
    guess = list(raw.strip().upper().replace(" ", ""))
    pool = COLOR_SYMBOLS[: preset["num_colors"]]
    if len(guess) != preset["code_length"]:
        return None
    if any(ch not in pool for ch in guess):
        return None
    if not preset["allow_duplicates"] and len(set(guess)) != len(guess):
        return None
    return guess
def render_guess(guess):
    """Return the guess as a colorized, space-separated peg string."""
    return " ".join(colorize(ch, ch) for ch in guess)
def play_game(preset):
    """Run one full game: secret generation, guess loop, and win/lose outcome."""
    secret = generate_secret(preset)
    length = preset["code_length"]
    max_attempts = preset["max_attempts"]
    pool = COLOR_SYMBOLS[: preset["num_colors"]]
    print(f"\nI have chosen a secret code of {length} colors "
          f"from: {' '.join(colorize(c, c) for c in pool)}")
    print("Feedback pegs: '*' = exact (right color, right position), "
          "'o' = partial (right color, wrong position).")
    print("Type 'q' at any prompt to quit and reveal the secret.\n")
    attempts_used = 0
    while attempts_used < max_attempts:
        raw = safe_input(f"Attempt {attempts_used + 1}/{max_attempts} - your guess: ")
        # EOF is treated exactly like the 'q' quit command.
        if raw is None or raw.strip().lower() in ("q", "quit"):
            print(f"You gave up. The secret code was: {render_guess(secret)}")
            return
        guess = parse_guess(raw, preset)
        if guess is None:
            print(f"  Invalid guess: enter exactly {length} symbols from {''.join(pool)}"
                  + ("" if preset["allow_duplicates"] else ", without repeats.")
                  + " Invalid input does not consume an attempt.")
            continue
        attempts_used += 1
        exact, partial = calculate_feedback(guess, secret)
        print(f"  {render_guess(guess)} -> {format_feedback(exact, partial, length)}")
        if exact == length:
            print(f"\n{GREEN}{BOLD}Code cracked in {attempts_used} "
                  f"attempt{'s' if attempts_used != 1 else ''} - YOU WIN!{RESET}")
            return
    print(f"\n{RED}{BOLD}Out of attempts - YOU LOSE!{RESET} "
          f"The secret code was: {render_guess(secret)}")
def main():
    """Entry point: enable colors, run games until the player quits or EOF."""
    enable_colors()
    print(f"{BOLD}=== Mastermind ==={RESET}")
    while True:
        preset = choose_difficulty()
        play_game(preset)
        again = safe_input("\nPlay again? [y/N]: ")
        # EOF is treated as "don't play again".
        if again is None or again.strip().lower() != "y":
            print("Thanks for playing - goodbye!")
            break
if __name__ == "__main__":
    main()