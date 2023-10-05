import os
from kivy.core.audio.audio_ffpyplayer import SoundFFPy
from ffpyplayer.player import MediaPlayer


class MySound(SoundFFPy):
    def __init__(self, **kwargs):
        self._ffplayer = None
        super(MySound, self).__init__(**kwargs)

    def load_seek(self, source, position):
        # self.source = os.path.abspath(source)
        # print("DEBUG: self.unload()")
        # self.unload()
        ff_opts = {'vn': True, 'sn': True, 'ar': 48000, 'ac': 2, 'ss': position}
        print(f"DEBUG: self._ffplayer = MediaPlayer({os.path.abspath(source)})")
        self._ffplayer = MediaPlayer(os.path.abspath(source),
                                     # callback=self._player_callback,
                                     loglevel='debug',
                                     ff_opts=ff_opts)
        return self
