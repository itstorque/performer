import cv2
from performer import *

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