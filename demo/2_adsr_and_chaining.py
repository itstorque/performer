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