# Raspberry Pi LCD Project

Modular test suite for Raspberry Pi projects including LCD display testing and music player UI for the Waveshare 1.3inch LCD HAT (240x240 ST7789 controller).

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

## Quick Start

The project uses a modular structure where you can run different tests conditionally:

```bash
# Activate virtual environment
source venv/bin/activate

# List available tests
python app.py --list

# Run LCD hardware test
sudo $(which python) app.py lcd

# Run music player
sudo $(which python) app.py music
```

**Note:** `sudo` is required for GPIO access on Raspberry Pi.

## Available Tests

### LCD Test (`python app.py lcd`)

Tests the LCD hardware functionality:
1. Initializes the LCD display
2. Displays solid colors (Red, Green, Blue, White)
3. Draws shapes (rectangle, circle) and text
4. Clears the display

You can also run the LCD test directly:
```bash
sudo $(which python) -m modules.lcd.lcd_test
```

### Music Player (`python app.py music`)

A fully functional music player interface with album art display and interactive controls.

**Controls:**
- KEY1 (GPIO 21) - Play/Pause
- Joystick LEFT - Previous track
- Joystick RIGHT - Next track
- Joystick UP - Volume up
- Joystick DOWN - Volume down
- KEY3 (GPIO 16) - Exit

Run directly as a module:
```bash
sudo $(which python) -m modules.music_player.ui
```

Or use the standalone version:
```bash
sudo $(which python) music_player_ui.py
```

## Project Structure

```
py-2/
├── app.py                      # Main entry point with test selection
├── modules/
│   ├── lcd/                   # LCD module
│   │   ├── __init__.py
│   │   ├── lcd_driver.py      # LCD hardware driver (ST7789)
│   │   └── lcd_test.py        # LCD test suite
│   └── music_player/          # Music player module
│       ├── __init__.py
│       ├── controls.py        # Button/joystick input handling
│       ├── player.py          # Music player logic and UI rendering
│       └── ui.py              # Music player main loop
├── music_player_ui.py         # Standalone music player (legacy)
├── album_cover_*.png          # Sample album artwork
└── requirements.txt
```

## Hardware Configuration

The LCD module uses the default BCM pin configuration:
- **RST**: GPIO 27
- **DC**: GPIO 25
- **BL** (Backlight): GPIO 24
- **CS**: GPIO 8 (CE0)
- **SPI**: Bus 0, Device 0

## Reference

Based on [Waveshare 1.3inch LCD HAT Wiki](https://www.waveshare.com/wiki/1.3inch_LCD_HAT)

