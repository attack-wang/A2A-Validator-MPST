'''
main.py — Entry point for "The Lantern of Eldermere",
an interactive storytelling game.
Run with:  python main.py
Optional:  python main.py --story path/to/story.json
'''
import sys
from game import Game
def parse_args(argv):
    story_path = "story_data.json"
    if "--story" in argv:
        idx = argv.index("--story")
        if idx + 1 < len(argv):
            story_path = argv[idx + 1]
    return story_path
def main():
    story_path = parse_args(sys.argv)
    game = Game(story_path=story_path)
    game.start()
if __name__ == "__main__":
    main()