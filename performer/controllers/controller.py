import time

class Controller:

    def __init__(self):
        self.items = {}
        self.pointers = {}

    def attach(self, item, param, init_value=None):
        if init_value==None: item.get_param(param)
        self.items[item] = {param: init_value}

    def attach_value(self, pointer):
        self.pointers.append(pointer)

    def init(self):
        pass
        # self.

    def write(self, idx, value):
        self.pointers[idx][0] = value

    def update(self):
        time.sleep(0.001)