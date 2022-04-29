from statistics import fmean
import numpy as np

from .oscillator import Oscillator

from ..generators.sine import *
from ..generators.square import *

class LFO(Oscillator):
    # TODO: maybe add windowing to remove clicks -> no need anymore?

    def __init__(self, audio=None, f=100, fmul=1, envelope=None, controller=None, volume=1, polyphonous=False, type=Sine):
        #TODO: implement envelope classes
        
        super().__init__(audio, controller, volume=volume)

        self.freq = f
        self.envelope = envelope

        self.fmul = fmul
        
        self.prev_f = f.__float__()

        self.idx_identity = f

        self.old_shift = 0

        self.polyphonous = polyphonous

        self.f_op = type()

        self.last_idx_modulation = 0

    def _next(self, buffer_size, fs, sample_index, f_overwrite=None):
        #TODO: use an if statement not a try :p

        idxs = np.arange(buffer_size, dtype=np.float32) + (sample_index-1)*buffer_size

        if f_overwrite==None: f_overwrite = self.freq.__float__()

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

        # if self.polyphonous: 

        #     if self.prev_f != f_overwrite:

        #         return self._next(self, buffer_size, fs, sample_index, self.prev_f) + self._apply_consts( self.f_op.generate(t = ( np.multiply(idxs, eff_f) + phase_match )/fs*self.fmul  ) )

        self.prev_f = f_overwrite

        eff_f = f_overwrite

        self.old_shift = idxs[-1]

        # print(f_overwrite)

        try: 
            
            eff_f[-1]
            
            idxs = np.cumsum(self.freq.next(buffer_size)) + self.last_idx_modulation
            
            self.last_idx_modulation = idxs[-1]

            # print(np.multiply(idxs, eff_f)[-1])

            # return np.multiply(idxs, eff_f)/fs

        except: 
            
            idxs *= eff_f

        # print('f', f_overwrite)

        # print('e', np.multiply(idxs, eff_f))

        # return self._apply_consts( self.f_op.generate(t = ( np.multiply(idxs, eff_f) + phase_match )/fs*self.fmul  ) )

        return self._apply_consts( self.f_op.generate(t = ( idxs + phase_match )*self.fmul, fs = fs  ) )