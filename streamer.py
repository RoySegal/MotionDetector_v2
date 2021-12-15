import multiprocessing
import cv2

class Streamer(multiprocessing.Process):
    def __init__(self, vid_path, frames_queue):
        super(Streamer, self).__init__()
        self.vid_path = vid_path
        self.frames_queue = frames_queue

    def run(self):
        try:
            cap = cv2.VideoCapture(self.vid_path)
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    self.frames_queue.put(frame)
                else:
                    break
            cap.release()
        finally:
            pass
