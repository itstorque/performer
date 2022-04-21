import asyncio
from signal import signal
from performer import *

from threading import Thread

from performer.controllers.controller import Controller

controller = MIDIKeyboard()

audio = AudioOut(fs=44100, 
                    buffer_bit_size=11, 
                    channels=1, 
                    volume=0.1, 
                    controller=controller, 
                    output_device=1,
                    latency='low')

F = np.array([1000.])

# F = Signal()

controller.attach_value(F)

lfo1 = LFO(None, f=F, envelope=None)
lfo2 = LFO(None, f=F, fmul=0.4, envelope=None)# + LFO(audio, f=F, fmul=0.33, envelope=None)

# lfo1.audio = None
# lfo2.audio = None

lfo = lfo1 + lfo2
audio.attach_voice(lfo)

lfo.audio = audio

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