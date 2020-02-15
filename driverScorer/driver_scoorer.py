import threading

from sensors.IMU import imu
from utils.logger import Logger


class DrivingScorer:
    def __init__(self, logging_target: str, is_mock=False):
        self._sensor = imu.Imu(is_mock)
        self.logger = Logger(logging_target)
        self._keep_running: bool = True
        self._threaded_data_recorder: threading.Thread = None

    def _start_recording_data(self, label):
        self._keep_running = True
        # self.logger.log_info("Thread %s starting", label)
        while self._keep_running:
            data = self._sensor.get_data()


            self.logger.log_info("%d, %d, %d,%s", data[0], data[1], data[2], label)  # format: data[0],data[1],data[2],label


    def start(self, label):
        self._threaded_data_recorder = threading.Thread(target=self._start_recording_data, args=(label,))
        self._threaded_data_recorder.start()

    def stop(self):
        self._keep_running = False
        self._threaded_data_recorder.join()


if __name__ == "__main__":
    import time

    driving_scorer = DrivingScorer("CONSOLE",
                                   is_mock=True)
    driving_scorer.logger.log_info("Main    : before creating thread")

    driving_scorer.start("Gal")

    time.sleep(3)
    driving_scorer.stop()
    print("main end")
