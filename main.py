import multiprocessing
import argparse
from streamer import Streamer
from detector import Detector
from presentor import Presentor

def start_procs(procs):
    for proc in procs:
        proc.start()

def wait_for_procs(procs):
    for proc in procs:
        proc.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('video_path', type=str)
    args = parser.parse_args()

    frames_queue = multiprocessing.Queue()
    detection_queue = multiprocessing.Queue()
    streamer_proc = Streamer(args.video_path, frames_queue)
    detector_proc = Detector(frames_queue, detection_queue)
    presentor_proc = Presentor(detection_queue)

    start_procs([streamer_proc, detector_proc, presentor_proc])

    wait_for_procs([streamer_proc, detector_proc, presentor_proc])

    print("Done")
