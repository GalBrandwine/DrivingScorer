# MPU6050 9-DoF Example Printout

import time


import os
import sys

# Simple path fixes
cwd = os.getcwd()
sys.path.insert(0, cwd)

# import mpu9250_i2c as mpu9250
import imu as imu

time.sleep(1)  # delay necessary to allow mpu9250 to settle

print("Initiating IMU")
imu = imu.Imu(is_mock=True)
print('recording data')
while 1:
    try:

        ax, ay, az, wx, wy, wz = imu.get_data()  # read and convert mpu6050 data

        # mx, my, mz = mpu9250.AK8963_conv()  # read and convert AK8963 magnetometer data
    except:
        continue

    print('{}'.format('-' * 30))
    print('accel [g]: x = {}, y = {}, z = {}'.format(ax, ay, az))
    print('gyro [dps]:  x = {}, y = {}, z = {}'.format(wx, wy, wz))
    # print('mag [uT]:   x = , y = , z = '.format(mx, my, mz))
    print('{}'.format('-' * 30))
    time.sleep(0.1)
