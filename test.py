import asyncio
from performer import *

audio = AudioOut(fs=44100, buffer_bit_size=10, channels=1, volume=0.1)

lfo1 = LFO(audio, f=1000, envelope=None)

asyncio.run( audio.stream() )

print("RUNNING")

# audio.destroy()