from statistics import fmean
import numpy as np

from .oscillator import Oscillator

from ..generators.sine import *
from ..generators.square import *

class LFO(Oscillator):
    # TODO: maybe add windowing to remove clicks

    def __init__(self, audio, f, fmul=1, envelope=None, controller=None, volume=1, polyphonous=False, type="sin"):
        #TODO: implement envelope classes
        
        super().__init__(audio, controller)

        self.annimatable_param["f"] = f
        self.envelope = envelope

        self.fmul = fmul
        
        self.prev_f = f[0]

        self.idx_identity = f

        self.old_shift = 0

        self.polyphonous = polyphonous

        if type=="sin": self.f_op = Sine()
        elif type=="sin": self.f_op = Square()
        else: self.f_op = type()

    def cycle(self):
        yield 

    def _next(self, buffer_size, fs, sample_index, f_overwrite=None):
        idxs = np.arange(buffer_size, dtype=np.float32) + (sample_index-1)*buffer_size

        if f_overwrite==None: f_overwrite = self.annimatable_param["f"]

        # print(self.annimatable_param["f"], self.prev_f)
        # print(self.annimatable_param["f"] - self.prev_f)

        # phase matching
        # idxs += self.annimatable_param["f"] - self.prev_f
        phase_match = (self.prev_f - f_overwrite)*self.old_shift

        # self.prev_f += ( self.prev_f-self.annimatable_param["f"] )*np.linspace(1, )

        # if self.prev_f != self.annimatable_param["f"]:
        #     # eff_f = np.linspace(self.prev_f, min(self.prev_f+self.annimatable_param["f"]/10, self.annimatable_param["f"]), buffer_size).reshape((buffer_size))
        #     # self.prev_f = eff_f[-1]
        #     eff_f = self.prev_f
        # else:
        #     eff_f = self.prev_f

        if self.polyphonous: 

            if self.prev_f != f_overwrite:

                return self._next(self, buffer_size, fs, sample_index, self.prev_f) + self._apply_consts( self.f_op.generate(t = ( np.multiply(idxs, eff_f) + phase_match )/fs*self.fmul  ) )

        self.prev_f = f_overwrite

        eff_f = f_overwrite

        self.old_shift = idxs[-1]

        # return self._apply_consts( self.f_op.generate(t = ( np.multiply(idxs, eff_f) + phase_match )/fs*self.fmul  ) )
        return self._apply_consts( self.f_op.generate(t = ( np.multiply(idxs, eff_f) + phase_match )*self.fmul, fs = fs  ) )

    def change_param(self, param, value):
        self.annimatable_param[param] = value

        if param == "f": self.idx_identity = value