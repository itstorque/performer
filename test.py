from audio.audio_out import *
from generators.lfo import *

audio = AudioOut(fs=44100, buffer_size=1024, channels=1, volume=1)

lfo1 = LFO(audio, f=20, envelope=None)

audio.stream()

audio.destroy()