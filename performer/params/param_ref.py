import numpy as np

class ParamRef():
    # TODO: implement a recursive reference param, i.e. x*P1 -> P2(x*P1.__float__)

    def __init__(self, param, mul=1, add=0, polyval=False) -> None:
        
        self.param = param

        self.mul = mul
        self.add = add

    def __float__(self) -> float:
        return self.param.__float__() * self.mul + self.add

    def __int__(self) -> float:
        return self.param.__int__() * self.mul + self.add

    def __mul__(self, v):
        return ParamRef(param=self.param, mul=self.mul*v, add=self.add)

    def __rmul__(self, v):
        return ParamRef(param=self.param, mul=self.mul*v, add=self.add)

    def __add__(self, v):
        return ParamRef(param=self.param, mul=self.mul, add=self.add+v)

    def __radd__(self, v):
        return ParamRef(param=self.param, mul=self.mul, add=self.add+v)

    def set(self, val):
        self.val = val

    def get(self):
        return self.val
