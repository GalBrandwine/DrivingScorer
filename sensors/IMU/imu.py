import numpy as np


class Imu:
    def __init__(self, is_mock=False):
        self._is_mock = is_mock
        if self._is_mock is True:
            print("IMU mock activated")

        self._data = np.array([])

    def get_data(self) -> np.array([]):
        if self._is_mock is True:
            self._data = [np.random.randint(-50, 50), np.random.randint(-50, 50), np.random.randint(-50, 50)]
            return self._data
