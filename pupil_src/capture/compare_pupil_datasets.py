import numpy as np
import os
import cv2

import scipy.spatial as sp

# make shared modules available across pupil_src
from sys import path as syspath
from os import path as ospath
loc = ospath.abspath(__file__).rsplit('pupil_src', 1)
syspath.append(ospath.join(loc[0], 'pupil_src', 'shared_modules'))

from uvc_capture import autoCreateCapture, FileCaptureError, EndofVideoFileError, CameraCaptureError



def main(data_dir):


    hand_labeled_data_txt_path = os.path.join(data_dir,'pupil-ellipses.txt')
    pupil_labeled_data_npy_path = os.path.join(data_dir,'pupil_detected_ellipses.npy')
    video_path  = os.path.join(data_dir,'test.avi')


    pupil_data = np.load(pupil_labeled_data_npy_path) # frame,x,y,a,b,angle between the horizontal axis and 'a' in degrees
    ground_truth = [] # frame,x,y,major radius,minor radius ,angle of the major axis with the x-axis (in radians)
    with open(hand_labeled_data_txt_path,'r') as f:
        for l in f:
            l = l.replace(" |",'')
            datum = map(float,l.split(' '))
            ground_truth.append(datum)
    ground_truth_by_index = dict([(e[0],e[1:]) for e in ground_truth ])
    cap = autoCreateCapture(video_path)

    results = []
    while True:
        # Get an image from the grabber
        try:
            frame = cap.get_frame()
        except CameraCaptureError:
            print "Capture from Camera Failed. Stopping."
            break
        except EndofVideoFileError:
            print "Video File is done. Stopping"
            break
        frame_index = cap.get_frame_index()-1

        cv2.imshow("bare",frame.img)


        pupil_ellipse = pupil_data[frame_index]
        e_img = np.zeros(frame.img.shape,dtype=np.uint8)
        cv2.ellipse(frame.img,((pupil_ellipse[1],pupil_ellipse[2]),
                                        (pupil_ellipse[3],pupil_ellipse[4]),
                                        pupil_ellipse[5]),(0,0,255))
        cv2.ellipse(e_img,((pupil_ellipse[1],pupil_ellipse[2]),
                                        (pupil_ellipse[3],pupil_ellipse[4]),
                                        pupil_ellipse[5]),(255,255,255))
        pupil_poly = cv2.findNonZero(e_img[:,:,0])
        pupil_poly.shape=(-1,2)

        true_ellipse = ground_truth_by_index.get(frame_index,None)
        if true_ellipse:
            e_img = np.zeros(frame.img.shape,dtype=np.uint8)
            cv2.ellipse(frame.img,((true_ellipse[0],true_ellipse[1]),
                                        (true_ellipse[2]*2,true_ellipse[3]*2),
                                        true_ellipse[4]*(360./(2*np.pi))),(0,255,0))
            cv2.ellipse(e_img,((true_ellipse[0],true_ellipse[1]),
                                        (true_ellipse[2]*2,true_ellipse[3]*2),
                                         true_ellipse[4]*(360./(2*np.pi))),(255,255,255))
            true_poly = cv2.findNonZero(e_img[:,:,0])
            true_poly.shape=(-1,2)

            d_matrix = sp.distance.cdist(true_poly,pupil_poly)
            results.append(max(np.min(d_matrix,0)))
            print max(np.min(d_matrix,0))

            cv2.imshow("result",frame.img)
            k = cv2.waitKey(1)
            if k == 27:         # wait for ESC key to exit
                cv2.destroyAllWindows()
                break

    return results
def calc_results(results):

    results = np.array(results)
    h,bins = np.histogram(results,500,(0,500))
    print h
    h = np.cumsum(h)
    h *= 100./len(results)
    return h

if __name__ == '__main__':
    # r0 = main('/Users/mkassner/Pupil/datasets/p2-right/frames/')
    # r1 = main('/Users/mkassner/Pupil/datasets/p1-left/frames/')
    # r2 = main('/Users/mkassner/Pupil/datasets/p2-left/frames/')
    # # r3 = main('/Users/mkassner/Pupil/datasets/p1-right/frames/')

    # r = r0 + r2 + r2 #+r3
    # r = np.array(r)
    # h = calc_results(r)
    # np.save("pupil_results.npy",h)
    h = np.load("pupil_results.npy")
    from matplotlib import pyplot as plt
    fig = plt.plot(h)
    fig.show()

