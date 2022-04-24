import asyncio
from socket import timeout
from threading import Thread

from .controller import Controller

class GUIHandler(Controller):

    def __init__(self):
        import PySimpleGUI as sg
        # sg should be cached in global memory now

        self.set_theme("BlueMono")
        self.windows = {}

        self.window_loop = None
        self.window_thread = None
        self.window_loop_running = False

    def set_theme(self, theme):
        import PySimpleGUI as sg
        
        sg.theme(theme)

    def init_window_loop(self):
        if self.window_loop_running == True: return
        # self.window_loop = asyncio.new_event_loop()
        # self.window_thread = Thread(target=self.gui_asyncloop, args=(self.window_loop,))
        # self.window_loop_running = True

        # self.window_thread.start()

        self.gui_asyncloop(None)

    def new_window(self, title, layout):
        import PySimpleGUI as sg

        self.windows[title] = sg.Window(title, layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True, grab_anywhere=True)
        self.windows[title].read(timeout=10)

        # TODO: put this in a better place
        self.window_loop_running = True
        # self.init_window_loop()

    def update(self):
        import time
        import PySimpleGUI as sg
        # print("UPDATING", [window for name, window in self.windows.items()])
        if self.window_loop_running == False: return

        for name, window in self.windows.items():
            if window != None:
                event, values = window.Read(timeout=10)
                if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                    self.windows[name] = None
                    window.close()
                    break
                if event != sg.TIMEOUT_EVENT:
                    print('You entered ', values[0])

    def gui_asyncloop(self, loop):
        # Set loop as the active event loop for this thread
        # asyncio.set_event_loop(loop)
        # We will get our tasks from the main thread so just run an empty loop    
        # loop.run_forever()
        import PySimpleGUI as sg

        while True:
            for name, window in self.windows.items():
                print(name)
                if window != None:
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                        self.windows[name] = None
                        window.close()
                        break
                    print('You entered ', values[0])