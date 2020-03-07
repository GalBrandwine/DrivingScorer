import numpy as np


class Imu:
    def __init__(self, is_sim=False, is_mock=False, sensor=None):
        self._is_mock = is_mock
        self._imu = sensor
        if self._is_mock is True:
            print("IMU mock activated")
        self._is_sim = is_sim
        if self._is_sim is True:
            print("SIMULATOR activated")
            import PySimpleGUI as sg
            text = sg.PopupGetFile('Enter the desired record for simulation')
        self._data: np.array([]) = np.array([])

    def get_data(self) -> np.array([]):
        if self._is_mock is True:
            self._data = np.random.uniform(-10, 10, 6)  # ax, ay, az, wx, wy, wz
            return self._data
        if self._is_sim is True:
            self._data = np.random.uniform(-10, 10, 6)  # ax, ay, az, wx, wy, wz
            return self._data
        else:
            self._data = np.array(self._imu.mpu6050_conv())
            # print(self._data)
            return self._data
