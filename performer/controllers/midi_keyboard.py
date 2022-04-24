import threading
from pynput import keyboard

import sys
import numpy as np
import time

from .controller import Controller
from ..midi.midinote import MIDINote

# def on_press(key):
#     print('pressed', key)

# def on_release(key):
#     print('released', key)
#     if str(key) == 'Key.esc':
#         print('Exiting')
#         return False

# def sleeper():
#     global escapePressed
#     escapePressed = False
#     with keyboard.Listener(
#     on_press = on_press,
#     on_release = on_release, suppress=True) as listener:
#         escapePressed = True
#         listener.join()


class MIDIKeyboard(Controller):
    # TODO: keydown msg to activate ADSR
    # TODO: midikey map

    current_octave = 4

    MIDDLE_C = 60
    OCTAVE_SIZE = 12

    # MIDIKEYMAP = [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_e, pygame.K_d, pygame.K_f, pygame.K_t, pygame.K_g, pygame.K_y, pygame.K_h, pygame.K_u, pygame.K_j, pygame.K_k, pygame.K_o, pygame.K_l]
    MIDIKEYMAP = list("awsedftgyhujkol")

    keys_down = set()

    def map_key_to_midi(self, keypress):
        try:
            return self.MIDIKEYMAP.index(str(keypress)[1]) + (self.current_octave-4) * self.OCTAVE_SIZE + self.MIDDLE_C
        except:
            pass

    def map_midi_to_freq(self, midi):
        return 2**((midi-69)/12) * 440 if midi!=None else None

    def map_key_to_freq(self, keypress):
        return self.map_midi_to_freq(self.map_key_to_midi(keypress))

    def __init__(self, midiout=False):
        super().__init__()

        self.items = {}
        self.pointer = None

        if midiout: self.midiout = MIDINote()
        else: self.midiout = None

    def init(self):
        # initialising pynput keyboard thread
        t1 = threading.Thread(target=self.async_keylistener, name = 'pynput_keyboard_thread')
        t1.start()

    def send(self, note_down, note):
        print(note, self.map_midi_to_freq(note))
        self.write(0, self.map_midi_to_freq(note))
        for i in np.arange(0, 100, 1) if note_down else np.arange(100, 0, -1):
            self.write(1, i/100)
            time.sleep(0.00001)
        if self.midiout: self.midiout.play_note(note, 127 if note_down else 0)

    def keydown(self, key):
        if '.' in str(key): sys.exit()
        
        if key in self.keys_down: return
        self.keys_down.add(key)

        return self.send(1, self.map_key_to_midi(key))

    def keyup(self, key):
        self.keys_down.remove(key)
        return self.send(0, self.map_key_to_midi(key))

    def async_keylistener(self):
        with keyboard.Listener(on_press=self.keydown,
                               on_release=self.keyup, 
                               suppress=True)         as listener:
            pass
            listener.join()

    def update(self):
        import time
        time.sleep(0.0001)
        return
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()

        #     if event.type == pygame.KEYDOWN:

        #         midinote = self.map_key_to_midi(event.key)

        #         if midinote:
        #             print("write 1")
        #             self.send(1, midinote)

        #         # if event.key == pygame.K_a:
        #         #     print("170")
        #         #     self.write(450)

        #         # if event.key == pygame.K_s:
        #         #     print("240")
        #         #     self.write(800)

        #     if event.type == pygame.KEYUP:
        #         midinote = self.map_key_to_midi(event.key)

        #         if midinote:
        #             print("write 0")
        #             self.send(0, midinote)