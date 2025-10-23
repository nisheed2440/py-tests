# DAC HAT Module

Testing module for the Inno-Maker HiFi DAC HAT using MPD (Music Player Daemon) and MPC (Music Player Client).

## Files

- **`__init__.py`** - Module initialization
- **`dac_test.py`** - Interactive DAC test with MPD/MPC
- **`dac_diagnostic.py`** - Comprehensive hardware and software diagnostic

## Usage

### Run from main app

```bash
# Interactive test
python app.py dac

# Diagnostic
python app.py dac-diag
```

### Run directly

```bash
# Interactive test
python -m modules.dac.dac_test

# Diagnostic
python -m modules.dac.dac_diagnostic
```

## Features

### DAC Test (`dac_test.py`)

- Checks MPD/MPC installation
- Verifies MPD service status
- Checks music directory for files
- Updates MPD database
- Plays music through the DAC
- Provides interactive playback controls

**Interactive Controls:**
- `p` - Play/Pause
- `n` - Next track
- `b` - Previous track
- `+` - Volume up
- `-` - Volume down
- `s` - Show status
- `l` - List playlist
- `q` - Quit

### DAC Diagnostic (`dac_diagnostic.py`)

Comprehensive checks:
1. **Hardware Detection** - I2C devices and sound cards
2. **Sound Card Detection** - Verifies DAC in ALSA
3. **ALSA Devices** - Lists available audio devices
4. **MPD Installation** - Checks MPD binary and version
5. **MPD Service** - Verifies service status
6. **MPD Configuration** - Validates config file
7. **MPC Installation** - Checks MPC binary
8. **Music Directory** - Verifies music files exist
9. **Boot Configuration** - Checks device tree overlay

## Requirements

### Hardware
- Inno-Maker HiFi DAC HAT
- Raspberry Pi (any model with 40-pin GPIO)
- Speakers or headphones

### Software
- MPD (Music Player Daemon)
- MPC (Music Player Client)
- ALSA utilities (optional)

### Installation

```bash
sudo apt-get update
sudo apt-get install mpd mpc
```

## Configuration

The DAC HAT requires the Allo Boss DAC device tree overlay (for PCM512x chips).

Edit `/boot/config.txt` or `/boot/firmware/config.txt`:
```
dtoverlay=allo-boss-dac-pcm512x-audio
# dtparam=audio=on  # Comment this out
```

**Note:** The Inno-Maker HiFi DAC uses the PCM5122 chip, compatible with the Allo Boss overlay.

Reboot after changes:
```bash
sudo reboot
```

## Quick Test

1. Install MPD and MPC
2. Add music to `~/Music`
3. Run diagnostic: `python app.py dac-diag`
4. Run test: `python app.py dac`

## Troubleshooting

### DAC not detected
- Check GPIO connection
- Verify boot config has `dtoverlay=allo-boss-dac-pcm512x-audio`
- Run: `cat /proc/asound/cards`

### No sound
- Test ALSA: `speaker-test -D hw:0,0 -c 2`
- Check volume: `alsamixer -c 0`
- Try different device in MPD config

### MPD won't start
- Check logs: `sudo journalctl -u mpd -n 50`
- Verify music directory exists
- Check permissions

## Documentation

See project root for complete documentation:
- **DAC_SETUP_GUIDE.md** - Complete setup instructions
- **MPC_QUICK_REFERENCE.md** - MPC command reference
- **mpd.conf.sample** - Sample configuration
- **DAC_TESTING_SUMMARY.md** - Quick start guide

## Reference

- [Inno-Maker HiFi DAC HAT Manual](https://www.inno-maker.com/wp-content/uploads/2017/11/HIFI-DAC-User-Manual-V1.2.pdf)
- [MPD Documentation](https://www.musicpd.org/doc/html/)
- [MPC Manual](https://www.musicpd.org/clients/mpc/)

