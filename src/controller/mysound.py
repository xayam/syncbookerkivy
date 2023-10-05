from kivy.core.audio.audio_ffpyplayer import SoundFFPy
from ffpyplayer.player import MediaPlayer


class MySound(SoundFFPy):
    def __init__(self, **kwargs):
        self._ffplayer = None
        super(MySound, self).__init__(**kwargs)

    def load_seek(self, source, position):
        self.source = source
        # print("DEBUG: self.unload()")
        # self.unload()
        ff_opts = {'vn': True, 'sn': True, 'ss': position}
        print("DEBUG: self._ffplayer = MediaPlayer()")
        self._ffplayer = MediaPlayer(self.source,
                                     callback=self._player_callback,
                                     loglevel='debug', ff_opts=ff_opts)
        # player = self._ffplayer
        # player.toggle_pause()
        # self._state = 'paused'
        return self
