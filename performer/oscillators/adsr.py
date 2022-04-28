import threading
import numpy as np

from .oscillator import Oscillator

class ADSR(Oscillator):

    def __init__(self, input, audio, A=0.5, D=0.5, S=0.4, R=0.5, controller=None):
        from time import time

        super().__init__(audio, controller)

        self.input = input
        self.amp = 0

        self.rising_amp, self.falling_amp = self.amp, self.amp

        self.A = A
        self.D = D
        self.S = S
        self.R = R
        
        self.Amax = 1

        self.on = False
        self.timer = 0

        self.adsr_thread = None

    def toggle(self, on):
        from time import time

        self.on = on
        self.timer = time()

        self.adsr_thread = threading.Thread(target=self.calc_amp)
        self.adsr_thread.start()

    def calc_amp(self):
        from time import time, sleep
        
        while True:
            T = time() - self.timer

            print(self.on, self.amp, T, " "*20, end="\r")

            if self.on:

                if T <= self.A: 
                    self.amp = np.interp(T, [0, self.A], [self.falling_amp, self.Amax])
                elif T <= self.D + self.A:
                    self.amp = np.interp(T, [self.A, self.A+self.D], [self.Amax, self.S])
                else:
                    self.amp = self.S

                self.rising_amp = self.amp
            
            else:

                if T <= self.R:
                    self.amp = np.interp(T, [0, self.R], [self.rising_amp, 0])
                else:
                    self.amp = 0

                self.falling_amp = self.amp

            # sleep(0.00001)

    def _next(self, buffer_size, fs, sample_index):
        return self.amp*self.input._next(buffer_size, fs, sample_index)