from plugin import System_Plugin_Base
from pyglui.cygl.utils import RGBA
from gl_utils import draw_circle_filled_func_builder
from methods import denormalize
import sched, time, threading
import pyautogui as pag

class dataFeederPlugin(System_Plugin_Base):
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
    order = 0.6
    alive = True

    # menu icon font, possible values `roboto`, `opensans`, `pupil_icons`,
    # or custom loaded font name
    icon_font = "pupil_icons"
    icon_chr = "?"  # character shown in menu icon
            
    def __init__(self, g_pool):
        super().__init__(g_pool)
        
        self.pupil_display_list = []
        if getattr(g_pool, "debug", False):
            self.__monkeypatch_gl_display_error_checking()

    def recent_events(self, events):
        for pt in events.get("gaze", []):
            recent_frame_size = self.g_pool.capture.frame_size
            point = denormalize(pt["norm_pos"], recent_frame_size, flip_y=True)
            self.pupil_display_list.append((point, pt["confidence"] * 0.8))
            print("point logged: " + str(self.pupil_display_list[len(self.pupil_display_list)-1]))

        self.pupil_display_list[:-3] = []

    def gl_display(self):
        for pt, a in self.pupil_display_list:
            # This could be faster if there would be a method to also add multiple colors per point
            self._draw_circle_filled(
                tuple(pt),
                size=35 / 2,
                color=RGBA(1.0, 0.2, 0.4, a),
            )

    def get_init_dict(self):
        return {}