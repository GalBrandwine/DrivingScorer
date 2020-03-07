import statistics
from collections import deque
from threading import Lock
from threading import Thread

import numpy as np

from sensors.IMU import imu
from utils.logger import Logger

# import a spcecific sensor
# import imu as imu
try:
    import sensors.IMU.mpu9250_i2c as mpu9250
except Exception as e:
    # ON laptop - theres no GPIO, must use mock
    print(e)
    mpu9250 = None
    pass


class DrivingScorer:

    def __init__(self, logging_target: str, is_sim=False, is_mock=True):
        self._THREAD_INTERVAL_MS = 20  # 50 hz
        self._MAXNUMBEROFSCORES = 50  # fill queue with new data every 1 second

        self._sensor = imu.Imu(is_sim=is_sim, is_mock=is_mock, sensor=mpu9250)
        self.logger = Logger(logging_target)
        self._keep_running: bool = True
        self._threaded_data_recorder: Thread = None

        self._data_lock = Lock()

        self._data_container: np.array([]) = np.zeros((1, 6))
        self._data_queue = deque(maxlen=self._MAXNUMBEROFSCORES)
        self._input_ticks = 1000 / self._THREAD_INTERVAL_MS
        self._warm_up_time_passed = False
        self._first_10_seconds = 10
        self._std_dev = np.zeros((1, 6))  # Std per axe

        # self._t_vec = np.zeros((self._MAXNUMBEROFSCORES, 6))
        # self._raw_data: np.array([]) = np.zeros(
        #     (self._MAXNUMBEROFSCORES, 6))
        # self._total_raw_data: np.array([]) = np.zeros((self._MAXNUMBEROFSCORES, 6))
        #
        # self._score_sum: float = 0
        # self._average_score: float = 1.0
        # self._number_of_scores: float = 1.0
        # self._current_driving_score: float = 0
        # self._previous_normalized_sensor_data: np.array([]) = np.random.uniform(-1, 1, 6)
        # self._driving_scores_arr: np.array([]) = np.zeros(self._MAXNUMBEROFSCORES)
        #
        # self._maximum_data_point: float = 0
        # self._minimum_data_point: float = 0

    def _process_data(self, label):
        import time
        self._keep_running = True

        while self._keep_running:
            data = self._sensor.get_data()

            with self._data_lock:  # Critical section

                self._preprocess_data(data)
                self._record_data(data, label)
                # self._t_vec.append(time.time())  # capture timestamp
                # self._t_vec = np.roll(self._t_vec, -1)  # Shift left by one.
                # self._t_vec[
                #     self._MAXNUMBEROFSCORES - 1] = time.time()

                if self._input_ticks < 0:  # Happen every 1 second
                    self._input_ticks = 1000 / self._THREAD_INTERVAL_MS

                    if self._warm_up_time_passed is True:
                        self._score_drive()
                    else:
                        if self._first_10_seconds >= 0:
                            print("Warming up.. %d sec left" % self._first_10_seconds)
                            self._first_10_seconds = self._first_10_seconds - 1

                        else:
                            print("Done warming up.")
                            self._std_dev = [[statistics.stdev(self._data_container[:, axe]) for axe in range(6)]]
                            print("Sensor noise per ax:")
                            print(self._std_dev)

                            self._data_container = np.zeros((1, 6))  # Clean data container
                            self._warm_up_time_passed = True

                    # print("RESETED")

            self._input_ticks = self._input_ticks - 1
            time.sleep(self._THREAD_INTERVAL_MS / 1000.0)

    def _record_data(self, data: np.array([]), label: str):
        self.logger.log_info("%f, %f, %f,%f, %f, %f, %s", data[0], data[1], data[2], data[3], data[4], data[5], label)

    def start(self, label) -> None:
        self._threaded_data_recorder = Thread(target=self._process_data, args=(label,))
        self._threaded_data_recorder.start()

    def stop(self) -> None:
        self._keep_running = False
        self._threaded_data_recorder.join()

    def get_scoring(self) -> (float, float):
        with self._data_lock:
            return self._current_driving_score, self._average_score

    def get_raw_data(self) -> (np.array([]), list):
        with self._data_lock:
            t_vec = np.subtract(self._t_vec, self._t_vec[0])
            return self._raw_data, t_vec

    def get_score_arr(self) -> (np.array([]), list):
        with self._data_lock:
            t_vec = np.subtract(self._t_vec, self._t_vec[0])
            return self._driving_scores_arr, t_vec

    def _score_drive(self) -> None:
        """
        Naive way for scoring a drive.
        :param data: Updated sensor data.
        :return: None
        """

        # self._raw_data = np.concatenate((self._raw_data, [data]), axis=0)
        # distance_between_current_data_and_prev = np.linalg.norm(self._total_raw_data[-1] - data)
        # print("distance_between_current_data_and_prev: ".format(distance_between_current_data_and_prev))
        # self._total_raw_data = np.concatenate((self._total_raw_data, [data]), axis=0)
        #
        # # print(np.mean(self._total_raw_data,axis=0))
        # # print((np.mean(np.mean(self._total_raw_data,axis=0))))
        #
        # # print((np.average(np.average(self._total_raw_data,axis=0))))
        #
        # self._raw_data = np.roll(self._raw_data, -1)  # Shift left by one.
        # self._raw_data[
        #     self._MAXNUMBEROFSCORES - 1] = data
        #
        # self._update_min_and_max(data)
        # normalized_current_data = self._normalize_current_data(data)
        #
        # current_normalized_datascore_between_0_to_1 = self._get_norm_of_normalized_current_data(normalized_current_data)
        # # print(current_normalized_datascore_between_0_to_1)
        # self._update_scores_arr(current_normalized_datascore_between_0_to_1)

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

    def _preprocess_data(self, data: np.array([])):
        """
        Add new data to cyclic data queue - for grading.

        NOTE: self._std_dev should be filled with zeros until the end of the warm-up.
        :param data: raw-data from sensor
        :return:
        """
        denoised_data = data - self._std_dev
        self._data_container = np.concatenate((self._data_container, denoised_data), axis=0)
        # self._data_queue.append(data)


if __name__ == "__main__":
    import time

    driving_scorer = DrivingScorer("CSV", is_sim=True,
                                   is_mock=False)
    driving_scorer.logger.log_info("Main    : before creating thread")

    driving_scorer.start("Gal")

    nump_of_scores = 1000
    while nump_of_scores > 0:
        # data, t_vect = driving_scorer.get_raw_data()
        # current_score = driving_scorer.get_scoring()
        # print(current_score)
        nump_of_scores = nump_of_scores - 1

        time.sleep(0.2)

    driving_scorer.stop()
    print("main end")
