class Oscillator:

    def __init__(self, audio, controller=None, child_osc=[]):

        if audio:
            self.audio = audio
            audio.attach_voice(self)

        self.controller = controller

        self.annimatable_param = {}

        self.current_index = 0

    def next(self, buffer_size=None):

        self.current_index += 1

        if buffer_size==None: buffer_size = self.audio.buffer_size()

        return self._next(buffer_size=buffer_size, fs=self.audio.fs, sample_index=self.current_index)

    def __add__(self, osc2):
        # TODO: implement audio, controller merge for sum of separate sources/controllers

        return Oscillator(audio=None, controller=None, child_osc=[self, osc2])

    def _next(self, buffer_size, fs, sample_index):
        return sum({i._next(buffer_size, fs, sample_index) for i in self.child_osc})