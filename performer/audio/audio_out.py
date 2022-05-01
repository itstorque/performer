# TODO: remove asyncio and pyaudio
import numpy as np
import asyncio
import threading

# import pyaudio
import sounddevice as sd

from ..controllers.controller import Controller

# TODO: implement stereo output!

class AudioOut:

    def __init__(self, fs=44100, buffer_bit_size=8, 
                 channels=1, 
                 controller=None, 
                 width=2, 
                 volume=1, 
                 output_device=0, 
                 latency=0.01, 
                 scope=None):
        # TODO: look at device param
        # TODO: buffer_bit_size, width, volume

        print(sd.query_devices())

        self.fs = fs
        self.volume = volume
        self.buffer_size = 2**buffer_bit_size
        self.channels = channels
        self.output_device = output_device
        self.latency = latency

        if controller==None: controller = Controller()

        self.controller = controller
        self.controller.init()
        
        self.start_idx = 0
        
        self.event = threading.Event()

        self.voices = set()
        self.osc_nonvoice = set()

        self.halted = False

        self.scope = scope

    def sample_count(self):
        return self.fs * self.buffer_size

    def add(self, osc):
        osc.audio = self
        self.osc_nonvoice.add(osc)

    def attach_voice(self, voice):
        # voices are Generator objects or TODO: other forms of inputs such as mic
        voice.audio = self
        self.voices.add(voice)

    def halt(self): self.stop()

    def stop(self):
        self.halted = True
        # self.audio_stream.abort()
        # # self.audio_stream.stop()
        # self.audio_stream.close()

        # self.event.set()

    def _stream(self, outdata, frames, time, status):
        # TODO: status and time

        if self.halted: 
            self.loop.call_soon_threadsafe(self.event.set)
            self.stop_audio_stream()

        t = (self.start_idx + np.arange(frames)) / self.fs
        t = t.reshape(-1, 1)

        for osc in self.osc_nonvoice: osc.next( self.buffer_size )

        K = [voice.next( self.buffer_size ) for voice in self.voices]

        outdata[:, 0] = self.volume.__float__() * sum( K )#np.sin(2 * np.pi * 500 * t)

        self.start_idx += frames

        if self.scope: self.scope.update(outdata)

    def stream(self, loop=None):
        
        with sd.OutputStream(device=self.output_device, channels=self.channels, callback=self._stream, samplerate=self.fs, blocksize=self.buffer_size, finished_callback=self.event.set, latency=self.latency) as audio_stream:
            self.audio_stream = audio_stream

            if self.scope: self.scope.start(audio_stream)

            while True: 
                if self.halted: break

                if loop: loop(self)

                self.controller.update()