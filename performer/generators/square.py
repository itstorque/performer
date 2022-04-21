import numpy as np

from .generator import Generator

class Square(Generator):
    # TODO: duty cycle, frequency
    # TODO: implement this

    def __init__(self):
        super().__init__(f_op=None)

    def generator(self, *args, **kwargs):
        return np.sin(*args, **kwargs)


Sq = Square
Rect = Square