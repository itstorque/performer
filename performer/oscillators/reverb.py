import threading
import numpy as np

from .oscillator import Oscillator

class Reverb(Oscillator):

    def __init__(self, input, delay=0.2, feedback=0, wet_to_dry_ratio=0.5, audio=None, controller=None, volume=1, multiplier=1, offset=0, child_osc=...):
        # TODO: currently can only deal with 10sec delay, shorter delays are unoptimized, can use a resizing version of allocation for self.*******_sample
        
        super().__init__(audio, controller, volume, multiplier, offset, child_osc)

        self.input = input

        self.buffer_size = self.audio.fs*100

        self.delayed_sample = np.zeros(self.buffer_size, dtype=np.float32)
        self.current_sample = np.array([0], dtype=np.float32)

        self.feedback = feedback
        self.delay = delay

        self.wet_to_dry_ratio = wet_to_dry_ratio

        self.buffer_pointer = int(self.delay.__float__() * self.audio.fs)

    def _next(self, buffer_size, fs, sample_index):
        self.current_sample = self.input.next(buffer_size)

        # self.delayed_sample *= self.feedback
        # self.delayed_sample += self.current_sample

        self.buffer_pointer = (self.buffer_pointer + np.shape(self.current_sample)[0]) % (self.buffer_size - np.shape(self.current_sample)[0])

        delay_index = int(self.delay.__float__() * self.audio.fs)
        # delay_index=0

        self.delayed_sample[self.buffer_pointer+delay_index:
                            self.buffer_pointer+delay_index+np.shape(self.current_sample)[0]] = self.current_sample

        return (1-self.wet_to_dry_ratio) * self.current_sample + self.wet_to_dry_ratio * self.delayed_sample[self.buffer_pointer:
                            self.buffer_pointer+np.shape(self.current_sample)[0]]