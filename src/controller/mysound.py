import time

from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_ffpyplayer import *
from ffpyplayer.player import MediaPlayer


class MySound(SoundFFPy):

    def __init__(self, **kwargs):
        super(MySound, self).__init__(**kwargs)

    def load_seek(self, position):
        self._state = ''
        self.state = 'stop'
        self.quitted = False

        ff_opts = {'vn': True, 'sn': True,
                   'ar': 48000,
                   # 'ac': 2,
                   'ss': position}
        print(f"DEBUG: self._ffplayer = MediaPlayer({self.source})")
        self._ffplayer = MediaPlayer(self.source,
                                     callback=self._player_callback,
                                     loglevel='debug',
                                     ff_opts=ff_opts)
        player = self._ffplayer
        player.set_volume(self.volume)
        # player.toggle_pause()
        # self._state = 'paused'
        s = time.perf_counter()
        while (player.get_metadata()['duration'] is None and
               not self.quitted and time.perf_counter() - s < 10.):
            time.sleep(0.005)

        return self

SoundLoader._classes = []
SoundLoader.register(MySound)