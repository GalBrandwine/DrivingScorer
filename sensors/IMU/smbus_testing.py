# i2ctest.py
# A brief demonstration of the Raspberry Pi I2C interface, using the Sparkfun
# Pi Wedge breakout board and a SparkFun MCP4725 breakout board:
# https://www.sparkfun.com/products/8736

import smbus

# I2C channel 1 is connected to the GPIO pins
channel = 1

#  MCP4725 defaults to address 0x60
# address = 0x60

# MPU2950 address
address_MPU9250 = 0x68

# Register addresses (with "normal mode" power-down bits)
reg_write_dac = 0x40

# Initialize I2C (SMBus)
i2c = smbus.SMBus(channel)


def readXYZ_acc():
    xyz_a_out = i2c.read_i2c_block_data(address_MPU9250, 0x3B, 6)

    x = (xyz_a_out[0] | xyz_a_out[1] << 8)
    x = x if x < 32768 else x - 65536

    y = (xyz_a_out[2] | xyz_a_out[3] << 8)
    y = y if y < 32768 else y - 65536

    z = (xyz_a_out[4] | xyz_a_out[5] << 8)
    z = z if z < 32768 else z - 65536
    # return mag_combined  if mag_combined < 32768 else mag_combined - 65536
    return x, y, z


# Create a sawtooth wave 16 times
for i in range(0x10000):
    # get MPU9250 smbus block data
    # xyz_a_out = i2c.read_i2c_block_data(address_MPU9250, 0x3B, 6)
    print(readXYZ_acc())
    # xyz_g_out = i2c.read_i2c_block_data(address_MPU9250, 0x43, 6)
    # print("xyz_a_out: {}".format(xyz_a_out))
    # print("xyz_g_out: {}".format(xyz_g_out))
