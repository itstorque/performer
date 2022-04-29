# from .abstract_generator import AbstractGenerator

from http.client import NotConnected


class Generator:

    def __init__(self, f_op=None, gui_handler=None, *args):
        self.gui_handler = gui_handler
        pass

    def __add__(self, g2):
        return Generator(lambda x1, x2: x1 + x2, self, g2)

    def add_gui_handler(self, gui_handler):
        self.gui_handler = gui_handler
        gui_handler.init()

    def __call__(self):
        return self

    def viz(self, name):
        if self.gui_handler == None:
            raise NotConnected("No gui_handler defined")

        import PySimpleGUI as sg

        layout = [  [sg.Text('GENERATOR ' + name)],
            [sg.Slider(orientation ='horizontal', key='slider1')],
            [sg.Button('Reset')] ]

        self.gui_handler.new_window(name, layout)

        

#Aliases
Gen = Generator
AbstractGenerator = Generator

# TODO: separate out aliases into an __alias__.py