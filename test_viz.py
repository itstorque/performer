from performer import *
from performer.controllers.gui_handler import GUIHandler

guihandler = GUIHandler()

gen = Generator(gui_handler=guihandler)

gen.viz()