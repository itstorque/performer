import threading
from pynput import keyboard

import sys
from subprocess import call
import os

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
    current_vel = 127

    MIDDLE_C = 60
    OCTAVE_SIZE = 12

    MIDIKEYMAP = list("awsedftgyhujkol")

    keys_down = set()

    def oct_down(self):
        self.current_octave -= 1
        print("OCTAVE:", self.current_octave, " "*20, "\n")

    def oct_up(self):
        self.current_octave += 1
        print("OCTAVE:", self.current_octave, " "*20, "\n")

    def vel_down(self):
        self.current_vel -= 1

    def vel_up(self):
        self.current_vel += 1

    MIDICONTROLMAP = {"z": oct_down, "x": oct_up, "c": vel_down, "v": vel_up }

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

        self.envelopes = set()

        self.all_freqs = set()

    def init(self):
        # initialising pynput keyboard thread
        t1 = threading.Thread(target=self.async_keylistener, name = 'pynput_keyboard_thread')
        t1.start()

    def attach_envelope(self, envelope):
        self.envelopes.add(envelope)

    def note_down(self, midinote):

        freq = self.map_midi_to_freq(midinote)

        if freq == None: return

        for freqptr in self.freq_pointers:
            freqptr.set(freq)

            print(freqptr.__float__())

        # self.all_freqs.add()

        if self.midiout: self.midiout.play_note(midinote, self.current_vel)

        return

    def note_up(self, midinote):

        return

    def keydown(self, key):
        
        if key == keyboard.Key.media_volume_up:
            call(['osascript -e "set volume output volume (output volume of (get volume settings) + 10) --100%"'], shell=True)
            print(os.system('osascript -e "get volume settings"'))
        
        if key == keyboard.Key.media_volume_down:
            call(['osascript -e "set volume output volume (output volume of (get volume settings) - 10) --100%"'], shell=True)
            print(os.system('osascript -e "get volume settings"'))

        if 'esc' in str(key): return sys.exit()
        if '.' in str(key): return
        
        if key in self.keys_down: return
        self.keys_down.add(key)

        
        for envelope in self.envelopes:
            envelope.toggle(on=True)

        if str(key)[1] in self.MIDICONTROLMAP:
            self.MIDICONTROLMAP[str(key)[1]](self)

        return self.note_down(self.map_key_to_midi(key))#self.send(1, self.map_key_to_midi(key))

    def keyup(self, key):
        if '.' in str(key): return

        self.keys_down.remove(key)
        # self.send(0, self.map_key_to_midi(key))
        self.note_up(self.map_key_to_midi(key))
        
        for envelope in self.envelopes:
            envelope.toggle(on=False)

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