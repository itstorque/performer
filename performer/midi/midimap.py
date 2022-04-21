# TODO:  find a better way to manage MIDI key input and midi devices?
# TODO: maybe restructure midi folder to become mididevices??
import pygame

current_octave = 4

MIDDLE_C = 60
OCTAVE_SIZE = 12

MIDIKEYMAP = [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_e, pygame.K_d, pygame.K_f, pygame.K_t, pygame.K_g, pygame.K_y, pygame.K_h, pygame.K_u, pygame.K_j, pygame.K_k, pygame.K_o, pygame.K_l]

m = MIDIKEYMAP.index(pygame.K_k) + (current_octave-4) * OCTAVE_SIZE + MIDDLE_C

fm = 2**((m-69)/12) * 440

print(m, fm)