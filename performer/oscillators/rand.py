import numpy as np

from .oscillator import Oscillator

class Random(Oscillator):
    # TODO: maybe add windowing to remove clicks

    def __init__(self, rate=8, range=(0, 1), audio=None, controller=None, volume=1, child_osc=...):
        super().__init__(audio, controller, volume, child_osc)

        self.rate = rate

        self.shift = 1

    def _next(self, buffer_size, fs, sample_index):
        idxs = np.arange(buffer_size, dtype=np.float32) + (sample_index-1)*buffer_size

        K = np.where((sample_index+idxs) > self.shift*fs/self.rate, 0, 255)

        print(K)

        if K[-1] != K[0]:
            self.shift += 1

        return (sample_index+idxs)/fs

RNG = Random
Rng = Random
Rand = Random