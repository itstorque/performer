import pyaudio
import numpy as np

import matplotlib.pyplot as plt

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 2.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float
f2 = 1/10.0

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*
            f*np.sin(2*np.pi*
                np.arange(fs*duration) * f2/fs))).astype(np.float32)

# plt.plot(samples)
# plt.show() 

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively) 
stream.write(volume*samples)
stream.write(volume*samples)
stream.write(volume*samples)

stream.stop_stream()
stream.close()

p.terminate()


# """
# PyAudio Example: Make a wire between input and output (i.e., record a
# few samples and play them back immediately).
# """

# import pyaudio

# CHUNK = 1024
# WIDTH = 2
# CHANNELS = 1
# RATE = 44100
# RECORD_SECONDS = 5

# p = pyaudio.PyAudio()

# stream = p.open(format=p.get_format_from_width(WIDTH),
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 output=True,
#                 frames_per_buffer=CHUNK)

# print("* recording")

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     stream.write(data, CHUNK)

# print("* done")

# stream.stop_stream()
# stream.close()

# p.terminate()