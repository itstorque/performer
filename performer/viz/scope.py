from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

import numpy as np
import queue

class Scope:

    def __init__(self):

        length = int(args.window * args.samplerate / (1000 * args.downsample))
        plotdata = np.zeros((length, len(args.channels)))

        self.fig, ax = plt.subplots()
        lines = ax.plot(plotdata)
        if len(args.channels) > 1:
            ax.legend(['channel {}'.format(c) for c in args.channels],
                    loc='lower left', ncol=len(args.channels))
        ax.axis((0, len(plotdata), -1, 1))
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

    def update_plot(frame):
        """
        This is called by matplotlib for each plot update.

        Typically, audio callbacks happen more frequently than plot updates,
        therefore the queue tends to contain multiple blocks of audio data.
        """
        while True:
            try:
                data = q.get_nowait()
            except queue.Empty:
                break
            shift = len(data)
            self.plotdata = np.roll(self.plotdata, -shift, axis=0)
            self.plotdata[-shift:, :] = data
        for column, line in enumerate(lines):
            line.set_ydata(self.plotdata[:, column])
        return lines

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])

scope = Scope()
scope.start(sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback))

# TODO: AAAAA, need to place things on queue for audio so that we can extract that for scope?