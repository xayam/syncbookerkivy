import time
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_ffpyplayer import SoundFFPy
from ffpyplayer.player import MediaPlayer


class MySound(SoundFFPy):
    def __init__(self, **kwargs):
        super(MySound, self).__init__(**kwargs)

    def load(self):
        self.unload()
        ff_opts = {'vn': True, 'sn': True, 'ar': 16000}  # only audio
        self._ffplayer = MediaPlayer(self.source,
                                     callback=self._player_callback,
                                     loglevel='info', ff_opts=ff_opts)
        player = self._ffplayer
        player.set_volume(self.volume)
        player.toggle_pause()
        self._state = 'paused'
        # wait until loaded or failed, shouldn't take long, but just to make
        # sure metadata is available.
        s = time.perf_counter()
        while (player.get_metadata()['duration'] is None and
               not self.quitted and time.perf_counter() - s < 10.):
            time.sleep(0.005)


SoundLoader._classes = []
SoundLoader.register(MySound)
