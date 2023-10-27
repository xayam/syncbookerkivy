from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_ffpyplayer import SoundFFPy
import ffpyplayer
from ffpyplayer.player import MediaPlayer
from ffpyplayer.tools import set_log_callback, get_log_callback, formats_in

from src.model.utils import DEBUG


class MySound(SoundFFPy):

    def __init__(self, **kwargs):
        super(MySound, self).__init__(**kwargs)
        self.ffplayer = None

    def load_seek(self, position):
        self._state = ''
        self.state = 'stop'
        self.quitted = False

        ff_opts = {
            'vn': True,  # video disable
            'sn': True,  # subtitle disable
            'ss': position,  # seek position
            # 'infbuf': True,
            # 'genpts': True,
            # 'fast': True,
            'ar': 16000,  # audio rate
            'ac': 1,  # count audio channels
        }
        if DEBUG:
            print(f"[MYDEBUG] Seek position ff_opts['ss'] is {position}")
            print(f"[MYDEBUG] Set self._ffplayer = MediaPlayer({self.source})")
        self._ffplayer = MediaPlayer(self.source,
                                     callback=self._player_callback,
                                     loglevel='debug',
                                     ff_opts=ff_opts)
        self._state = 'playing'
        self.state = 'play'
        self.ffplayer = self._ffplayer
        if DEBUG:
            print(f"[MYDEBUG] Seek ffplayer")
        self.ffplayer.seek(pts=position,
                           seek_by_bytes=False,
                           relative=False,
                           accurate=True)
        if DEBUG:
            print(f"[MYDEBUG] Exit from function 'load_seek()'")
        return self


SoundLoader._classes = []
SoundLoader.register(MySound)
