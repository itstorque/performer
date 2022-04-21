import asyncio
from performer import *

from threading import Thread

audio = AudioOut(fs=44100, buffer_bit_size=10, channels=1, volume=0.1)

lfo1 = LFO(audio, f=1000, envelope=None)

# asyncio.run( audio.stream() )

# asyncio.ensure_future( audio.stream() )
# loop.run_forever()

print("RUNNING")

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


asyncio.run(  audio.testing() )