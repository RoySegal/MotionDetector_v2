import multiprocessing
import queue
import cv2
import imutils
import numpy as np

AREA = 500


class Detector(multiprocessing.Process):
    def __init__(self, frames_queue, detection_queue):
        super(Detector, self).__init__()
        self.frames_queue = frames_queue
        self.detection_queue = detection_queue

    def motion_detector(self):
        firstFrame = None

        # loop over the frames of the video
        while True:
            # grab the current frame and initialize the occupied/unoccupied
            # text
            frame = self.frames_queue.get(block=True, timeout=4)

            # resize the frame, convert it to grayscale, and blur it
            # copy the frame in order not to change it
            changed_frame = np.copy(imutils.resize(frame, width=500))
            gray = cv2.cvtColor(changed_frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            pos_arr = []
            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < AREA:
                    continue
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                pos_arr.append([x, y, w, h])

            self.detection_queue.put([changed_frame, pos_arr])

    def run(self):
        try:
            self.motion_detector()
        except queue.Empty:
            pass
        finally:
            pass