"""
LCD Driver for Waveshare 1.3inch LCD HAT
ST7789 controller, 240x240 resolution
"""

import time
import spidev as SPI
from PIL import Image

# LCD Configuration
LCD_WIDTH = 240
LCD_HEIGHT = 240

# Pin definitions (BCM)
RST_PIN = 27
DC_PIN = 25
BL_PIN = 24
CS_PIN = 8

# SPI Configuration
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED = 40000000  # 40 MHz


class LCD_1in3:
    """Driver class for Waveshare 1.3inch LCD HAT with ST7789 controller"""
    
    def __init__(self, setup_buttons=False):
        """
        Initialize the LCD driver.
        
        Args:
            setup_buttons: If True, configure GPIO for the HAT's buttons and joystick.
                          Only needed if you're using the input controls.
        """
        import RPi.GPIO as GPIO
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(RST_PIN, GPIO.OUT)
        self.GPIO.setup(DC_PIN, GPIO.OUT)
        self.GPIO.setup(BL_PIN, GPIO.OUT)
        self.GPIO.output(BL_PIN, GPIO.HIGH)
        
        # Optionally setup button inputs (for music player, etc.)
        if setup_buttons:
            from ..music_player.controls import (KEY1, KEY2, KEY3, JOY_UP, JOY_DOWN, 
                                                 JOY_LEFT, JOY_RIGHT, JOY_PRESS)
            for pin in [KEY1, KEY2, KEY3, JOY_UP, JOY_DOWN, JOY_LEFT, JOY_RIGHT, JOY_PRESS]:
                self.GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.spi = SPI.SpiDev(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_SPEED
        self.spi.mode = 0b00
        
    def reset(self):
        """Hardware reset of the LCD"""
        self.GPIO.output(RST_PIN, self.GPIO.HIGH)
        time.sleep(0.01)
        self.GPIO.output(RST_PIN, self.GPIO.LOW)
        time.sleep(0.01)
        self.GPIO.output(RST_PIN, self.GPIO.HIGH)
        time.sleep(0.01)
        
    def write_cmd(self, cmd):
        """Write a command to the LCD"""
        self.GPIO.output(DC_PIN, self.GPIO.LOW)
        self.spi.writebytes([cmd])
        
    def write_data(self, data):
        """Write data to the LCD"""
        self.GPIO.output(DC_PIN, self.GPIO.HIGH)
        self.spi.writebytes([data])
        
    def init(self):
        """Initialize the LCD with ST7789 register settings"""
        self.reset()
        
        self.write_cmd(0x36)
        self.write_data(0x70)
        
        self.write_cmd(0x3A)
        self.write_data(0x05)
        
        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)
        
        self.write_cmd(0xB7)
        self.write_data(0x35)
        
        self.write_cmd(0xBB)
        self.write_data(0x19)
        
        self.write_cmd(0xC0)
        self.write_data(0x2C)
        
        self.write_cmd(0xC2)
        self.write_data(0x01)
        
        self.write_cmd(0xC3)
        self.write_data(0x12)
        
        self.write_cmd(0xC4)
        self.write_data(0x20)
        
        self.write_cmd(0xC6)
        self.write_data(0x0F)
        
        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)
        
        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)
        
        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)
        
        self.write_cmd(0x11)
        time.sleep(0.12)
        
        self.write_cmd(0x29)
        
    def set_window(self, x_start, y_start, x_end, y_end):
        """Set the drawing window for the LCD"""
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(x_start)
        self.write_data(0x00)
        self.write_data(x_end - 1)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(y_start)
        self.write_data(0x00)
        self.write_data(y_end - 1)
        
        self.write_cmd(0x2C)
        
    def display(self, image):
        """Display a PIL Image on the LCD"""
        img = image.rotate(0)
        pix = img.load()
        self.set_window(0, 0, LCD_WIDTH, LCD_HEIGHT)
        self.GPIO.output(DC_PIN, self.GPIO.HIGH)
        
        for y in range(LCD_HEIGHT):
            line = []
            for x in range(LCD_WIDTH):
                r, g, b = pix[x, y]
                rgb = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                line.append(rgb >> 8)
                line.append(rgb & 0xFF)
            self.spi.writebytes(line)
            
    def clear(self):
        """Clear the LCD by filling it with black"""
        image = Image.new('RGB', (LCD_WIDTH, LCD_HEIGHT), (0, 0, 0))
        self.display(image)

