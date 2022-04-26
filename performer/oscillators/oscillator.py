class Oscillator:

    def __init__(self, audio, controller=None, volume=1, child_osc=[]):

        if audio:
            self.audio = audio
            audio.attach_voice(self)

        self.controller = controller

        self.annimatable_param = {}

        self.current_index = 0

        self.child_osc = child_osc

        self.idx_identity = None

        self.multiplier = volume
        self.offset = 0

    def next(self, buffer_size=None):

        self.current_index += 1

        if self.idx_identity: self.current_index = self.current_index % self.idx_identity

        if buffer_size==None: buffer_size = self.audio.buffer_size()

        return self._next(buffer_size=buffer_size, fs=self.audio.fs, sample_index=self.current_index)

    # note factors can be either ints or other osc objects

    def __add__(self, factor):
        # TODO: implement audio, controller merge for sum of separate sources/controllers

        if type(factor) in {int, float}: self.offset += factor

        return Oscillator(audio=None, controller=None, child_osc=[self, factor])

    def __radd__(self, factor):
        return self.__add__(factor)

    def __mul__(self, factor):
        if type(factor) in {int, float}: self.multiplier *= factor
        return self

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def _apply_consts(self, signal):
        return self.offset + self.multiplier * signal

    def _next(self, buffer_size, fs, sample_index):
        return self._apply_consts( sum([i._next(buffer_size, fs, sample_index) for i in self.child_osc]) )