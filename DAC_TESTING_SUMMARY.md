# DAC HAT Testing - Quick Start Summary

This document provides a quick overview of testing your Inno-Maker HiFi DAC HAT with the automated test scripts.

## What's Been Created

The following files have been added to help you test and configure your DAC HAT:

1. **`modules/dac/dac_test.py`** - Interactive test script for the DAC
2. **`modules/dac/dac_diagnostic.py`** - Diagnostic tool to check your setup
3. **`DAC_SETUP_GUIDE.md`** - Complete step-by-step setup guide
4. **`MPC_QUICK_REFERENCE.md`** - Quick reference for MPC commands
5. **`mpd.conf.sample`** - Sample MPD configuration file

## Quick Start Guide

### Step 1: Hardware Setup

1. Power off your Raspberry Pi
2. Install the HiFi DAC HAT on the 40-pin GPIO header
3. Connect your headphones or speakers to the 3.5mm jack or RCA outputs
4. Power on your Raspberry Pi

### Step 2: Software Configuration

Edit the boot configuration:

**For Raspberry Pi OS Bookworm (2023+) or newer:**
```bash
sudo nano /boot/firmware/config.txt
```

**For older Raspberry Pi OS versions:**
```bash
sudo nano /boot/config.txt
```

Add this line:
```
dtoverlay=allo-boss-dac-pcm512x-audio
```

**Note:** The Inno-Maker HiFi DAC uses the PCM5122 chip, which is compatible with the Allo Boss DAC overlay.

Comment out (or remove):
```
# dtparam=audio=on
```

Save and reboot:
```bash
sudo reboot
```

### Step 3: Install MPD and MPC

```bash
sudo apt-get update
sudo apt-get install mpd mpc
```

### Step 4: Set Up Music Directory

```bash
# Create Music directory
mkdir -p ~/Music

# Copy your music files to ~/Music
# Example: cp -r /media/usb/music/* ~/Music/
```

Supported formats: MP3, FLAC, WAV, OGG, AAC, M4A

### Step 5: Configure MPD

You can use the provided sample configuration:

```bash
# Backup original config
sudo cp /etc/mpd.conf /etc/mpd.conf.backup

# Copy and edit the sample config
sudo cp mpd.conf.sample /etc/mpd.conf
sudo nano /etc/mpd.conf
```

Key settings to verify:
- `music_directory` points to your music folder (e.g., `/home/pi/Music`)
- Audio output device is set to `hw:0,0`
- Mixer control is set to `Digital`

Restart MPD:
```bash
sudo systemctl restart mpd
sudo systemctl enable mpd
```

### Step 6: Run the Diagnostic

Check if everything is set up correctly:

```bash
cd /Users/nisheed_jagadish/Projects/py-2
python app.py dac-diag
```

The diagnostic will check:
- ✓ Hardware detection (sound cards, I2C)
- ✓ MPD installation and service status
- ✓ MPC installation
- ✓ MPD configuration
- ✓ Music directory and files
- ✓ Boot configuration

Fix any issues reported before proceeding.

### Step 7: Run the Interactive Test

Start the DAC test:

```bash
python app.py dac
```

The test will:
1. Check MPD/MPC installation ✓
2. Check MPD status ✓
3. Verify music directory ✓
4. Update MPD database ✓
5. Start playing music ✓
6. Launch interactive controls

### Step 8: Use Interactive Controls

Once the test starts playing music, you'll have these controls:

```
Commands:
  p  - Play/Pause
  n  - Next track
  b  - Previous track
  +  - Volume up
  -  - Volume down
  s  - Show status
  l  - List playlist
  q  - Quit
```

## Manual Testing with MPC

If you prefer manual control, use these commands:

```bash
# Update database and add all music
mpc update
mpc clear
mpc add /
mpc play

# Playback controls
mpc toggle      # Play/Pause
mpc next        # Next track
mpc prev        # Previous track
mpc volume 75   # Set volume to 75%

# View status
mpc current     # Show current track
mpc status      # Show playback status
mpc playlist    # Show playlist
```

See **[MPC_QUICK_REFERENCE.md](MPC_QUICK_REFERENCE.md)** for complete command reference.

## Troubleshooting

### Problem: DAC not detected

**Check sound cards:**
```bash
cat /proc/asound/cards
```

Should show sound card for the DAC (may show as `sndrpihifiberry` or similar).

**Solution:**
- Verify `dtoverlay=allo-boss-dac-pcm512x-audio` is in boot config
- Location: `/boot/firmware/config.txt` (Bookworm) or `/boot/config.txt` (older)
- Ensure onboard audio is disabled: `# dtparam=audio=on`
- Reboot after changes
- Check GPIO connection is secure

