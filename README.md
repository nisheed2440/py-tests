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

Tests the MFRC522 NFC/RFID reader functionality:
1. Initializes the MFRC522 reader
2. Continuously scans for NFC cards/tags
3. Displays card UID (Unique Identifier)
4. Shows card type and size information
5. Attempts to read and authenticate MIFARE Classic cards

Run directly as a module:
```bash
sudo $(which python) -m modules.nfc.nfc_test
```

**Supported Cards:**
- MIFARE Classic 1K/4K
- MIFARE Ultralight
- NTAG series
- Most ISO 14443A compatible cards

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
│       ├── mfrc522.py         # MFRC522 driver
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
Default configuration:
- **SPI Bus**: 0
- **SPI Device**: 0
- **RST**: GPIO 22 (BOARD pin mode)
- **SPI Speed**: 1 MHz

**Wiring:**
- SDA (NSS) → GPIO 8 (CE0)
- SCK → GPIO 11 (SCLK)
- MOSI → GPIO 10
- MISO → GPIO 9
- GND → Ground
- RST → GPIO 22
- 3.3V → 3.3V

## Reference

Based on [Waveshare 1.3inch LCD HAT Wiki](https://www.waveshare.com/wiki/1.3inch_LCD_HAT)

