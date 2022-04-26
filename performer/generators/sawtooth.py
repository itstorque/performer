import numpy as np
from scipy.signal import sawtooth

from .generator import Generator

class Sawtooth(Generator):
    # TODO: duty cycle, frequency
    # TODO: implement this

    def __init__(self):
        super().__init__(f_op=None)

    def generate(self, t):
        return sawtooth(2 * np.pi * 5 * t)


Saw = Sawtooth