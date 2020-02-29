# MPU6050 9-DoF Example Printout

from sensors.IMU.mpu9250_i2c import *

time.sleep(1)  # delay necessary to allow mpu9250 to settle

print('recording data')
while 1:
    try:
        ax, ay, az, wx, wy, wz = mpu6050_conv()  # read and convert mpu6050 data
        mx, my, mz = AK8963_conv()  # read and convert AK8963 magnetometer data
    except:
        continue

    print('{}'.format('-' * 30))
    print('accel [g]: x = , y = , z = '.format(ax, ay, az))
    print('gyro [dps]:  x = , y = , z = '.format(wx, wy, wz))
    print('mag [uT]:   x = , y = , z = '.format(mx, my, mz))
    print('{}'.format('-' * 30))
    time.sleep(1)
