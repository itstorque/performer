from statistics import fmean
import numpy as np

from .lfo import LFO

from ..generators.sine import *
from ..generators.square import *

class PolyLFO(LFO):
    # TODO: maybe add windowing to remove clicks

    def __init__(self, audio, f, fmul=1, envelope=None, controller=None, volume=1, type="sin"):
        self.DATA = lambda freq: (audio, freq, fmul, envelope, controller, volume, True, type)

        super().__init__(audio, f, fmul, envelope, controller, volume, polyphonous=True, type=type)

        self.freqs = {}

    def cycle(self):
        yield 

    def _next(self, buffer_size, fs, sample_index, f_overwrite=None):

        if self.f not in self.freqs:
            self.freqs[self.f] = LFO(self.DATA(self.f))

        return sum([lfo._next(self,buffer_size, fs, sample_index) for lfo in self.LFOs])

    def change_param(self, param, value):
        self.annimatable_param[param] = value

        if param == "f": self.idx_identity = value