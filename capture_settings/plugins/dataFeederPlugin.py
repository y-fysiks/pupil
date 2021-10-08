from plugin import Plugin
from methods import denormalize
import pyautogui as pag

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
            ppt = self.pupil_display_list[-1]
            print(tuple(ppt))

        self.pupil_display_list[0:-3] = []

    def get_init_dict(self):
        return {}