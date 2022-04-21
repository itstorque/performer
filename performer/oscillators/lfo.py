import numpy as np

from .oscillator import Oscillator

from time import time

class LFO(Oscillator):

    def __init__(self, audio, f, envelope=None, controller=None):
        #TODO: implement envelope classes
        
        super().__init__(audio, controller)

        self.annimatable_param["f"] = f
        self.envelope = envelope

    def cycle(self):
        yield 

    def _next(self, buffer_size, fs, sample_index):
        idxs = np.arange(buffer_size) + (sample_index-1)*buffer_size
        return  np.sin( 2*np.pi* ( idxs * self.annimatable_param["f"]/fs )  )

    def change_param(self, param, value):
        self.annimatable_param[param] = value