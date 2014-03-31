import sys,os,platform
# We are running in a normal Python environment.
# Make all pupil shared_modules available to this Python session.
pupil_base_dir = os.path.abspath(__file__).rsplit('pupil_src', 1)[0]
sys.path.append(os.path.join(pupil_base_dir, 'pupil_src', 'shared_modules'))

from time import sleep
from time import time
import cv2
import numpy as np
from glfw import *
from gl_utils import basic_gl_setup, adjust_gl_view, draw_gl_texture, clear_gl_screen, draw_gl_point_norm,draw_gl_texture,make_coord_system_norm_based
if platform.system() == 'Linux':
    # here we use a different timesource in uvc capture.
    from c_methods import c_time as time
from uvc_capture.linux_video.v4l2_capture import dll 
get_time_monotonic = dll.get_time_monotonic
def main():

    # Callback functions
    def on_resize(window,w, h):
        adjust_gl_view(w,h,window)

    # Initialize glfw
    glfwInit()
    window = glfwCreateWindow(400, 100, "latency test", None, None)
    glfwMakeContextCurrent(window)
    glfwSetWindowSizeCallback(window,on_resize)

    basic_gl_setup()
    make_coord_system_norm_based()
    # refresh speed settings
    glfwSwapInterval(0)

    def refresh_time():
        old_time, bar.timestamp = bar.timestamp, time()
        dt = bar.timestamp - old_time
        if dt:
            bar.fps.value += .05 * (1. / dt - bar.fps.value)


    timestamp = get_time_monotonic()
    d = 0
    while not glfwWindowShouldClose(window):

        t = get_time_monotonic()
        dif, timestamp = t-timestamp,t
        img = np.zeros((100,400,3),dtype=np.uint8)
        time_str = '%.6f : %.6f'%(timestamp+dif,dif) # we add the dif as it is the daly we know will happen on swap buffers.
        # time_str  = str(timestamp) + ' : ' + str(dif)
        # print time_str
        if not d:
            cv2.putText(img, time_str, (-10,80), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255,255,255), thickness=1)#[, thickness[, lineType[, bottomLeftOrigin]]])
            d = 4
        d -=1

        draw_gl_texture(img)
        glfwSwapBuffers(window)
        glfwPollEvents()
        sleep(.001)

if __name__ == '__main__':
    main()
