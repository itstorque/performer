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
    faceCascade = controller.faceCascade

    ret, frames = cap.read()
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces) > 0:

        (x, y, w, h) = faces[0]

        controller.set_param('freq', x)
        controller.set_param('amp', y/1000)

    else:
        controller.set_param('amp', 0)

    return

controller = Controller(control, videocap=cap, faceCascade=cv2.CascadeClassifier(os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"))

audio = AudioOut(fs=44100, 
                    buffer_bit_size=8, 
                    channels=1, 
                    volume=0.4, 
                    controller=controller, 
                    output_device=1,
                    latency=0.01,)
                    # scope=Scope(downsample=20)) # sounddevice.query_devices

F = Param(300, 'freq')
A = Param(1, 'amp')

controller.attach_param(F)
controller.attach_param(A)


lfo1 = LFO(f=F, volume=A, type=Sin, fmul=1)
lfo2 = LFO(f=F, volume=A, type=Sin, fmul=0.66)
lfo3 = LFO(f=F, volume=A, type=Sin, fmul=0.33)

out = lfo1 + lfo2 + lfo3
out.audio = audio
audio.attach_voice(out)

audio.stream()




# faceCascade = cv2.CascadeClassifier(os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml")

# video_capture = cv2.VideoCapture(0)
# while True:
#     # Capture frame-by-frame
#     ret, frames = video_capture.read()
#     gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
#     faces = faceCascade.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=5,
#         minSize=(30, 30),
#         flags=cv2.CASCADE_SCALE_IMAGE
#     )
#     # Draw a rectangle around the faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     # Display the resulting frame
#     cv2.imshow('Video', frames)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break