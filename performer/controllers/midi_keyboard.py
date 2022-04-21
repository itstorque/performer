import pygame
import sys
from .controller import Controller

class MIDIKeyboard(Controller):
    # TODO: keydown msg to activate ADSR
    # TODO: midikey map

    current_octave = 4

    MIDDLE_C = 60
    OCTAVE_SIZE = 12

    MIDIKEYMAP = [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_e, pygame.K_d, pygame.K_f, pygame.K_t, pygame.K_g, pygame.K_y, pygame.K_h, pygame.K_u, pygame.K_j, pygame.K_k, pygame.K_o, pygame.K_l]

    def map_key_to_midi(self, keypress):
        return MIDIKEYMAP.index(keypress) + (current_octave-4) * OCTAVE_SIZE + MIDDLE_C

    def map_midi_to_freq(self, midi):
        return 2**((midi-69)/12) * 440

    def map_key_to_freq(self, keypress):
        return self.map_midi_to_freq(self.map_key_to_midi(keypress))

    def __init__(self):
        super().__init__()

        self.items = {}
        self.pointer = None

    def attach(self, item, param, init_value=None):
        if init_value==None: item.get_param(param)
        self.items[item] = {param: init_value}

    def attach_value(self, pointer):
        self.pointer = pointer
        print("ATTACHED", self.pointer)

    def init(self):
        # initialising pygame
        pygame.init()
        
        # creating display
        display = pygame.display.set_mode((300, 300))

    def update(self):
        # TODO: separate this into another controller... this is null controller
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a:
                    print("170")
                    self.write(450)

                if event.key == pygame.K_s:
                    print("240")
                    self.write(800)