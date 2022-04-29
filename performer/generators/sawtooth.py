import numpy as np
from scipy.signal import sawtooth

from .generator import Generator

class Sawtooth(Generator):
    # TODO: duty cycle, frequency
    # TODO: implement this
    programmed_fs = 44100

    SAW = sawtooth(2*np.pi* np.arange(0, programmed_fs*2)/programmed_fs)

    def __init__(self):
        super().__init__(f_op=None)

    def generate(self, t, fs):

        if fs!=self.programmed_fs:
            self.SIN = np.sin(2*np.pi* np.arange(0, self.programmed_fs*2)/self.programmed_fs)
            self.programmed_fs = fs

        return self.SAW[t.astype(int) % fs*2] 
        
        # return sawtooth(2 * np.pi * 5 * t)


Saw = Sawtooth