import numpy as np

class Signal:

    def __init__(self, init_value=0, dtype=np.float32):
        self.value = dtype(init_value)

        self.dtype = dtype

    def set(self, value):
        self.value = self.dtype(value)

    def get(self):
        return self.value

    def amimate(self):
        #TODO: implement animated params
        pass