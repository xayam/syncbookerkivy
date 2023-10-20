from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_ffpyplayer import SoundFFPy
from ffpyplayer.player import MediaPlayer

from src.model.utils import DEBUG

SoundLoader._classes = []


class MySound(SoundFFPy):

    def __init__(self, **kwargs):
        super(MySound, self).__init__(**kwargs)

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
            # 'ar': 48000, # audio rate
            # 'ac': 2, # count audio channels
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
        self._ffplayer.seek(pts=position,
                            relative=False,
                            accurate=True)
        return self

SoundLoader.register(MySound)
