from machine import Pin
import time

class HX711:
    def __init__(self, d_out=None, sck=None, dout=None, pd_sck=None, gain=128):
        if d_out is None and dout is not None:
            d_out = dout
        if sck is None and pd_sck is not None:
            sck = pd_sck
        if d_out is None or sck is None:
            raise ValueError("Specify d_out and sck")

        self.dout = Pin(d_out, Pin.IN)
        self.sck = Pin(sck, Pin.OUT)
        self.gain = gain
        self.offset = 0
        self.sck.value(0)
        time.sleep_ms(10)

    def _gain_pulses(self):
        return {128: 1, 64: 3, 32: 2}.get(self.gain, 1)

    def _read_raw(self):
        while self.dout.value() == 1:
            pass
        value = 0
        for _ in range(24):
            self.sck.value(1)
            value = (value << 1) | self.dout.value()
            self.sck.value(0)
        for _ in range(self._gain_pulses()):
            self.sck.value(1)
            self.sck.value(0)
        if value & 0x800000:
            value -= 1 << 24
        return value

    def read_average(self, times=5):
        total = 0
        for _ in range(times):
            total += self._read_raw()
        return total // times

    def tare(self, times=15):
        self.offset = self.read_average(times)

    def read(self):
        return self.read_average() - self.offset

    def read_percent(self, raw_min=0, raw_max=100000):
        raw = self.read()
        span = raw_max - raw_min
        if span == 0:
            return 0
        pct = int((raw - raw_min) * 100 / span)
        return max(0, min(100, pct))
