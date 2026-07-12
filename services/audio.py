try:
    from kivy.core.audio import SoundLoader
except ImportError:
    SoundLoader = None

_sounds = {}

def preload_sounds():
    for name in ('hit', 'critical', 'skill', 'death', 'victory', 'defeat'):
        sound = SoundLoader.load(f'assets/sounds/{name}.wav')
        if sound:
            _sounds[name] = sound

def play_sound(name):
    sound = _sounds.get(name)
    if sound:
        sound.play()
