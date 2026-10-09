class SoundManager:
    def __init__(self):
        try init mixer; generate tones:
        - swap: short blip 300Hz
        - invalid: low buzz 150Hz
        - match: pleasant pop (rising)
        - special: chime
        - cascade: pitch rises with level
        - win/lose jingles: short sequences
    def play(name)