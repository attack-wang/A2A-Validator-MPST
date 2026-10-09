'''
word_dictionary.py
Provides the word list used by the validator to recognise "real" words that
are not puzzle targets. Tries to load the operating system dictionary when
available and always falls back to a built-in list of common English words
(including the strand fragments themselves, so partial merges such as
"HOPPER" or "BUTTER" can be given meaningful feedback).
'''
import os
BUILTIN_WORDS = """
CAT DOG SUN MOON STAR RAIN BOW GRASS HOP PER KEY BOARD LAP TOP SOFT WARE NET
WORK CUP CAKE ICE CREAM DONUT CHO COLA LATE BREAK FAST BUT TER BUTTER FLY
COAT HIGH SCHOOL BUS STOP TRAFFIC LIGHT PARK ING LOT HOPPER SUNFLOWER RAINBOW
GRASSHOPPER FLOWER FLOW SNOW MAN SNOWMAN FIRE PLACE FIREFLIGHT ...
"""