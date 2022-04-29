import numpy as np
from scipy.signal import square

from .generator import Generator

class Square(Generator):
    # TODO: duty cycle, frequency
    # TODO: implement this

    def __init__(self, duty=0.5):
        super().__init__(f_op=None)

        self.duty = duty

    def generate(self, t, fs):
        return 2*square(2 * np.pi * t, duty=self.duty.__float__()) - 1


Sq = Square
Rect = Square