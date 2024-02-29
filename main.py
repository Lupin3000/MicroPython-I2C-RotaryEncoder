from micropython import const
from lib.DFRobot_RotaryEncoder_I2C import DFRobot_VisualRotaryEncoder
from time import sleep


SDA_PIN = const(21)
SCL_PIN = const(22)
SECONDS = const(1)


if __name__ == '__main__':
    encoder = DFRobot_VisualRotaryEncoder(sda=SDA_PIN, scl=SCL_PIN)

    print(encoder.get_device_info())
    print(f'Encoder current gain coefficient: {encoder.get_gain_coefficient()}')

    while True:
        print(f'Encoder value: {encoder.get_encoder_value()}')
        sleep(SECONDS)
