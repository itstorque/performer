class Generator:

    def __init__(self, audio, controller):

        self.audio = audio
        self.controller = controller

        audio.attach_voice(self)

    def next(self, buffer_size=None):

        if buffer_size==None: buffer_size = self.audio.buffer_size()

        return self._next(buffer_size=buffer_size, fs=self.audio.fs)