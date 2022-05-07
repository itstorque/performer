import asyncio
from signal import signal
from performer import *

from threading import Thread

from performer.controllers.controller import Controller

from time import time
import cv2

import psutil

from random import randint

cap = cv2.VideoCapture(0)

def control(controller):

    cap = controller.videocap

    ret, photo = cap.read() 

    cv2.waitKey(10); cv2.imshow('frame', photo)

    controller.set_param('freq1', 0*(int(photo[0,0,0]) + int(photo[-1,-1,0])) * 4)

    controller.second_note = (controller.second_note + 10) % 900 + 100

    print(psutil.cpu_percent(interval=1))
    
    controller.set_param('freq2', psutil.cpu_percent(interval=1)*20)

    return

controller = Controller(control, videocap=cap, second_note=0)

audio = AudioOut(fs=44100, 
                    buffer_bit_size=8, 
                    channels=1, 
                    volume=0.4, 
                    controller=controller, 
                    output_device=1,
                    latency=0.01,)
                    # scope=Scope(downsample=20)) # sounddevice.query_devices

F1 = Param(300, 'freq1')
F2 = Param(250, 'freq2')

controller.attach_freq(F1)

controller.attach_param(F1)
controller.attach_param(F2)


lfo1 = LFO(f=F1, volume=1, type=Sin, fmul=1)
lfo2 = LFO(f=F2, volume=1, type=Sin, fmul=1)

out = lfo1 + lfo2
out.audio = audio
audio.attach_voice(out)

audio.stream()