import numpy as np


class Imu:
    def __init__(self, use_case="sensor", sensor=None):
        self._use_case = use_case
        self._imu = sensor
        if self._use_case == "sensor":
            print("IMU with sensor activated")
        elif self._use_case == "mock":
            print("IMU mock activated")

        elif self._use_case == "simulator":
            print("SIMULATOR activated")
            import PySimpleGUI as sg
            import pandas as pd
            record_path = sg.PopupGetFile('Enter the desired record for simulation')

            self._df = pd.read_csv(record_path)
            self._num_of_rows = self._df.shape[0]
            self._current_row = 0
        else:
            message = "NO SUCH IMU USECASE. Possible usecases: sensor,simulator,mock"
            raise Exception(message)

        self._data: np.array([]) = np.array([])

    def get_data(self) -> np.array([]):
        if self._use_case == "mock":
            self._data = np.random.uniform(-10, 10, 6)  # ax, ay, az, wx, wy, wz
            return self._data
        if self._use_case == "simulator":
            if self._current_row < self._num_of_rows:
                self._data = self._df.iloc[self._current_row,
                             1:-1].values  # ax, ay, az, wx, wy, wz (skip TimeStamp, and Label)
                self._current_row = self._current_row + 1
                return self._data
            return np.zeros((6))
        if self._use_case == "sensor":
            self._data = np.array(self._imu.mpu6050_conv())
            return self._data
