from machine import I2C
import time

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Wake up MPU6050
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')
        time.sleep_ms(100)

    def _int16(self, high, low):
        value = (high << 8) | low
        if value & 0x8000:
            value -= 65536
        return value

    def read_raw(self):
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
        return {
            'accel_x': self._int16(data[0], data[1]),
            'accel_y': self._int16(data[2], data[3]),
            'accel_z': self._int16(data[4], data[5]),
            'temp': self._int16(data[6], data[7]),
            'gyro_x': self._int16(data[8], data[9]),
            'gyro_y': self._int16(data[10], data[11]),
            'gyro_z': self._int16(data[12], data[13])
        }

    def get_accel(self):
        raw = self.read_raw()
        ax = raw['accel_x'] / 16384.0
        ay = raw['accel_y'] / 16384.0
        az = raw['accel_z'] / 16384.0
        return ax, ay, az

    def get_gyro(self):
        raw = self.read_raw()
        gx = raw['gyro_x'] / 131.0
        gy = raw['gyro_y'] / 131.0
        gz = raw['gyro_z'] / 131.0
        return gx, gy, gz

    def is_moving(self, threshold=0.2):
        ax, ay, az = self.get_accel()
        diff = abs(ax) + abs(ay) + abs(az - 1.0)
        return diff > threshold
