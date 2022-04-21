from .oscillator import Oscillator

class ADSR(Oscillator):

    def __init__(self, input, audio, controller=None):
        super().__init__(audio, controller)

        self.input = input
        self.amp = 1

    def _next(self, buffer_size, fs, sample_index):
        return self.amp*self.input._next(buffer_size, fs, sample_index)