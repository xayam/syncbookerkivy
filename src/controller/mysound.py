from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_ffpyplayer import *
from ffpyplayer.player import MediaPlayer

from src.model.utils import DEBUG


class MySound(SoundFFPy):

    def __init__(self, **kwargs):
        super(MySound, self).__init__(**kwargs)

    def load_seek(self, position):
        self._state = ''
        self.state = 'stop'
        self.quitted = False

        ff_opts = {'vn': True, 'sn': True,
                   # 'ar': 48000,
                   # 'ac': 2,
                   'ss': position
                   }
        if DEBUG:
            print(f"DEBUG: self._ffplayer = MediaPlayer({self.source})")
        self._ffplayer = MediaPlayer(self.source,
                                     callback=self._player_callback,
                                     loglevel='debug',
                                     ff_opts=ff_opts)
        self._state = 'playing'
        self.state = 'play'
        return self

SoundLoader._classes = []
SoundLoader.register(MySound)