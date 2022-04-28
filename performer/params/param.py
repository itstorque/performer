import numpy as np

from .param_ref import ParamRef

class Param():
    # TODO: implement a recursive reference param, i.e. x*P1 -> P2(x*P1.__float__)

    def __init__(self, val, name="", polyval=False) -> None:
        self.name = name
        self.val = val

    def __float__(self) -> float:
        return self.val.__float__()

    def __int__(self) -> float:
        return self.val.__int__()

    def __mul__(self, v) -> ParamRef:
        return ParamRef(self, mul=v)

    def __rmul__(self, v) -> ParamRef:
        return ParamRef(self, mul=v)

    def __add__(self, v) -> ParamRef:
        return ParamRef(self, add=v)

    def __radd__(self, v) -> ParamRef:
        return ParamRef(self, add=v)

    def set(self, val):
        self.val = val

    def get(self):
        return self.val
