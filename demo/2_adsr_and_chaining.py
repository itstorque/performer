# from performer import *

# controller = MIDIKeyboard()

# audio = AudioOut(volume=0.4, output_device=1, controller=controller)

# F = Param(200)

# osc1 = OSC(f=F, volume=1, type=Sine)

# osc2 = OSC(f=F, volume=1, type=Sine, fmul=0.66) + OSC(f=F, volume=1, type=Sine, fmul=0.33)

# controller.attach_freq(F)

# audio.attach_voice(osc1 + osc2)
# audio.stream()

# from performer import *

# controller = MIDIKeyboard()

# audio = AudioOut(volume=0.4, output_device=1, controller=controller)

# F = Param(200)

# osc1 = OSC(f=F, volume=1, type=Sine)

# osc2 = OSC(f=F, volume=1, type=Sine, fmul=0.66) + OSC(f=F, volume=1, type=Sine, fmul=0.33)

# adsr = ADSR(osc1 + osc2, A=0.1, D=0.2, S=0.9, R=1.0)

# controller.attach_freq(F)
# controller.attach_envelope(adsr)

# audio.attach_voice(adsr)
# audio.stream()

# from performer import *

# controller = MIDIKeyboard()

# audio = AudioOut(volume=0.4, output_device=1, controller=controller, scope=AudioOutFile('test_2'))

# F = Param(200)

# osc1 = 0.5*OSC(f=F, volume=1, type=Sine)

# osc2 = OSC(f=F*0.66, volume=1, type=Sine) + OSC(f=F*0.33, volume=1, type=Sine)

# adsr = ADSR(osc1 + osc2, A=0.1, D=0.2, S=0.9, R=1.0)

# controller.attach_freq(F)
# controller.attach_envelope(adsr)

# audio.attach_voice(adsr)
# audio.stream()

from performer import *

controller = MIDIKeyboard()

audio = AudioOut(volume=0.4, output_device=1, controller=controller, scope=AudioOutFile('test_2'))

F = Param(200)
lfo = LFO(f=10)

osc1 = 0.5*OSC(f=F, volume=lfo, type=Sine)

osc2 = OSC(f=F*0.66, volume=lfo, type=Sine) + OSC(f=F*0.33, volume=lfo, type=Sine)

adsr = ADSR(osc1 + osc2, A=0.1, D=0.2, S=0.9, R=1.0)

controller.attach_freq(F)
controller.attach_envelope(adsr)

audio.attach_voice(adsr)
audio.stream()