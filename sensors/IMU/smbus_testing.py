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

# Create a sawtooth wave 16 times
for i in range(0x10000):

    # get MPU9250 smbus block data
    xyz_a_out = i2c.read_i2c_block_data(address_MPU9250, 0x3B, 6)
    xyz_g_out = i2c.read_i2c_block_data(address_MPU9250, 0x43, 6)
    print("xyz_a_out: {}".format(xyz_a_out))
    # print("xyz_g_out: {}".format(xyz_g_out))
