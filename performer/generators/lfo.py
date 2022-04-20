import numpy as np

from .generator import Generator

class LFO(Generator):

    def __init__(self, audio, f, envelope=None, controller=None):
        #TODO: implement envelope classes
        
        super().__init__(audio, controller)

        self.f = f
        self.envelope = envelope

    def cycle(self):
        yield 

    def _next(self, buffer_size, fs):
        return np.sin( 2*np.pi* np.arange(buffer_size) * self.f/fs )