from performer import *

audio = AudioOut(volume=0.4, output_device=1)

osc1 = OSC(f=200, volume=1, type=Sine)

audio.attach_voice(osc1)
audio.stream()

###

from performer import *

audio = AudioOut(volume=0.4, output_device=1)

F = 200

osc1 = OSC(f=F, volume=1, type=Sine)

osc2 = OSC(f=F, volume=1, type=Sine, fmul=0.66)

audio.attach_voice(osc1 + osc2)
audio.stream()

###

from performer import *

audio = AudioOut(volume=0.4, output_device=1, scope=Scope())

F = 200

osc1 = OSC(f=F, volume=1, type=Sine)

osc2 = OSC(f=F, volume=1, type=Sine, fmul=0.66) + OSC(f=F, volume=1, type=Sine, fmul=0.33)

audio.attach_voice(osc1 + osc2)
audio.stream()