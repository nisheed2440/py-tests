"""
Test suite for the LCD module
"""

import time
from PIL import Image, ImageDraw, ImageFont
from .lcd_driver import LCD_1in3, LCD_WIDTH, LCD_HEIGHT


def run_test():
    """
    Run comprehensive LCD tests including color fills, shapes, and text rendering.
    
    This test will:
    1. Initialize the LCD
    2. Display solid color fills (red, green, blue, white)
    3. Draw shapes (rectangle, ellipse) and text
    4. Clear the display
    """
    print("Initializing 1.3inch LCD HAT...")
    lcd = LCD_1in3()
    lcd.init()
    
    print("Running LCD test...")
    
    # Test 1: Color fills
    colors = [
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Blue", (0, 0, 255)),
        ("White", (255, 255, 255))
    ]
    
    for name, color in colors:
        print(f"Displaying {name}...")
        image = Image.new('RGB', (LCD_WIDTH, LCD_HEIGHT), color)
        lcd.display(image)
        time.sleep(1)
    
    # Test 2: Shapes and text
    print("Drawing shapes and text...")
    image = Image.new('RGB', (LCD_WIDTH, LCD_HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    draw.rectangle((20, 20, 220, 80), fill=(255, 0, 0), outline=(255, 255, 255))
    draw.ellipse((60, 100, 180, 180), fill=(0, 255, 0), outline=(255, 255, 255))
    draw.text((40, 200), "LCD Test OK!", fill=(255, 255, 255))
    
    lcd.display(image)
    print("Test complete! Display will remain on for 5 seconds.")
    time.sleep(5)
    
    # Clear display
    print("Clearing display...")
    lcd.clear()
    print("LCD test done!")


if __name__ == '__main__':
    try:
        run_test()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        raise

