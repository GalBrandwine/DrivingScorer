import numpy as np


class Imu:
    def __init__(self, is_mock=False):
        self._is_mock = is_mock
        if self._is_mock is True:
            print("IMU mock activated")

        self._data: np.array([]) = np.array([])

    def get_data(self) -> np.array([]):
        if self._is_mock is True:
            self._data = np.random.uniform(-50, 50, 3)
            return self._data
