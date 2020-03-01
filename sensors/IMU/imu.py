import numpy as np


class Imu:
    def __init__(self, is_mock=False, sensor=None, ):
        self._is_mock = is_mock
        self._imu = sensor
        if self._is_mock is True:
            print("IMU mock activated")

        self._data: np.array([]) = np.array([])

    def get_data(self) -> np.array([]):
        if self._is_mock is True:
            self._data = np.random.uniform(-1, 1, 6)  # ax, ay, az, wx, wy, wz
            return self._data
        else:
            self._data = self._imu.mpu6050_conv()
