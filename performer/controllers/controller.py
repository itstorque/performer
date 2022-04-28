import time

class Controller:

    def __init__(self):
        self.items = {}
        self.pointers = {}


        self.freq_pointers = set()
        self.toggle_pointers = set()

    def attach(self, item, param, init_value=None):
        if init_value==None: item.get_param(param)
        self.items[item] = {param: init_value}

    def attach_value(self, pointer):
        self.pointers.append(pointer)

    def attach_freq(self, pointer):
        self.freq_pointers.add(pointer)

    def attach_toggle(self, pointer):
        self.toggle_pointers.add(pointer)

    def init(self):
        pass
        # self.

    def write(self, idx, value):
        self.pointers[idx][0] = value

    def update(self):
        time.sleep(0.001)