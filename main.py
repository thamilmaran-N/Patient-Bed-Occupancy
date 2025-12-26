# main.py – ESP32 Bed Unit (Main Code)
# Integration of IoT with Legacy Systems

from machine import Pin, I2C
import time
from hx711 import HX711
from mpu6050 import MPU6050
from i2c_lcd import I2cLcd
from ble_scanner import BLEScanner

# ---------------- I2C (LCD + MPU6050) ----------------
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
mpu = MPU6050(i2c)

# ---------------- HX711 Load Cell -------------------
hx = HX711(d_out=18, sck=19)
hx.tare()

# Calibration values (set after calibration)
RAW_MIN = 0        # raw value at 0 kg
RAW_MAX = 100000   # raw value at 5 kg

# ---------------- Switch -----------------------------
switch = Pin(5, Pin.IN, Pin.PULL_DOWN)

# ---------------- LEDs -------------------------------
led_green = Pin(15, Pin.OUT)
led_yellow = Pin(2, Pin.OUT)
led_red = Pin(4, Pin.OUT)

def leds_off():
    led_green.off()
    led_yellow.off()
    led_red.off()

# ---------------- BLE Scanner ------------------------
TARGET_MAC = "01:23:45:67:94:C7"   # HM-10 MAC address
ble = BLEScanner(target_mac=TARGET_MAC)

RSSI_STRONG = -65
RSSI_WEAK = -80

WEIGHT_PRESENT_PCT = 5
OCCUPIED_PCT = 20

blink_state = False

# ---------------- Helper Functions -------------------
def classify_status(weight_pct, rssi, moving):
    has_weight = weight_pct > WEIGHT_PRESENT_PCT
    above_occupied = weight_pct > OCCUPIED_PCT

    if rssi is None:
        strong = False
        weak = False
        very_weak = True
    else:
        strong = rssi >= RSSI_STRONG
        weak = RSSI_WEAK <= rssi < RSSI_STRONG
        very_weak = rssi < RSSI_WEAK

    if above_occupied and strong and not moving:
        return "OCCUPIED"

    if (has_weight and weak) or moving or (strong and not has_weight):
        return "ABNORMAL"

    if (not has_weight) and very_weak and moving:
        return "NOT_OCCUPIED"

    return "NOT_OCCUPIED"

def update_lcd(status, moving):
    lcd.move_to(0, 0)
    if status == "OCCUPIED":
        lcd.putstr("Bed: OCCUPIED  ")
    elif status == "ABNORMAL":
        lcd.putstr("Bed: ABNORMAL  ")
    else:
        lcd.putstr("Bed: NOT OCC   ")

    lcd.move_to(0, 1)
    if moving:
        lcd.putstr("Motion: DETECT ")
    else:
        lcd.putstr("Motion: NONE   ")

def update_leds_blink(status, blink_on):
    leds_off()
    if not blink_on:
        return
    if status == "OCCUPIED":
        led_green.on()
    elif status == "ABNORMAL":
        led_yellow.on()
    else:
        led_red.on()

# ---------------- Main Loop --------------------------
lcd.clear()
lcd.putstr("System Ready")
time.sleep(1)
lcd.clear()

while True:
    if switch.value() == 0:
        leds_off()
        lcd.move_to(0, 0)
        lcd.putstr("Switch OFF     ")
        lcd.move_to(0, 1)
        lcd.putstr("System Idle    ")
        time.sleep(0.5)
        continue

    rssi = ble.scan_once(1000)
    weight_pct = hx.read_percent(RAW_MIN, RAW_MAX)
    moving = mpu.is_moving()

    status = classify_status(weight_pct, rssi, moving)

    blink_state = not blink_state
    update_leds_blink(status, blink_state)
    update_lcd(status, moving)

    print("Status:", status,
          "| RSSI:", rssi,
          "| Weight%:", weight_pct,
          "| Moving:", moving)

    time.sleep(0.5)
