'''
banner.py
Title banner for the Mastermind game.
Builds the ASCII banner once at import time using bold() from the
colors module, so main.py can simply import BANNER.
'''
from colors import bold
BANNER = bold(r"""
========================================
   M A S T E R M I N D  -  Code Breaker
========================================
""")