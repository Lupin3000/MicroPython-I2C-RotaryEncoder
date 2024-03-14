from micropython import const
from lib.DFRobot_RotaryEncoder_I2C import DFRobot_VisualRotaryEncoder
from time import sleep


SDA_PIN = const(21)
SCL_PIN = const(22)
SECONDS = const(.5)


if __name__ == '__main__':
    rotary_encoder = DFRobot_VisualRotaryEncoder(sda=SDA_PIN, scl=SCL_PIN)

    print(str(rotary_encoder))
    print(f'Encoder current gain coefficient: {rotary_encoder.coefficient()}')

    while True:
        if bool(rotary_encoder):
            print('Encoder button pressed')

        print(f'Encoder value: {rotary_encoder.value()}')
        sleep(SECONDS)
