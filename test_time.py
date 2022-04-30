import asyncio
from signal import signal
from performer import *

from threading import Thread

from performer.controllers.controller import Controller

from time import time

def control(controller):

    print(time() % 4 <= 2, end="\r")
    
    if time() % 4 <= 2: controller.set_freq(100)
    else: controller.set_freq(400)

    return

controller = Controller(control)

audio = AudioOut(fs=44100, 
                    buffer_bit_size=8, 
                    channels=1, 
                    volume=0.4, 
                    controller=controller, 
                    output_device=1,
                    latency=0.01,)
                    # scope=Scope(downsample=20)) # sounddevice.query_devices

F = Param(300, 'freq')#300.

controller.attach_freq(F)


lfo1 = LFO(f=F, volume=1, type=Sin, fmul=1)

out = lfo1
out.audio = audio
audio.attach_voice(out)

audio.stream()