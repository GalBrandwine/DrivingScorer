from threading import Lock
from threading import Thread

import numpy as np

from sensors.IMU import imu
from utils.logger import Logger


class DrivingScorer:

    def __init__(self, logging_target: str, is_mock=False):
        self._THREAD_INTERVAL_MS = 20
        self._MAXNUMBEROFSCORES = 100
        self._sensor = imu.Imu(is_mock)
        self.logger = Logger(logging_target)
        self._keep_running: bool = True
        self._threaded_data_recorder: Thread = None

        self._data_lock = Lock()

        self._score_sum: float = 0
        self._average_score: float = 1.0
        self._number_of_scores: float = 1.0
        self._current_driving_score: float = 0
        self._previous_normalized_sensor_data: np.array([]) = np.random.uniform(0, 1, 3)
        self._driving_scores_arr: np.array([]) = np.zeros(self._MAXNUMBEROFSCORES)

        self._maximum_data_point: float = 0
        self._minimum_data_point: float = 0

    def _process_data(self, label):
        import time
        self._keep_running = True

        while self._keep_running:
            data = self._sensor.get_data()
            with self._data_lock:
                # Critical section
                self._score_drive(data)
                self._record_data(data, label)

            time.sleep(self._THREAD_INTERVAL_MS / 1000.0)

    def _record_data(self, data: np.array([]), label: str):
        self.logger.log_info("%f, %f, %f,%s", data[0], data[1], data[2], label)

    def start(self, label) -> None:
        self._threaded_data_recorder = Thread(target=self._process_data, args=(label,))
        self._threaded_data_recorder.start()

    def stop(self) -> None:
        self._keep_running = False
        self._threaded_data_recorder.join()

    def get_scoring(self) -> (float, float):
        with self._data_lock:
            return self._current_driving_score, self._average_score

    def get_score_arr(self) -> np.array([]):
        with self._data_lock:
            return self._driving_scores_arr

    def _score_drive(self, data: np.array([])) -> None:
        """
        Naive way for scoring a drive.
        :param data: Updated sensor data.
        :return: None
        """

        self._update_min_and_max(data)

        normalized_current_data = self._normalize_current_data(data)
        current_normalized_datascore_between_0_to_1 = self._get_norm_of_normalized_current_data(normalized_current_data)
        self._update_scores_arr(current_normalized_datascore_between_0_to_1)

    def _update_min_and_max(self, data):
        temp_min = data.min()
        temp_max = data.max()

        self._maximum_data_point = temp_max if temp_max > self._maximum_data_point else self._maximum_data_point
        self._minimum_data_point = temp_min if temp_min < self._minimum_data_point else self._minimum_data_point

    def _normalize_current_data(self, data: np.array([])) -> np.array([]):
        return (data - self._minimum_data_point) / (self._maximum_data_point - self._minimum_data_point)

    def _get_norm_of_normalized_current_data(self, normalized_current_data: np.array([])) -> np.array([]):
        """
        Normalize data to range between 0 and 1.
        :param normalized_current_data:
        :return: normal of current normalized data in the values between 0 to 1
        """
        normalized_current_data_between_0_to_1 = np.linalg.norm(
            normalized_current_data - self._previous_normalized_sensor_data)
        self._previous_normalized_sensor_data = normalized_current_data

        return normalized_current_data_between_0_to_1

    def _update_scores_arr(self, current_normalized_datascore_between_0_to_1):
        """
        Add most updated normalized values to the end of the scores_arr,
        while maintaining all previews data using a shift left method.
        :param current_normalized_datascore_between_0_to_1: Updated and normalized scoring per current data sample.
        :return: None
        """
        self._driving_scores_arr = np.roll(self._driving_scores_arr, -1)  # Shift left by one.
        self._driving_scores_arr[
            self._MAXNUMBEROFSCORES - 1] = 1 - current_normalized_datascore_between_0_to_1  # Add to the end.
        self._update_current_score(current_normalized_datascore_between_0_to_1)

    def _update_current_score(self, current_normalized_score) -> None:
        self._current_driving_score = 1 - current_normalized_score
        self._score_sum = self._score_sum + self._current_driving_score
        self._number_of_scores = self._number_of_scores + 1

        self._average_score = self._score_sum / self._number_of_scores


if __name__ == "__main__":
    import time

    driving_scorer = DrivingScorer("CONSOLE",
                                   is_mock=True)
    driving_scorer.logger.log_info("Main    : before creating thread")

    driving_scorer.start("Gal")

    time.sleep(3)
    driving_scorer.stop()
    print("main end")
