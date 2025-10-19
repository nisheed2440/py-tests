"""
LCD Module for Waveshare 1.3inch LCD HAT
ST7789 controller, 240x240 resolution
"""

from .lcd_driver import LCD_1in3, LCD_WIDTH, LCD_HEIGHT
from .lcd_test import run_test

__all__ = ['LCD_1in3', 'LCD_WIDTH', 'LCD_HEIGHT', 'run_test']

