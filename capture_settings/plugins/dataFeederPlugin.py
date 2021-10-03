from plugin import Plugin

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
    order = 0.6
    alive = True

    # menu icon font, possible values `roboto`, `opensans`, `pupil_icons`,
    # or custom loaded font name
    icon_font = "roboto"

    def __init__(self, g_pool):
        super().__init__(g_pool)

        if getattr(g_pool, "debug", False):
            self.__monkeypatch_gl_display_error_checking()

    def init_ui(self):
        """
        Called when the context will have a gl window with us. You can do your init for that here.
        """
        pass
    
    def recent_events(self, events):
        """
        Called in Player and Capture.
        Gets called once every frame.
        If you plan to update data inplace, note that this will affect all plugins executed after you.
        Use self.order to deal with this appropriately
        """
        pass

    def gl_display(self):
        """
        Gets called once every frame when its time to draw onto the gl canvas.
        """
        pass

    def on_click(self, pos, button, action):
        """
        Gets called when the user clicks in the window screen and the event has
        not been consumed by the GUI.
        Return True if the event was consumed and should not be propagated
        to any other plugin.
        """
        return False

    def on_pos(self, pos):
        """
        Gets called when the user moves the mouse in the window screen.
        """
        pass

    def on_key(self, key, scancode, action, mods):
        """
        Gets called on key events that were not consumed by the GUI.
        Return True if the event was consumed and should not be propagated
        to any other plugin.
        See http://www.glfw.org/docs/latest/input_guide.html#input_key for
        more information key events.
        """
        return False

    def on_char(self, character):
        """
        Gets called on char events that were not consumed by the GUI.
        Return True if the event was consumed and should not be propagated
        to any other plugin.
        See http://www.glfw.org/docs/latest/input_guide.html#input_char for
        more information char events.
        """
        return False

    def on_drop(self, paths):
        """
        Gets called on dropped paths of files and/or directories on the window.
        Return True if the event was consumed and should not be propagated
        to any other plugin.
        See http://www.glfw.org/docs/latest/input_guide.html#path_drop for
        more information.
        """
        return False

    def on_window_resize(self, window, w, h):
        """
        gets called when user resizes window.
        window is the glfw window handle of the resized window.
        """
        pass

    def on_notify(self, notification):
        """
        this gets called when a plugin wants to notify all others.
        notification is a dict in the format {'subject':'notification_category.notification_name',['addional_field':'blah']}
        implement this fn if you want to deal with notifications
        note that notifications are collected from all threads and processes and dispatched in the update loop.
        this callback happens in the main thread.
        """
        pass

    # if you want a session persistent plugin implement this function:
    def get_init_dict(self):
        # raise NotImplementedError() if you dont want you plugin to be persistent.

        d = {self}
        # add all aguments of your plugin init fn with paramter names as name field
        # do not include g_pool here.
        return d

    def deinit_ui(self):
        """
        Called when the context will have a ui with window. You can do your deinit for that here.
        """
        pass
        
        