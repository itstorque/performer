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

    # TODO: check if introducing eq and hash created bugs
    def __eq__(self, __o: object) -> bool:
        return __o in {self.__float__, self.__int__, self}

    def __hash__(self):
        return hash(self.val)

    def set(self, val):
        self.val = val

    def get(self):
        return self.val

    def _next(self, *args, **kwargs): 
        # throw inputs since _next means some object thinks
        # a Param object is a generator object.
        return self.__float__()
