from sensors.IMU.imu import Imu

if __name__ == "__main__":
    imu = Imu(is_mock=True)
    print(imu.get_data())
