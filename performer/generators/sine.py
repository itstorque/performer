import numpy as np

from .generator import Generator

class Sin(Generator):
    # TODO: frequency

    def __init__(self):
        super().__init__(f_op=None)

    def generate(self, t):
        return np.sin(2*np.pi* t)


# Aliases
Sine = Sin