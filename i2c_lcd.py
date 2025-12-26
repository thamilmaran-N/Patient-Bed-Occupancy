from lcd_api import LcdApi
import utime

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = 0x08
        utime.sleep_ms(20)
        self.hal_write_init_nibble(0x03)
        utime.sleep_ms(5)
        self.hal_write_init_nibble(0x03)
        utime.sleep_ms(1)
        self.hal_write_init_nibble(0x03)
        self.hal_write_init_nibble(0x02)

        cmd = self.LCD_FUNCTION | self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)
        self.clear()
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)

        super().__init__(num_lines, num_columns)

    def hal_write_init_nibble(self, nibble):
        self.i2c.writeto(self.i2c_addr, bytes([nibble << 4 | self.backlight]))
        self.i2c.writeto(self.i2c_addr, bytes([nibble << 4 | 0x04 | self.backlight]))
        self.i2c.writeto(self.i2c_addr, bytes([nibble << 4 | self.backlight]))

    def hal_write_command(self, cmd):
        self.hal_write_byte(cmd, 0)

    def hal_write_data(self, data):
        self.hal_write_byte(data, 1)

    def hal_write_byte(self, data, mode):
        high = mode | (data & 0xF0) | self.backlight
        low = mode | ((data << 4) & 0xF0) | self.backlight
        self.i2c.writeto(self.i2c_addr, bytes([high]))
        self.i2c.writeto(self.i2c_addr, bytes([high | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([high]))
        self.i2c.writeto(self.i2c_addr, bytes([low]))
        self.i2c.writeto(self.i2c_addr, bytes([low | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([low]))
