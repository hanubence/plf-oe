from machine import I2C, Pin, RTC, SDCard, SPI
from sensors import MPU9250, MLX90614, DS1307, INMP441


MPU_I2C_ADDR = 0x69
TEMP_I2C_ADDR = 0x5A
RTC_I2C_ADDR = 0x68

SD_MOUNT_POINT = '/sd'

class Moo:

    def __init__(self) -> None:
        self._init_i2c()
        self._init_spi()
        # self._init_sd()
        # self._init_mic()

    def _init_mic(self):
        print('Initializing INMP441 microphone')
        self.mic = INMP441()
        print('INMP441 microphone initialized')

    def _init_i2c(self):
        print('Initializing I2C sensors (RTC, TEMP, GYRO, ACCEL)')
        self.i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
        self._mpu9250 = MPU9250(self.i2c, address=MPU_I2C_ADDR)
        self._mlx90614 = MLX90614(self.i2c, address=TEMP_I2C_ADDR)
        self._rtc = DS1307(self.i2c, addr=RTC_I2C_ADDR)

        RTC().datetime(self._rtc.datetime())
        print('I2C sensors initialized')

    def _init_spi(self):
        print('Initializing SPI')
        try:
            self.spi = SPI(1, baudrate=100000, polarity=0, phase=0)
            print('SPI initialized')
        except Exception as e:
            print('SPI failed to initialize: ', e)

    def _init_sd(self):
        print('Initializing SD card')
        try:
            import os
            self.sd = SDCard(slot=2)
            os.mount(self.sd, SD_MOUNT_POINT)
            print('SD card initialized')
        except Exception as e:
            print('SD card failed to initialize: ', e)

    def record_audio(self, seconds, filename):
        self.mic.record(self.sd, seconds, filename)

    @property
    def i2c_addresses(self):
        return self.i2c.scan()
    
    @property
    def acc(self):
        return self._mpu9250.acceleration
    
    @property
    def gyro(self):
        return self._mpu9250.gyro
    
    @property
    def ambient_temp(self):
        return self._mlx90614.ambient_temp
    
    @property
    def object_temp(self):
        return self._mlx90614.object_temp
    
    @property
    def datetime(self):
        return self._rtc.datetime()
    
    @property
    def pretty_data(self):
        '''
        example:
        |-------[12:34:56]-------|
        |--------[ACCEL.]--------|
        | X: 0.0000000           |
        | Y: 0.0000000           |
        | Z: 0.0000000           |
        |---------[GYRO]---------|
        | X: 0.0000000           |
        | Y: 0.0000000           |
        | Z: 0.0000000           |
        |---------[TEMP]---------|
        | Ambient: 25.0          |
        | Object temp: 25.0      |
        |------------------------|
        '''
        time = self.datetime
        ret = ""
        ret += f"|-------[{time[4]:02}:{time[5]:02}:{time[6]:02}]-------|\n"
        ret += f"|--------[ACCEL.]--------|\n"
        ret += f"| X: {self.acc[0]:.7f}           |\n"
        ret += f"| Y: {self.acc[1]:.7f}           |\n"
        ret += f"| Z: {self.acc[2]:.7f}          |\n"
        ret += f"|---------[GYRO]---------|\n"
        ret += f"| X: {self.gyro[0]:.7f}           |\n"
        ret += f"| Y: {self.gyro[1]:.7f}           |\n"
        ret += f"| Z: {self.gyro[2]:.7f}          |\n"
        ret += f"|---------[TEMP]---------|\n"
        ret += f"| Ambient: {self.ambient_temp:.2f}         |\n"
        ret += f"| Object temp: {self.object_temp:.2f}     |\n"
        ret += f"|------------------------|\n"
        return ret