# TODO: remove asyncio and pyaudio
import numpy as np
import asyncio
import threading

# import pyaudio
import sounddevice as sd

from ..controllers.controller import Controller

# TODO: implement stereo output!

class AudioOut:

    def __init__(self, fs, buffer_bit_size, channels=1, controller=None, width=2, volume=0.1, output_device=0, latency=None) -> None:
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

        self.halted = False

    def sample_count(self):
        return self.fs * self.buffer_size

    def attach_voice(self, voice):
        # voices are Generator objects or TODO: other forms of inputs such as mic
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

        K = [voice.next( self.buffer_size ) for voice in self.voices]

        outdata[:, 0] = self.volume * sum( K )#np.sin(2 * np.pi * 500 * t)

        self.start_idx += frames

    def stream(self):
        
        with sd.OutputStream(device=self.output_device, channels=self.channels, callback=self._stream, samplerate=self.fs, blocksize=self.buffer_size, finished_callback=self.event.set, latency=self.latency) as audio_stream:
            self.audio_stream = audio_stream

            while True: 
                if self.halted: break

                self.controller.update()

class AudioOutManagerTest:

    def __init__(self, fs, buffer_bit_size, channels, width=2, volume=0.1) -> None:
        # TODO: look at device param
        # TODO: buffer_bit_size, width, volume

        self.fs = fs
        self.volume = volume
        self.buffer_size = 2**buffer_bit_size
        
        self.start_idx = 0
        
        self.event = threading.Event()

        self.voices = set()

        self.halt = False
        
        self.audio_stream = sd.OutputStream(device=0, channels=channels, callback=self._stream, samplerate=fs, blocksize=self.buffer_size, finished_callback=self.event.set)

    def sample_count(self):
        return self.fs * self.buffer_size

    def attach_voice(self, voice):
        # voices are Generator objects or TODO: other forms of inputs such as mic
        self.voices.add(voice)

    def stop_audio_stream(self):
        self.audio_stream.abort()
        # self.audio_stream.stop()
        self.audio_stream.close()

        self.event.set()

    def _stream(self, outdata, frames, time, status):
        # TODO: status and time

        if self.halt: 
            self.loop.call_soon_threadsafe(self.event.set)
            self.stop_audio_stream()

        t = (self.start_idx + np.arange(frames)) / self.fs
        t = t.reshape(-1, 1)

        K = [voice.next( self.buffer_size ) for voice in self.voices]

        outdata[:, 0] = self.volume * sum( K )#np.sin(2 * np.pi * 500 * t)

        self.start_idx += frames

    async def stream(self, queue):

        print('stream', queue)
        
        with self.audio_stream:
            await self.event.wait()

        print("stream done")

    def test_manager(self, loop, queue):

        import time 
        time.sleep(2)

        print('manager', loop)

        # loop.stop()
        # loop.close()
        self.halt = True

        # loop.call_soon_threadsafe(queue.put_nowait, 'manager halted')
        loop.call_soon_threadsafe(self.stop_audio_stream)

        return

    async def testing(self):

        print('testing')
        queue = asyncio.Queue()
        loop = asyncio.get_running_loop()

        self.loop = loop

        blocking_fut = loop.run_in_executor(None, self.test_manager, loop, queue)
        nonblocking_task = loop.create_task(self.stream(queue))

        while not self.halt:
            # Get messages from both blocking and non-blocking in parallel
            message = await queue.get()
            # You could send any messages, and do anything you want with them
            print(message)

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