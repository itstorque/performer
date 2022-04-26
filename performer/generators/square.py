import numpy as np
from scipy.signal import square

from .generator import Generator

class Square(Generator):
    # TODO: duty cycle, frequency
    # TODO: implement this

    def __init__(self):
        super().__init__(f_op=None)

    def generate(self, t):
        return square(2 * np.pi * 5 * t)


Sq = Square
Rect = Square