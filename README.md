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

# Run DAC HAT test
python app.py dac
```

**Note:** `sudo` is required for GPIO access on Raspberry Pi. DAC testing doesn't require sudo unless MPD is configured to require it.

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

### DAC HAT Test (`python app.py dac`)

Tests the Inno-Maker HiFi DAC HAT using MPD (Music Player Daemon) and MPC (Music Player Client):
1. Checks MPD/MPC installation and configuration
2. Verifies music directory setup
3. Updates MPD database
4. Tests audio playback through the DAC
5. Provides interactive playback controls

**If the DAC isn't working, run the diagnostic first:**
```bash
python app.py dac-diag
```

Run the test directly as a module:
```bash
python -m modules.dac.dac_test
```

**Interactive Controls:**
- `p` - Play/Pause
- `n` - Next track
- `b` - Previous track
- `+` - Volume up
- `-` - Volume down
- `s` - Show status
- `l` - List playlist
- `q` - Quit

**Setup Required:**
Before running the DAC test, you need to:
1. Install the DAC HAT hardware
2. Configure the device tree overlay
3. Install MPD and MPC
4. Set up your music directory

**Quick Setup (on Raspberry Pi):**
```bash
# Run the automated setup script
./setup_dac.sh
```

**Additional Resources:**
- **[DAC_TESTING_SUMMARY.md](DAC_TESTING_SUMMARY.md)** - Quick start guide ⭐ Start here!
- **[DAC_SETUP_GUIDE.md](DAC_SETUP_GUIDE.md)** - Complete setup instructions
- **[MPC_QUICK_REFERENCE.md](MPC_QUICK_REFERENCE.md)** - MPC command reference
- **[mpd.conf.sample](mpd.conf.sample)** - Sample MPD configuration file
- **[setup_dac.sh](setup_dac.sh)** - Automated setup script

### DAC Hardware Diagnostic (`python app.py dac-diag`)

Comprehensive diagnostic tool to check DAC HAT setup:
1. Tests hardware detection (I2C/sound cards)
2. Verifies MPD installation and service status
3. Checks MPD configuration
4. Validates MPC installation
5. Checks music directory and files
6. Reviews boot configuration for DAC overlay

Use this if you're having issues with the DAC:
```bash
python app.py dac-diag
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
│   ├── nfc/                   # NFC/RFID module
│   │   ├── __init__.py
│   │   ├── diagnostic.py      # Hardware diagnostic tool
│   │   └── nfc_test.py        # NFC reader test suite
│   └── dac/                   # DAC HAT module
│       ├── __init__.py
│       ├── dac_test.py        # DAC test suite with MPD/MPC
│       └── dac_diagnostic.py  # DAC hardware diagnostic
├── music_player_ui.py         # Standalone music player (legacy)
├── album_cover_*.png          # Sample album artwork
├── DAC_TESTING_SUMMARY.md     # DAC quick start guide
├── DAC_SETUP_GUIDE.md         # Complete DAC HAT setup guide
├── MPC_QUICK_REFERENCE.md     # MPC command reference
├── mpd.conf.sample            # Sample MPD configuration
├── setup_dac.sh               # Automated DAC setup script
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

### HiFi DAC HAT (Inno-Maker)
Uses I2S interface for high-quality audio:
- **DAC Chip**: PCM5122
- **Interface**: I2S (via GPIO)
- **Sample Rate**: Up to 384kHz
- **Bit Depth**: 32-bit
- **Outputs**: 3.5mm headphone jack, RCA stereo

**Configuration:**
Requires device tree overlay in boot config:
```
dtoverlay=allo-boss-dac-pcm512x-audio
```

**Config file location:**
- `/boot/firmware/config.txt` (Raspberry Pi OS Bookworm 2023+)
- `/boot/config.txt` (older versions)

Note: Uses Allo Boss DAC overlay as the HiFi DAC HAT uses the PCM5122 chip.

**Software Requirements:**
- MPD (Music Player Daemon)
- MPC (Music Player Client)

See **[DAC_SETUP_GUIDE.md](DAC_SETUP_GUIDE.md)** for complete setup instructions.

## Reference

- [Waveshare 1.3inch LCD HAT Wiki](https://www.waveshare.com/wiki/1.3inch_LCD_HAT)
- [Inno-Maker HiFi DAC HAT Manual](https://www.inno-maker.com/wp-content/uploads/2017/11/HIFI-DAC-User-Manual-V1.2.pdf)
- [MPD Documentation](https://www.musicpd.org/doc/html/)
- [MPC Documentation](https://www.musicpd.org/clients/mpc/)

