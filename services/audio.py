import os
try:
    from kivy.core.audio import SoundLoader
except ImportError:
    SoundLoader = None

_sounds = {}

def preload_sounds():
    sound_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'sounds')
    sound_files = {
        'hit': os.path.join(sound_dir, 'hit.wav'),
        'critical': os.path.join(sound_dir, 'critical.wav'),
        'skill': os.path.join(sound_dir, 'skill.wav'),
        'death': os.path.join(sound_dir, 'death.wav'),
        'victory': os.path.join(sound_dir, 'victory.wav'),
        'defeat': os.path.join(sound_dir, 'defeat.wav'),
    }
    for name, path in sound_files.items():
        if os.path.exists(path):
            sound = SoundLoader.load(path)
            if sound:
                _sounds[name] = sound

def play_sound(name):
    sound = _sounds.get(name)
    if sound:
        sound.play()
