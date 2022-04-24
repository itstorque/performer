from performer import *
from performer.controllers.gui_handler import GUIHandler

guihandler = GUIHandler()

audio = AudioOut(fs=44100, 
                    buffer_bit_size=11, 
                    channels=1, 
                    volume=0.1, 
                    controller=guihandler, 
                    output_device=1,
                    latency='low')

gen = Generator(gui_handler=guihandler)

# gen2 = Generator(gui_handler=guihandler)

gen.viz('1')
print("1 PASS")
# gen2.viz('2')
# print("2 PASS")

# gen3 = Generator(gui_handler=guihandler)

# gen3.viz('3')

print("3 PASS")

LFO(audio, f=0, envelope=None, volume=0)

audio.stream()

# import PySimpleGUI as sg  
# import time  
  
# # ----------------  Create Form  ----------------  
# sg.ChangeLookAndFeel('Black')  
# sg.SetOptions(element_padding=(0, 0))  
  
# layout = [[sg.Text('')],  
#          [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='text')],  
#          [sg.ReadButton('Pause', key='button', button_color=('white', '#001480')),  
#           sg.ReadButton('Reset', button_color=('white', '#007339'), key='Reset'),  
#           sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]]  
  
# window = sg.Window('Running Timer', no_titlebar=True, auto_size_buttons=False, keep_on_top=True, grab_anywhere=True).Layout(layout)  
  
# # ----------------  main loop  ----------------  
# current_time = 0  
# paused = False  
# start_time = int(round(time.time() * 100))  
# while (True):  
#     # --------- Read and update window --------  
#     event, values = window.Read(timeout=1)  
#     print(event)
#     if event == sg.WIN_CLOSED or event == 'Exit': 
#         window.close()
#         window = None
#     current_time = int(round(time.time() * 100)) - start_time  
#     # --------- Display timer in window --------  
#     window.FindElement('text').Update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,  
#                                                                   (current_time // 100) % 60,  
#                                                                   current_time % 100))