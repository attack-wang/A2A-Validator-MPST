import sys

from game import play

if __name__ == "__main__":
    play(random_mode="--random" in sys.argv)