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