### Problem: No sound output

**Test ALSA directly:**
```bash
speaker-test -D hw:0,0 -c 2
```

**Check volume:**
```bash
alsamixer -c 0
```

**Solution:**
- Press M to unmute if needed
- Use arrow keys to increase volume
- Try different audio output device in MPD config (`hw:0,0`, `hw:1,0`, or `default`)

### Problem: MPD won't start

**Check logs:**
```bash
sudo journalctl -u mpd -n 50
```

**Common issues:**
- Music directory doesn't exist or has wrong permissions
- Port 6600 already in use
- Invalid configuration syntax

**Solution:**
```bash
# Fix permissions
sudo chown -R mpd:audio /var/lib/mpd
sudo chown -R mpd:audio ~/Music

# Or if using user MPD:
sudo chown -R $USER:$USER ~/.config/mpd
sudo chown -R $USER:$USER ~/Music
```

### Problem: Music files not found

**Update database:**
```bash
mpc update
mpc rescan      # Force complete rescan
```

**Check permissions:**
```bash
ls -la ~/Music
```

**Solution:**
- Ensure music files are in the correct directory
- Verify file permissions are readable
- Check supported formats: .mp3, .flac, .wav, .ogg, .m4a

## Testing Checklist

Use this checklist to verify your setup:

- [ ] DAC HAT physically installed on GPIO pins
- [ ] `dtoverlay=allo-boss-dac-pcm512x-audio` added to `/boot/config.txt`
- [ ] Onboard audio disabled in `/boot/config.txt`
- [ ] Raspberry Pi rebooted after config changes
- [ ] DAC appears in `cat /proc/asound/cards`
- [ ] MPD installed: `which mpd`
- [ ] MPC installed: `which mpc`
- [ ] Music files copied to `~/Music` (or configured directory)
- [ ] MPD configuration updated (`/etc/mpd.conf`)
- [ ] MPD service running: `systemctl status mpd`
- [ ] Database updated: `mpc update`
- [ ] Diagnostic passes: `python app.py dac-diag`
- [ ] Test plays music: `python app.py dac`
- [ ] Audio output working through DAC

## Additional Features

### Web Interface

You can install web-based MPD clients for remote control:

- **Rompr**: Full-featured web interface
- **myMPD**: Lightweight modern web UI
- **ympd**: Minimalist web interface

### Mobile Apps

Control MPD from your phone:

- **M.A.L.P.** (Android)
- **MPod** (iOS)
- **MPoD** (iOS)

### Network Streaming

Enable HTTP streaming in MPD config to stream music to other devices on your network.

## Performance Tips

1. **Reduce Stuttering**: Increase `audio_buffer_size` in MPD config
2. **Better Quality**: Use FLAC or high-bitrate MP3 files
3. **Lower CPU**: Reduce resampling in MPD config
4. **Faster Database**: Use SSD or fast SD card for music storage

## File Organization

For best results, organize your music like this:

```
~/Music/
├── Artist 1/
│   ├── Album 1/
│   │   ├── 01 - Track 1.mp3
│   │   ├── 02 - Track 2.mp3
│   │   └── cover.jpg
│   └── Album 2/
│       └── ...
├── Artist 2/
│   └── ...
└── Various Artists/
    └── ...
```

MPD will automatically scan and organize by artist, album, and genre.

## Getting More Help

If you're still having issues:

1. **Run the diagnostic**: `python app.py dac-diag`
2. **Check MPD logs**: `sudo journalctl -u mpd -n 50`
3. **Verify hardware**: `aplay -l`
4. **Test ALSA**: `speaker-test -D hw:0,0 -c 2`

## Reference Documentation

- **[DAC_SETUP_GUIDE.md](DAC_SETUP_GUIDE.md)** - Complete setup guide with detailed troubleshooting
- **[MPC_QUICK_REFERENCE.md](MPC_QUICK_REFERENCE.md)** - All MPC commands with examples
- **[mpd.conf.sample](mpd.conf.sample)** - Fully commented MPD configuration
- **[Official DAC Manual](https://www.inno-maker.com/wp-content/uploads/2017/11/HIFI-DAC-User-Manual-V1.2.pdf)** - Hardware specifications

## Next Steps

Once your DAC is working:

1. **Build your music library** - Add more music to your collection
2. **Create playlists** - Organize music with `mpc save "playlist name"`
3. **Explore web clients** - Control MPD from a browser
4. **Set up remote access** - Access MPD from other devices on your network
5. **Add automation** - Create scripts to play music at specific times

Enjoy your high-quality audio! 🎵

