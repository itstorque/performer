class Oscillator:

    def __init__(self, audio, controller):

        self.audio = audio
        self.controller = controller

        audio.attach_voice(self)

        self.annimatable_param = {}

        self.current_index = 0

    def next(self, buffer_size=None):

        self.current_index += 1

        if buffer_size==None: buffer_size = self.audio.buffer_size()

        return self._next(buffer_size=buffer_size, fs=self.audio.fs, sample_index=self.current_index)