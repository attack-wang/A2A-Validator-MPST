def main():
    print banner
    validate all puzzles at load (unique solution check) — raise/report if any fails
    for each puzzle:
        run game loop
        on completion: celebration + stats (merges attempted, valid, hints used)
        prompt next or quit
    goodbye