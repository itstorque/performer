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