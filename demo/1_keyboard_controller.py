# from performer import *

# audio = AudioOut(volume=0.4, output_device=1, scope=Scope())

# F = 200

# osc1 = OSC(f=F, volume=1, type=Sine)

# osc2 = OSC(f=F, volume=1, type=Sine, fmul=0.66) + OSC(f=F, volume=1, type=Sine, fmul=0.33)

# audio.attach_voice(osc1 + osc2)
# audio.stream()

# ###

# from performer import *

# controller = MIDIKeyboard()

# audio = AudioOut(volume=0.4, output_device=1, controller=controller)

# F = 200

# osc1 = OSC(f=F, volume=1, type=Sine)

# osc2 = OSC(f=F, volume=1, type=Sine, fmul=0.66) + OSC(f=F, volume=1, type=Sine, fmul=0.33)

# audio.attach_voice(osc1 + osc2)
# audio.stream()

###

from performer import *

controller = MIDIKeyboard()

audio = AudioOut(volume=0.4, output_device=1, controller=controller)

F = Param(200)

osc1 = OSC(f=F, volume=1, type=Sine)

osc2 = OSC(f=F, volume=1, type=Sine, fmul=0.66) + OSC(f=F, volume=1, type=Sine, fmul=0.33)

controller.attach_freq(F)

audio.attach_voice(osc1 + osc2)
audio.stream()