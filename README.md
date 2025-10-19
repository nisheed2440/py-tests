# Waveshare 1.3inch LCD HAT Test

Simple test script for the Waveshare 1.3inch LCD HAT (240x240 ST7789 controller).

## Setup on Raspberry Pi

### 1. Enable SPI Interface
```bash
sudo raspi-config
# Navigate to: Interfacing Options -> SPI -> Yes
sudo reboot
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Run the Test

```bash
source venv/bin/activate
sudo $(which python) lcd_test.py
```

**Note:** `sudo` is required for GPIO access.

## What the Test Does

1. Initializes the LCD display
2. Displays solid colors (Red, Green, Blue, White)
3. Draws shapes (rectangle, circle) and text
4. Clears the display

## Pin Configuration

The script uses the default BCM pin configuration:
- **RST**: GPIO 27
- **DC**: GPIO 25
- **BL** (Backlight): GPIO 24
- **CS**: GPIO 8 (CE0)
- **SPI**: Bus 0, Device 0

## Music Player UI

A fully functional music player interface with album art display.

### Create Sample Album Covers
```bash
python3 create_sample_cover.py
```

This generates 4 different album cover styles:
- **Vinyl Record** - Classic vinyl disc design
- **Neon/Synthwave** - Retro 80s aesthetic
- **Gradient** - Modern gradient with music note
- **Abstract** - Geometric shapes

### Run Music Player
```bash
source venv/bin/activate
sudo $(which python) music_player_ui.py
```

**Controls:**
- KEY1 - Play/Pause
- Joystick LEFT/RIGHT - Previous/Next track
- Joystick UP/DOWN - Volume control
- KEY3 - Exit

## Reference

Based on [Waveshare 1.3inch LCD HAT Wiki](https://www.waveshare.com/wiki/1.3inch_LCD_HAT)

