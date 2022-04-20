import pyaudio
import numpy as np

class AudioOut:
    # TODO: add channels and stereo support
    # TODO: audio manager that AudioOut is a subclass of for managing
    #       input and output.

    def __init__(self, fs, buffer_size, channels, width=2, volume=0.1) -> None:

        self.fs = fs
        self.buffer_size = buffer_size
        self.channels = channels
        self.width = width
        self.volume = volume
        
        self.pyaudio = pyaudio.PyAudio()

        self.audio_stream = self.pyaudio.open(  format=self.pyaudio.get_format_from_width(width),
                                                channels=channels,
                                                rate=fs,
                                                input=False,
                                                output=True,
                                                frames_per_buffer=buffer_size)

        self.voices = set()

        self.streaming = False

    def sample_count(self):
        return self.fs * self.buffer_size

    def attach_voice(self, voice):
        # voices are Generator objects or TODO: other forms of inputs such as mic
        self.voices.add(voice)

    def stream(self):

        self.streaming = True

        while self.streaming:

            samples = np.zeros(self.sample_count())

            for voice in self.voices:
                samples += voice.next( self.sample_count() )

            print(samples)

            self.audio_stream.write(self.volume * samples, self.buffer_size)

    def pause_stream(self):

        self.streaming = False

    def destroy(self):

        self.pause_stream()

        self.audio_stream.stop_stream()
        self.audio_stream.close()

        self.pyaudio.terminate()