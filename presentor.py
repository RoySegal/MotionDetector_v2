import multiprocessing
import queue
import cv2
import datetime

X_POS = 0
Y_POS = 1
W_POS = 2
H_POS = 3

class Presentor(multiprocessing.Process):
    def __init__(self, detection_queue):
        super(Presentor, self).__init__()
        self.detection_queue = detection_queue

    def run(self):
        try:
            while True:
                frame, pos_arr = self.detection_queue.get(block=True, timeout=2)
                for position in pos_arr:
                    cv2.rectangle(frame, (position[X_POS], position[Y_POS]), (position[X_POS] + position[W_POS], position[Y_POS] + position[H_POS]), (0, 255, 0), 2)
                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                cv2.imshow('frame', frame)
                cv2.waitKey(1)

            cv2.destroyAllWindows()

        except queue.Empty:
            pass
        finally:
            pass




