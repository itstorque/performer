# TODO: remove asyncio and pyaudio
import numpy as np
import asyncio
import threading

import pyaudio
import sounddevice as sd

class AudioOut:

    def __init__(self, fs, buffer_bit_size, channels, width=2, volume=0.1) -> None:
        # TODO: look at device param
        # TODO: buffer_bit_size, width, volume

        self.fs = fs
        self.volume = volume
        self.buffer_size = 2**buffer_bit_size
        
        self.start_idx = 0
        
        self.event = threading.Event()

        self.voices = set()
        
        self.audio_stream = sd.OutputStream(device=0, channels=channels, callback=self._stream, samplerate=fs, blocksize=self.buffer_size)

    def sample_count(self):
        return self.fs * self.buffer_size

    def attach_voice(self, voice):
        # voices are Generator objects or TODO: other forms of inputs such as mic
        self.voices.add(voice)

    def _stream(self, outdata, frames, time, status):
        # TODO: status and time

        t = (self.start_idx + np.arange(frames)) / self.fs
        t = t.reshape(-1, 1)

        K = [voice.next( self.buffer_size ) for voice in self.voices]

        outdata[:, 0] = self.volume * sum( K )#np.sin(2 * np.pi * 500 * t)

        self.start_idx += frames

    async def stream(self):
        
        with self.audio_stream:
            await self.event.wait()

class AudioOut_Asyncio:
    # TODO: add channels and stereo support
    # TODO: audio manager that AudioOut is a subclass of for managing
    #       input and output.

    def __init__(self, fs, buffer_bit_size, channels, width=2, volume=0.1) -> None:

        self.fs = fs
        self.buffer_size = 2**buffer_bit_size
        self.channels = channels
        self.width = width
        self.volume = volume
        
        self.pyaudio = pyaudio.PyAudio()

        self.audio_stream = self.pyaudio.open(  format=self.pyaudio.get_format_from_width(width),
                                                channels=channels,
                                                rate=fs,
                                                input=False,
                                                output=True,
                                                frames_per_buffer=self.buffer_size)

        self.voices = set()

        self.process_loop = loop = asyncio.get_event_loop()

        self.streaming = False

    def sample_count(self):
        return self.fs * self.buffer_size

    def attach_voice(self, voice):
        # voices are Generator objects or TODO: other forms of inputs such as mic
        self.voices.add(voice)

    def stream(self):

        self.streaming = True

        asyncio.ensure_future(self._get_stream())
        asyncio.ensure_future(self._stream())

        self.process_loop.run_forever()

    async def _get_stream(self):

        self.samples = np.zeros(self.buffer_size)

        while self.streaming:

            # print("_get_stream")

            await asyncio.sleep(0.00001)

            samples = np.zeros(self.sample_count())

            for voice in self.voices:
                samples += voice.next( self.sample_count() )

            self.samples = self.volume * samples


    async def _stream(self):

        while self.streaming:

            # print("_stream")

            # await asyncio.sleep(0.00001)

            self.audio_stream.write(self.samples, self.buffer_size)

            print(self.samples)
            

    def pause_stream(self):

        self.streaming = False

    def destroy(self):

        self.process_loop.close()

        self.pause_stream()

        self.audio_stream.stop_stream()
        self.audio_stream.close()

        self.pyaudio.terminate()


class AudioOut_SingleStream:
    # TODO: add channels and stereo support
    # TODO: audio manager that AudioOut is a subclass of for managing
    #       input and output.

    def __init__(self, fs, buffer_bit_size, channels, width=2, volume=0.1) -> None:

        self.fs = fs
        self.buffer_size = 2**buffer_bit_size
        self.channels = channels
        self.width = width
        self.volume = volume
        
        self.pyaudio = pyaudio.PyAudio()

        self.audio_stream = self.pyaudio.open(  format=self.pyaudio.get_format_from_width(width),
                                                channels=channels,
                                                rate=fs,
                                                input=False,
                                                output=True,
                                                frames_per_buffer=self.buffer_size)

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