from micropython import const
from machine import I2C, Pin


VISUAL_ROTARY_ENCODER_DEFAULT_I2C_ADDR = const(0x54)


class DFRobot_VisualRotaryEncoder:
    """
    MicroPython class for communication with the Rotary Encoder from DFRobot via I2C
    """

    VISUAL_ROTARY_ENCODER_PID = const(0x01F6)
    VISUAL_ROTARY_ENCODER_PID_MSB_REG = const(0x00)
    VISUAL_ROTARY_ENCODER_COUNT_MSB_REG = const(0x08)
    VISUAL_ROTARY_ENCODER_KEY_STATUS_REG = const(0x0A)
    VISUAL_ROTARY_ENCODER_GAIN_REG = const(0x0B)

    def __init__(self, sda, scl, i2c_addr=VISUAL_ROTARY_ENCODER_DEFAULT_I2C_ADDR, i2c_bus=0):
        """
        Initialize the DFRobot_GNSS communication
        :param sda: I2C SDA Pin
        :param scl: I2C SCL Pin
        :param i2c_addr: I2C address
        :param i2c_bus: I2C bus number
        """
        self._addr = i2c_addr

        try:
            self._i2c = I2C(i2c_bus, sda=Pin(sda), scl=Pin(scl), freq=100000)
        except Exception as err:
            print(f'Could not initialize i2c! bus: {i2c_bus}, sda: {sda}, scl: {scl}, error: {err}')

    def _write_reg(self, reg, data) -> None:
        """
        Write data to the I2C register
        :param reg: register address
        :param data: data to write
        :return: None
        """
        if isinstance(data, int):
            data = [data]

        try:
            self._i2c.writeto_mem(self._addr, reg, bytearray(data))
        except Exception as err:
            print(f'Write issue: {err}')

    def _read_reg(self, reg, length) -> bytes:
        """
        Reads data from the I2C register
        :param reg: I2C register address
        :param length: number of bytes to read
        :return: bytes
        """
        try:
            result = self._i2c.readfrom_mem(self._addr, reg, length)
        except Exception as err:
            print(f'Read issue: {err}')
            result = [0, 0]

        return result

    def set_gain_coefficient(self, gain_value: int) -> None:
        """
        Set the current gain factor of the encoder, and the numerical accuracy of turning one-step
        accuracy range：1~51，the minimum is 1 (light up one LED about every 2.5 turns),
        the maximum is 51 (light up one LED every one-step rotation)
        :param gain_value: gain_value range[1, 51], the setting is invalid when out of range
        :return: None
        """
        if 0x01 <= int(gain_value) <= 0x33:
            self._write_reg(self.VISUAL_ROTARY_ENCODER_GAIN_REG, int(gain_value))

    def set_encoder_value(self, value: int) -> None:
        """
        Set the encoder count
        :param value: value range[0, 1023], the setting is invalid when out of range
        :return: None
        """
        if 0x0000 <= int(value) <= 0x3FF:
            temp_buf = [(int(value) & 0xFF00) >> 8, int(value) & 0x00FF]
            self._write_reg(self.VISUAL_ROTARY_ENCODER_COUNT_MSB_REG, temp_buf)

    def get_device_info(self) -> str:
        """
        Get the device PID, VID, version and I2C address
        :return: string
        """
        data = self._read_reg(self.VISUAL_ROTARY_ENCODER_PID_MSB_REG, 8)

        pid = (data[0] << 8) | data[1]
        vid = (data[2] << 8) | data[3]
        version = (data[4] << 8) | data[5]
        i2c_addr = data[7]

        return f'PID: {pid}, VID: {vid}, Version: {version}, I2C: {i2c_addr}'

    def get_encoder_value(self) -> int:
        """
        Get the current encoder count
        :return: value range： 0-1023
        """
        data = self._read_reg(self.VISUAL_ROTARY_ENCODER_COUNT_MSB_REG, 2)
        return (data[0] << 8) | data[1]

    def get_gain_coefficient(self) -> int:
        """
        Get the current gain factor of the encoder, and the numerical accuracy of turning one-step
        accuracy range：1~51，the minimum is 1 (light up one LED about every 2.5 turns),
        the maximum is 51 (light up one LED every one-step rotation)
        :return: value range： 1-51
        """
        return self._read_reg(self.VISUAL_ROTARY_ENCODER_GAIN_REG, 1)[0]

    def detect_button_down(self) -> bool:
        """
        Detect if the button is pressed
        :return: bool
        """
        if 1 == self._read_reg(self.VISUAL_ROTARY_ENCODER_KEY_STATUS_REG, 1)[0]:
            self._write_reg(self.VISUAL_ROTARY_ENCODER_KEY_STATUS_REG, 0)
            return True
        else:
            return False
