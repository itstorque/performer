from statistics import fmean
import numpy as np

from .oscillator import Oscillator

from ..generators.sine import *
from ..generators.square import *

class LFO(Oscillator):
    # TODO: maybe add windowing to remove clicks

    def __init__(self, audio, f, fmul=1, envelope=None, controller=None, volume=1, type="sin"):
        #TODO: implement envelope classes
        
        super().__init__(audio, controller)

        self.annimatable_param["f"] = f
        self.envelope = envelope

        self.fmul = fmul
        
        self.prev_f = f

        self.idx_identity = f

        if type=="sin": self.f_op = Sine()
        elif type=="sin": self.f_op = Square()
        else: self.f_op = type()

    def cycle(self):
        yield 

    def _next(self, buffer_size, fs, sample_index):
        idxs = np.arange(buffer_size, dtype=np.float32) + (sample_index-1)*buffer_size

        # print(self.annimatable_param["f"], self.prev_f)
        # print(self.annimatable_param["f"] - self.prev_f)

        # phase matching
        # idxs += self.annimatable_param["f"] - self.prev_f
        self.prev_f += (self.prev_f-self.annimatable_param["f"])*0.0001

        return self._apply_consts( self.f_op.generate(t = ( idxs * self.prev_f/fs )*self.fmul  ) )

    def change_param(self, param, value):
        self.annimatable_param[param] = value

        if param == "f": self.idx_identity = value