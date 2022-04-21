import numpy as np

from .oscillator import Oscillator

from ..generators.sine import Sine

class LFO(Oscillator):
    # TODO: maybe add windowing to remove clicks

    def __init__(self, audio, f, envelope=None, controller=None, type="sin"):
        #TODO: implement envelope classes
        
        super().__init__(audio, controller)

        self.annimatable_param["f"] = f
        self.envelope = envelope
        
        self.prev_f = f

        self.f_op = Sine()

    def cycle(self):
        yield 

    def _next(self, buffer_size, fs, sample_index):
        idxs = np.arange(buffer_size) + (sample_index-1)*buffer_size

        idxs += int(self.annimatable_param["f"] - self.prev_f)

        return self.f_op.generate(t = ( idxs * self.prev_f/fs )  )

    def change_param(self, param, value):
        self.annimatable_param[param] = value