import asyncio
from signal import signal
from performer import *

from threading import Thread

from performer.controllers.controller import Controller

controller = MIDIKeyboard(midiout=False)

# print(sounddevice.query_devices())

audio = AudioOut(fs=44100, 
                    buffer_bit_size=6, 
                    channels=1, 
                    volume=0.1, 
                    controller=controller, 
                    output_device=1,
                    latency=0.01,)
                    # scope=Scope(downsample=20)) # sounddevice.query_devices

F = Param(100, 'freq')#300.

A = Param(1, 'amp')#1.

# F = Signal()

controller.attach_freq(F)
# controller.attach_value(A)

controller.attach_toggle(A)

# lfo_mod = LFO(f=1)
lfo_mod = LFO(f=100)

# lfo_mod.audio = audio
# audio.add(lfo_mod)

print("LFO1")

lfo1 = LFO(f=lfo_mod+100, volume=0.5, type=Sine, fmul=1)
lfo1.audio = audio
# lfo2 = LFO(f=F, fmul=0.66, volume=A) + LFO(None, f=F, fmul=0.33, envelope=None, volume=A)

# lfo1.audio = None
# lfo2.audio = None

# out = lfo1

out = lfo1#Reverb(lfo1, audio=audio, delay=0.01, wet_to_dry_ratio=0.5)
# controller.attach_envelope(out)

audio.attach_voice(out)

out.audio = audio

# asyncio.run( audio.stream() )

# asyncio.ensure_future( audio.stream() )
# loop.run_forever()

print("RUNNING")

audio.stream()

# audio.destroy()

# def asyncloop(loop):
#     # Set loop as the active event loop for this thread
#     asyncio.set_event_loop(loop)
#     # We will get our tasks from the main thread so just run an empty loop    
#     loop.run_forever()

# create a new loop
# loop = asyncio.new_event_loop()
# # Create the new thread, giving loop as argument
# t = Thread(target=asyncloop, args=(loop,))
# # Start the thread
# t.start()


# asyncio.run(  audio.testing() )


# C4 is 60
# A is C, thru L is D
# wetyuo sharps