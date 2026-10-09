'''
sound.py
SoundManager: generates all sound effects procedurally (square beeps and
noise bursts) with the pygame mixer, so the game needs no external audio
files. If no audio device is available the manager silently disables
itself and the game keeps running without sound.
'''