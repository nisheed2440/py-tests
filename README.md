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

**Note:** This includes:
- `Pillow` - Image processing for LCD
- `RPi.GPIO` - GPIO control
- `spidev` - SPI communication
- `mfrc522` - NFC/RFID reader library

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

# Run NFC/RFID reader test
sudo $(which python) app.py nfc
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

### NFC/RFID Reader Test (`python app.py nfc`)

Tests the MFRC522 NFC/RFID reader functionality using the `mfrc522-python` library:
1. Initializes the MFRC522 reader
2. Continuously scans for NFC cards/tags
3. Displays card UID (Unique Identifier) in both decimal and hex format
4. Reads and displays any text data stored on the card
5. Simple and reliable card detection with debouncing

**If cards aren't being detected, run the diagnostic first:**
```bash
sudo $(which python) app.py nfc-diag
```

Run the test directly as a module:
```bash
sudo $(which python) -m modules.nfc.nfc_test
```

**Supported Cards:**
- MIFARE Classic 1K (most common)
- MIFARE Classic 4K
- MIFARE Ultralight
- Most ISO 14443A compatible cards

### NFC Hardware Diagnostic (`python app.py nfc-diag`)

Comprehensive diagnostic tool to check MFRC522 setup:
1. Tests GPIO module and configuration
2. Verifies SPI interface is enabled and accessible
3. Checks MFRC522 library installation
4. Tests reader initialization
5. Reads and validates chip version register
6. Performs 5-second card detection test

Use this if you're having issues with card detection:
```bash
sudo $(which python) app.py nfc-diag
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
│   ├── music_player/          # Music player module
│   │   ├── __init__.py
│   │   ├── controls.py        # Button/joystick input handling
│   │   ├── player.py          # Music player logic and UI rendering
│   │   └── ui.py              # Music player main loop
│   └── nfc/                   # NFC/RFID module
│       ├── __init__.py
│       ├── diagnostic.py      # Hardware diagnostic tool
│       └── nfc_test.py        # NFC reader test suite
├── music_player_ui.py         # Standalone music player (legacy)
├── album_cover_*.png          # Sample album artwork
└── requirements.txt
```

## Hardware Configuration

### LCD Module (Waveshare 1.3inch HAT)
Default BCM pin configuration:
- **RST**: GPIO 27
- **DC**: GPIO 25
- **BL** (Backlight): GPIO 24
- **CS**: GPIO 8 (CE0)
- **SPI**: Bus 0, Device 0

### Button Controls (Waveshare 1.3inch HAT)
- **KEY1**: GPIO 21
- **KEY2**: GPIO 20
- **KEY3**: GPIO 16
- **Joystick UP**: GPIO 6
- **Joystick DOWN**: GPIO 19
- **Joystick LEFT**: GPIO 5
- **Joystick RIGHT**: GPIO 26
- **Joystick PRESS**: GPIO 13

### NFC/RFID Module (MFRC522)
Uses the `mfrc522-python` library with default configuration:
- **RST**: GPIO 25 (BCM mode, BOARD pin 22)
- **SPI**: CE0 (default SPI pins)

**Standard Wiring:**
- SDA/NSS → GPIO 8 (CE0, pin 24)
- SCK → GPIO 11 (SCLK, pin 23)
- MOSI → GPIO 10 (pin 19)
- MISO → GPIO 9 (pin 21)
- GND → Ground
- RST → GPIO 25 (BCM) / pin 22 (BOARD)
- 3.3V → 3.3V (pin 1 or 17)

**Note:** The library uses BCM GPIO 25 for RST by default, which is physical pin 22.

## Reference

Based on [Waveshare 1.3inch LCD HAT Wiki](https://www.waveshare.com/wiki/1.3inch_LCD_HAT)

