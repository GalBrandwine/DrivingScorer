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

    def __init__(self, logging_target: str, use_case="sensor"):
        self._THREAD_INTERVAL_MS = 20  # 50 hz
        self._MAXNUMBEROFSCORES = 50  # Fill queue with new data every 1 second

        self._sensor = imu.Imu(use_case=use_case, sensor=mpu9250)
        self.logger = Logger(logging_target)
        self._keep_running: bool = True
        self._threaded_data_recorder: Thread = None

        self._data_lock = Lock()

        self._data_container: np.array([]) = np.zeros((1, 6))
        self._data_queue = deque(maxlen=self._MAXNUMBEROFSCORES)
        self._preprocessed_data_queue = deque(maxlen=self._MAXNUMBEROFSCORES)
        self._input_ticks = 1000 / self._THREAD_INTERVAL_MS
        self._warm_up_time_passed = False
        self._first_10_seconds = 10
        self._std_dev = np.zeros((1, 6))  # Std per axe
        self._scoring_sampling_step = 10
        self._average_score = 6
        self._num_of_scores_so_far = 1
        self._current_driving_score = 6.0  # Driver start with best score.
        self._axis_weights = {
            "AX": 0.35,  # Driving direction
            "AY": 0.35,  # Cause for acceleration changes: Changing lanes aggressively
            "AZ": 0.1,  # Cause for acceleration changes: Path-holes
            "GX": 0.1,  # Cause for acceleration changes: One wheel Path-holes (or two wheels in the same side)
            "GY": 0.1,  # Cause for acceleration changes: Driving into driving-slower bumper
            "GZ": 0,  # Cause for acceleration changes: None?
        }

    def _process_data(self, label):
        import time
        self._keep_running = True

        while self._keep_running:
            data = self._sensor.get_data()

            with self._data_lock:  # Critical section

                self._preprocess_data(data)
                self._record_data(data, label)

                if self._input_ticks < 0:  # Happen every 1 second
                    self._input_ticks = 1000 / self._THREAD_INTERVAL_MS

                    if self._warm_up_time_passed:
                        # Score the driving once a second.
                        self._score_drive()
                    else:
                        if self._first_10_seconds > 0:
                            print("Warming up.. %d sec left" % self._first_10_seconds)
                            self._first_10_seconds = self._first_10_seconds - 1

                        else:
                            print("Done warming up.")
                            self._std_dev = [[statistics.stdev(self._data_container[:, axe]) for axe in range(6)]]
                            print("Sensor noise per ax:")
                            print(self._std_dev)

                            self._data_container = np.zeros((1, 6))  # Clean data container
                            self._warm_up_time_passed = True

            self._input_ticks = self._input_ticks - 1
            time.sleep(self._THREAD_INTERVAL_MS / 1000.0)

    def _record_data(self, data: np.array([]), label: str):
        self.logger.log_info("%f, %f, %f,%f, %f, %f, %s", data[0], data[1], data[2], data[3], data[4], data[5], label)

    def start(self, label) -> None:

        self._threaded_data_recorder = Thread(target=self._process_data, args=(label,))
        self._threaded_data_recorder.start()
        print("Thread started")

    def stop(self) -> None:
        self._keep_running = False
        self._threaded_data_recorder.join()

    def get_scoring(self) -> (float, float):
        with self._data_lock:
            return self._current_driving_score, self._average_score

    def _score_drive(self) -> None:
        """
        Score data using weighted scoring method.

        :param data: Updated sensor data.
        :return: None
        """
        grade = np.zeros((int(self._MAXNUMBEROFSCORES / self._scoring_sampling_step), 6))
        for step in range(int(self._MAXNUMBEROFSCORES / self._scoring_sampling_step)):
            grade[step] = (self._preprocessed_data_queue[self._scoring_sampling_step * step])

        raw_grade_per_axe = grade.sum(axis=0)
        weighted_grade = [raw_grade_per_axe[i] * self._axis_weights[key] for i, key in
                          enumerate(self._axis_weights.keys())]
        res_array = np.array(weighted_grade, dtype=np.float)

        self._current_driving_score = 6 - res_array.sum()  # 6 meaning no acceleration changes at all.

        # Update average scoring, using accumulating average approach:
        #   avg(i) = (i - 1) / i * avg(i - 1) + x(i) / i; (i > 1)
        self._average_score = (
                                          self._num_of_scores_so_far - 1) / self._num_of_scores_so_far * self._average_score + self._current_driving_score / self._num_of_scores_so_far
        self._num_of_scores_so_far = self._num_of_scores_so_far + 1

    def _normalize_current_data(self, distribution_shifted_data: deque) -> np.array([]):
        """
        Normalizing using: 
        
        norm = (data - data.min) / (data.max - data.min)
        
        :param distribution_shifted_data: 
        :return: normalized_data
        """
        normalized_data = np.zeros((self._MAXNUMBEROFSCORES, 6))
        for i, data_sample in enumerate(distribution_shifted_data):
            normalized_data[i] = data_sample

        normalized_data -= normalized_data.min()
        normalized_data /= normalized_data.max()

        return normalized_data

    def _preprocess_data(self, data: np.array([])):
        """
        Add new data to cyclic data queue - for grading.

        NOTE: self._std_dev should be filled with zeros until the end of the warm-up.
        :param data: raw-data from sensor
        :return:
        """

        # Shift data distribution to be 0-centered.
        denoised_data = data - self._std_dev

        if self._first_10_seconds:
            self._data_container = np.concatenate((self._data_container, denoised_data), axis=0)
        else:
            # Warm up time is over.
            # Add shifted data to cyclic queue, that fills every 1 second.
            self._data_queue.append(denoised_data)

            # Step 1: Normalize Data
            normalized_data_shifted_data = self._normalize_current_data(self._data_queue)

            # Step 2: smooth normalized data, using mean on the queue,
            # that performs as a sliding window in size of 1 second
            mean_normalized_data_shifted_data = self._data_smoother(normalized_data_shifted_data)

            # Step 3: Save the preprocessed data for later grading.
            self._accumulate_mean(mean_normalized_data_shifted_data)

    def _data_smoother(self, normalized_shifted_data: deque):
        """
        Smooth data using sliding window-mean.
        :return: None
        """
        data_mean = np.zeros((self._MAXNUMBEROFSCORES, 6))
        for i, data_sample in enumerate(normalized_shifted_data):
            data_mean[i] = data_sample

        return data_mean.mean(axis=0)

    def _accumulate_mean(self, mean_normalized_data_shifted_data):
        self._preprocessed_data_queue.append(mean_normalized_data_shifted_data)

    def set_average(self, user_average):
        self._average_score = user_average

    def get_warm_up_time_left(self):
        return self._first_10_seconds


if __name__ == "__main__":
    import time

    driving_scorer = DrivingScorer("CSV", use_case="simulator")
    driving_scorer.logger.log_info("Main    : before creating thread")

    driving_scorer.start("Gal")

    nump_of_scores = 1000
    while nump_of_scores > 0:
        cur_score = driving_scorer.get_scoring()
        print(cur_score)
        nump_of_scores = nump_of_scores - 1

        time.sleep(0.2)

    driving_scorer.stop()
    print("main end")
