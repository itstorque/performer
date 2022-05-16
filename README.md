# Peformer

### Simple Additive LFO

```python
from performer import *

audio = AudioOut(output_device=1)

out = ADSR(OSC(f=261.63) + OSC(f=329.63)) + OSC(f=392.00))

audio.attach_voice(out)
audio.stream()
```

### MIDI Keyboard Example

```python
from performer import *

controller = MIDIKeyboard(midiout=True)

audio = AudioOut(volume=0.1, output_device=4, controller=controller)

F = Param(200)

osc1 = OSC(f=F, volume=1, type=Sine)
osc2 = OSC(f=F, volume=1, type=Sine, fmul=0.66)
osc3 = OSC(f=F, volume=1, type=Sine, fmul=0.33)

controller.attach_freq(F)

audio.attach_voice(osc1 + osc2 + osc3)
audio.stream()
```

### Face Detection Theremin

```python
from performer import *
import cv2

faceCascade = cv2.CascadeClassifier(os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)

def control(controller):
    # Capture frame-by-frame
    ret, frames = video_capture.read()
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Display the resulting frame
    cv2.imshow('Video', frames)

    if len(faces) > 0:

        (x, y, w, h) = faces[0]
        
        controller.set_param('freq', x)
        controller.set_param('amp', y/500)

    else:

        controller.set_param('amp', 0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        pass

controller = Controller(control)

audio = AudioOut(controller=controller, output_device=2)

F = Param(300, 'freq')
A = Param(1, 'amp')

controller.attach_param(F)
controller.attach_param(A)

lfo1 = LFO(f=F, volume=A, type=Sin, fmul=1)
lfo2 = LFO(f=F, volume=A, type=Sin, fmul=0.66)
lfo3 = LFO(f=F, volume=A, type=Sin, fmul=0.33)

audio.attach_voice(sum([lfo1, lfo2, lfo3]))
audio.stream()
```


### requirements

- numpy
- sounddevice
- matplotlib
- soundfile

You also need to install `libsndfile` from a package manager like homebrew
using a command similar to:

```shell
brew install python-soundfile
```

Note that if you face an error similar to this, then your soundfile install is weird.
This workaround is M1 Macs.
``` python
Traceback (most recent call last):
  File "/Users/torque/Library/Python/3.8/lib/python/site-packages/soundfile.py", line 142, in <module>
    raise OSError('sndfile library not found')
OSError: sndfile library not found

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/torque/programs/performer/performer/__init__.py", line 13, in <module>
    from .audio.audio_out_file import *
  File "/Users/torque/programs/performer/performer/audio/audio_out_file.py", line 2, in <module>
    import soundfile as sf
  File "/Users/torque/Library/Python/3.8/lib/python/site-packages/soundfile.py", line 162, in <module>
    _snd = _ffi.dlopen(_os.path.join(
OSError: cannot load library '/Users/torque/Library/Python/3.8/lib/python/site-packages/_soundfile_data/libsndfile.dylib': dlopen(/Users/torque/Library/Python/3.8/lib/python/site-packages/_soundfile_data/libsndfile.dylib, 0x0002): tried: '/Users/torque/Library/Python/3.8/lib/python/site-packages/_soundfile_data/libsndfile.dylib' (no such file), '/usr/local/lib/libsndfile.dylib' (no such file), '/usr/lib/libsndfile.dylib' (no such file)
```

`libsndfile` won't work out of the box on M1 macs. To fix that, you need
to add the homebrew path to your PATH. The below command has some security
consequences, but is generally okay and should fix the problem
```shell
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
```

The alternative would be to manually install the `libsndfile` library
in the default `/usr/local/lib` homebrew used on intel macs.