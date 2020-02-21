from threading import Lock
from threading import Thread

import numpy as np

from sensors.IMU import imu
from utils.logger import Logger


class DrivingScorer:

    def __init__(self, logging_target: str, is_mock=False):
        self._sensor = imu.Imu(is_mock)
        self.logger = Logger(logging_target)
        self._keep_running: bool = True
        self._threaded_data_recorder: Thread = None

        self._data_lock = Lock()

        self._current_driving_score: float = 0
        # self._average_driver_score: float = 0
        self._current_acceleration_deltas: np.array([]) = np.zeros(3)
        self._previous_sensor_data: np.array([]) = np.zeros(3)
        self._driving_scores_arr: np.array([]) = np.array([])

    def _proccess_data(self, label):
        self._keep_running = True

        while self._keep_running:
            data = self._sensor.get_data()
            with self._data_lock:
                # Critical section
                self._score_drive(data)
                self._record_data(data, label)

    def _record_data(self, data: np.array([]), label: str):
        self.logger.log_info("%f, %f, %f,%s", data[0], data[1], data[2],
                             label)  # format: data[0],data[1],data[2],label

    def start(self, label) -> None:
        self._threaded_data_recorder = Thread(target=self._proccess_data, args=(label,))
        self._threaded_data_recorder.start()

    def stop(self) -> None:
        self._keep_running = False
        self._threaded_data_recorder.join()

    def get_current_score(self) -> float:
        with self._data_lock:
            return self._current_driving_score

    def get_deltas(self) -> np.array([]):
        with self._data_lock:
            return self._current_acceleration_deltas

    def _score_drive(self, data: np.array([])) -> None:
        """
        Naive way for scoring a drive.
        :param data: Updated sensor data.
        :return: float current scoring
        """
        current_score = np.linalg.norm(data - self._previous_sensor_data)
        self._current_driving_score = current_score
        self._driving_scores_arr = np.append(self._driving_scores_arr, current_score)
        self._current_acceleration_deltas = np.subtract(data, self._previous_sensor_data)
        self._previous_sensor_data = data


if __name__ == "__main__":
    import time

    driving_scorer = DrivingScorer("CONSOLE",
                                   is_mock=True)
    driving_scorer.logger.log_info("Main    : before creating thread")

    driving_scorer.start("Gal")

    time.sleep(3)
    driving_scorer.stop()
    print("main end")
