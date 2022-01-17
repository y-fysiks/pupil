from plugin import Plugin
from methods import denormalize
import pyautogui as pag
import sys
from tkinter import *
import threading
import pywintypes
import win32api
import win32gui
import win32con
from win32api import GetSystemMetrics


class dataFeederPlugin(Plugin):
    """
    datafeeder is a plugin that will send data to the custom C# User Interface application in order to control the mouse. 
    """
    # if you have a plugin that can exist multiple times make this false in your derived class
    uniqueness = "by_class"
    # uniqueness = 'not_unique'
    # uniqueness = 'by_base_class'

    # between 0 and 1 this indicated where in the plugin excecution order you plugin lives:
    # <.5  are things that add/mofify information that will be used by other plugins and rely on untouched data.
    # You should not edit frame if you are here!
    # == .5 is the default.
    # >.5 are things that depend on other plugins work like display , saving and streaming
    # you can change this in __init__ for your instance or in the class definition
    order = 0.8
    alive = True

    # menu icon font, possible values `roboto`, `opensans`, `pupil_icons`,
    # or custom loaded font name
    icon_font = "pupil_icons"


    def displayFiducials(self):
                
        root = Tk()
        img1 = PhotoImage(file="C:\\Users\\yubo0\\OneDrive\\Documents\\GitHub\pupil\\capture_settings\\plugins\\fiducial_0_scaled.gif")
        img2 = PhotoImage(file="C:\\Users\\yubo0\\OneDrive\\Documents\\GitHub\pupil\\capture_settings\\plugins\\fiducial_1_scaled.gif")
        img3 = PhotoImage(file="C:\\Users\\yubo0\\OneDrive\\Documents\\GitHub\pupil\\capture_settings\\plugins\\fiducial_2_scaled.gif")
        img4 = PhotoImage(file="C:\\Users\\yubo0\\OneDrive\\Documents\\GitHub\pupil\\capture_settings\\plugins\\fiducial_3_scaled.gif")

        screenWidth = GetSystemMetrics(0)
        screenHeight = GetSystemMetrics(1)

        canvas = Canvas(root, width=screenWidth, height=screenHeight)
        canvas.create_image(0, 0, anchor=NW, image=img1)
        canvas.create_image(screenWidth, 0, anchor=NE, image=img2)
        canvas.create_image(screenWidth, screenHeight, anchor=SE, image = img3)
        canvas.create_image(0, screenHeight, anchor=SW, image = img4)

        canvas.pack()

        canvas.master.overrideredirect(True)
        canvas.master.geometry("+250+250")
        canvas.master.lift()
        canvas.master.wm_attributes("-topmost", True)
        canvas.master.wm_attributes("-disabled", True)
        canvas.master.wm_attributes("-transparentcolor", "#f0f0f0")

        hWindow = pywintypes.HANDLE(int(canvas.master.frame(), 16))
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT

        # exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
        win32gui.MoveWindow(hWindow, 0, 0, screenWidth, screenHeight, True)

        canvas.pack()
        mainloop()
            
    def __init__(self, g_pool):
        super().__init__(g_pool)
        
        self.pupil_display_list = []

        self.screenWidth = GetSystemMetrics(0)
        self.screenHeight = GetSystemMetrics(1)
        print(f'screen width: {self.screenWidth}, screen height: {self.screenHeight}')


        self.fiducials = threading.Thread(target=self.displayFiducials)

        self.fiducials.start()

        if getattr(g_pool, "debug", False):
            self.__monkeypatch_gl_display_error_checking()

    def recent_events(self, events):
        for pt in events.get("surfaces", []):
            point = pt["gaze_on_surfaces"]
            for x in point:
                if (x["confidence"] > 0.8):
                    pos = x["norm_pos"]
                    posX = pos[0] * self.screenWidth + 15
                    posY = self.screenHeight - pos[1] * self.screenHeight + 15
                    if (posX > 5 and posX < self.screenWidth - 5 and posY > 5 and posY < self.screenHeight - 5):
                        pag.moveTo(posX, posY)
                    break
            
                
        #self.pupil_display_list[0:-3] = []

    def cleanup(self):
        #end the fiducials thread
        super().cleanup()


    def get_init_dict(self):
        return {}