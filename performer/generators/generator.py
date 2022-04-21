# from .abstract_generator import AbstractGenerator

class Generator:

    def __init__(self, f_op=None, *args):
        pass

    def __add__(self, g2):
        return Generator(lambda x1, x2: x1 + x2, self, g2)

#Aliases
Gen = Generator
AbstractGenerator = Generator

# TODO: separate out aliases into an __alias__.py