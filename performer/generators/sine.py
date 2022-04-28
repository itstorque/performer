import numpy as np

from .generator import Generator

class Sin(Generator):
    programmed_fs = 44100

    SIN = np.sin(2*np.pi* np.arange(0, programmed_fs*2)/programmed_fs)

    def __init__(self):
        super().__init__(f_op=None)

    def generate(self, t, fs):

        if fs!=self.programmed_fs:
            self.SIN = np.sin(2*np.pi* np.arange(0, self.programmed_fs*2)/self.programmed_fs)
            self.programmed_fs = fs

        # return np.sin(2*np.pi* t /fs)

        return self.SIN[t.astype(int) % fs*2]


# Aliases
Sine = Sin