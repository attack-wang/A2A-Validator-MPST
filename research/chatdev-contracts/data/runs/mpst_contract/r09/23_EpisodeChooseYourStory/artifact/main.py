"""Entry point for 'The Hollow Crown' interactive story game."""
import sys

from engine import GameEngine
from story_data import STORY, START


def main() -> int:
    GameEngine(STORY, START).run()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nFarewell, traveller.")
        sys.exit(0)