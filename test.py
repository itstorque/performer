import asyncio
from signal import signal
from performer import *

from threading import Thread

from performer.controllers.controller import Controller

controller = Controller()

audio = AudioOut(fs=44100, buffer_bit_size=10, channels=1, volume=0.5, controller=controller)

F = [1000]

F = Signal()

controller.attach_value(F)

lfo1 = LFO(audio, f=F, envelope=None) + LFO(audio, f=F, envelope=None)

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