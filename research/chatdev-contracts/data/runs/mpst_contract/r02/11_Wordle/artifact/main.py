#!/usr/bin/env python3
"""Terminal Wordle. Run: python3 main.py [optional custom 5-letter word]"""
import sys
from wordle import play

if __name__ == "__main__":
    play(sys.argv[1] if len(sys.argv) > 1 else None)