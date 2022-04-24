from simplecoremidi import send_midi

MIDINoteMsgTypes = {"NOTE_OFF": '000', "NOTE_ON": "001"}

class MIDINote:

    def __init__(self, polyphonic=False):
        self.polyphonic=False

    def message(self):
        return []

    def __to_bitstring__(self, item, length):

        bitstring = format(item, '0' + str(length) + 'b')

        if len(bitstring) != length: raise IndexError

        return bitstring

    def generate_status_byte(self, msgid=MIDINoteMsgTypes['NOTE_ON'], channel=0):

        channel = self.__to_bitstring__(channel, 4)

        if len(msgid) != 3: raise IndexError

        return int('1' + msgid + channel, 2).to_bytes(1, byteorder='big')

    def generate_data_bytes(self, b1, b2):

        b1, b2 = (  self.__to_bitstring__(b1, 7), 
                    self.__to_bitstring__(b2, 7) )

        return (int('0' + b1, 2).to_bytes(1, byteorder='big'),
                int('0' + b2, 2).to_bytes(1, byteorder='big'))

    def play_note(self, note, velocity, channel=0):
        return tuple(int.from_bytes(i, 'big') for i in (self.generate_status_byte(MIDINoteMsgTypes['NOTE_ON'], 0),
                *self.generate_data_bytes(note, velocity)))

m = MIDINote()

import time
import random

while True:

    time.sleep(0.1)

    rand_note = random.randint(48, 96-12)

    print(rand_note)

    for i in range(0, 12):
        send_midi(m.play_note(rand_note+i, random.randint(0, 127)))
        time.sleep(0.1)

    for i in range(0, 12):
        send_midi(m.play_note(rand_note+i, 0))
        time.sleep(0.1)