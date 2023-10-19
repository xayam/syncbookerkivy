import time

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

        ff_opts = {
            'vn': True,  # video mute
            'sn': True,  # subtitle mute
            'ss': position  # seek position
            # 'ar': 48000, # audio rate
            # 'ac': 2, # count audio channel
        }
        if DEBUG:
            print(f"[MYDEBUG] Seek position ff_opts['ss'] is {position}")
            print(f"[MYDEBUG] Set self._ffplayer = MediaPlayer({self.source})")
        self._ffplayer = MediaPlayer(self.source,
                                     callback=self._player_callback,
                                     loglevel='debug',
                                     ff_opts=ff_opts)
        player = self._ffplayer
        self._state = 'playing'
        self.state = 'play'

        s = time.perf_counter()
        while (player.get_metadata()['duration'] is None and
               not self.quitted and time.perf_counter() - s < 10.):
            time.sleep(0.005)

        return self


SoundLoader._classes = []
SoundLoader.register(MySound)
