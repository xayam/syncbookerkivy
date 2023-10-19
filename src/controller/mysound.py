from kivy.core.audio.audio_ffpyplayer import *
from ffpyplayer.player import MediaPlayer


class MySound(SoundFFPy):

    def __init__(self, app, **kwargs):
        self.app = app
        super(MySound, self).__init__(**kwargs)

    def load_seek(self, position):
        self._state = ''
        self.state = 'stop'
        self.quitted = False

        ff_opts = {
            'vn': True,  # video mute
            'sn': True,  # subtitle mute
            'ss': position  # seek position
            # 'infbuf': True,
            # 'genpts': True,
            # 'fast': True,
            # 'ar': 48000, # audio rate
            # 'ac': 2, # count audio channels
        }
        self.app.log.debug(f"Seek position ff_opts['ss'] is {position}")
        self.app.log.debug(f"Set self._ffplayer = MediaPlayer({self.source})")
        self._ffplayer = MediaPlayer(self.source,
                                     callback=self._player_callback,
                                     loglevel='debug',
                                     ff_opts=ff_opts)
        self._state = 'playing'
        self.state = 'play'
        self._ffplayer.seek(pts=position,
                            relative=False,
                            accurate=False)
        return self
