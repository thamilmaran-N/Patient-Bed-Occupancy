import bluetooth
from micropython import const
import time

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)

class BLEScanner:
    def __init__(self, target_mac=None):
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.target_mac = target_mac
        self.last_rssi = None
        self.device_found = False
        self.scan_done = False
        self.ble.irq(self._irq)

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            mac = ":".join("{:02X}".format(b) for b in addr)
            if self.target_mac and mac == self.target_mac:
                self.last_rssi = rssi
                self.device_found = True
        elif event == _IRQ_SCAN_DONE:
            self.scan_done = True

    def scan_once(self, duration_ms=2000):
        self.last_rssi = None
        self.device_found = False
        self.scan_done = False
        self.ble.gap_scan(duration_ms, 30000, 30000)
        start = time.ticks_ms()
        while not self.scan_done and time.ticks_diff(time.ticks_ms(), start) < duration_ms + 500:
            time.sleep_ms(10)
        if self.device_found:
            return self.last_rssi
        return None
