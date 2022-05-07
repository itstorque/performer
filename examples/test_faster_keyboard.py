import threading
from pynput import keyboard

global windowOpened
windowOpened = False

def on_press(key):
    print('pressed', key)

def on_release(key):
    print('released', key)
    if str(key) == 'Key.esc':
        print('Exiting')
        return False

def sleeper():
    global escapePressed
    escapePressed = False
    with keyboard.Listener(
    on_press = on_press,
    on_release = on_release, suppress=True) as listener:
        escapePressed = True
        listener.join()

t1 = threading.Thread(target = sleeper, name = 'esc_detection_thread')
t1.start()

for i in range(10):
    if escapePressed == True:
        sys.exit()
    else:
        #open calculator and close it by clicking the red x
        pass