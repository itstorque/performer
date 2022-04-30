import time

class Controller:

    def __init__(self, func=None, **kwargs):
        self.items = {}
        self.pointers = {}


        self.freq_pointers = set()
        self.toggle_pointers = set()
        self.adsr_pointers = set()

        self.named_params = {}

        self.abstract_func = func

        for k, v in kwargs.items():
            setattr(self, k, v)

    def attach(self, item, param, init_value=None):
        if init_value==None: item.get_param(param)
        self.items[item] = {param: init_value}

    def attach_value(self, pointer):
        self.pointers.append(pointer)

    def attach_freq(self, pointer):
        self.freq_pointers.add(pointer)

    def attach_toggle(self, pointer):
        self.toggle_pointers.add(pointer)

    def attach_param(self, param):
        if param.name == None: 
            print("Give parameter a name to be able to attach it.")
            raise IndexError

        self.named_params[param.name] = param

    def set_param(self, name, val):

        self.named_params[name].set(val)

    def toggle(self, on=None):

        if on==None: on = not list(self.toggle_pointers)[0].__int__()

        for toggle in self.toggle_pointers:
            toggle.set(1 if on else 0)

    def set_freq(self, freq):

        for freqptr in self.freq_pointers:
            freqptr.set(freq)

    # def attach_adsr(self, pointer):
    #     self.adsr_pointers.add(pointer)

    # def run_adsr(self):
    #     return

    def init(self):
        pass
        # self.

    def write(self, idx, value):
        self.pointers[idx][0] = value

    def update(self):
        time.sleep(0.001)
        if self.abstract_func: self.abstract_func(self)