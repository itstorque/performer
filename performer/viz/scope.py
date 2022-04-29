import sounddevice as sd
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

import numpy as np
import queue

plt.rcParams['keymap.save'].remove('s')

class Scope:

    def __init__(self, downsample=20):

        self.window_size = 200
        self.fs = 44100
        self.downsample = downsample

        length = int(self.window_size * self.fs / (1000 * self.downsample))
        self.plotdata = np.zeros((length, 1))

        self.fig, ax = plt.subplots()
        self.lines = ax.plot(self.plotdata)
        ax.axis((0, len(self.plotdata), -1, 1))
        # ax.axis((0, len(self.plotdata), -50000, 5000000))
        ax.set_yticks([0])
        ax.yaxis.grid(True)
        ax.tick_params(bottom=False, top=False, labelbottom=False,
                    right=False, left=False, labelleft=False)
        self.fig.tight_layout(pad=0)

        self.q = queue.Queue()

    def start(self, stream):
        ani = FuncAnimation(self.fig, self.update_plot, interval=30, blit=True)
        with stream:
            plt.show()

    def update_plot(self, frame):
        """
        This is called by matplotlib for each plot update.

        Typically, audio callbacks happen more frequently than plot updates,
        therefore the queue tends to contain multiple blocks of audio data.
        """
        while True:
            try:
                data = self.q.get_nowait()
            except queue.Empty:
                break
            shift = len(data)
            self.plotdata = np.roll(self.plotdata, -shift, axis=0)
            self.plotdata[-shift:, :] = data
        for column, line in enumerate(self.lines):
            line.set_ydata(self.plotdata[:, column])
        return self.lines

    def update(self, indata, *args, **kwargs):
        """This is called (from a separate thread) for each audio block."""
        # TODO: rn this takes in args and kwargs and discards them...

        self.q.put(indata[::self.downsample, (0, )])

# scope = Scope()
# scope.start(sd.InputStream(
#         device=1, channels=1,
#         samplerate=44100, callback=scope.update))

# TODO: AAAAA, need to place things on queue for audio so that we can extract that for scope?
