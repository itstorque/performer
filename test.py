import asyncio
from signal import signal
from performer import *

from threading import Thread

from performer.controllers.controller import Controller

controller = MIDIKeyboard(midiout=True)

# print(sounddevice.query_devices())

audio = AudioOut(fs=44100, 
                    buffer_bit_size=12, 
                    channels=1, 
                    volume=0.4, 
                    controller=controller, 
                    output_device=0,
                    latency=0.01,)
                    # scope=Scope(downsample=5)) # sounddevice.query_devices

F = np.array([300.])

A = np.array([1.])

# F = Signal()

controller.attach_value('recent_freq', F)
# controller.attach_value(A)

lfo1 = LFO(None, f=F, envelope=None, volume=A, type=Sine, fmul=1)
lfo2 = LFO(None, f=F, fmul=0.66, envelope=None, volume=A) + LFO(None, f=F, fmul=0.33, envelope=None, volume=A)

# lfo1.audio = None
# lfo2.audio = None

# out = lfo1

out = ADSR(lfo1 + lfo2, None)
controller.attach_envelope(out)

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