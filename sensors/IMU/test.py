from sensors.IMU.imu_mock import Imu

if __name__ == "__main__":
    imu = Imu(is_mock=True)
    print(imu.get_data())
