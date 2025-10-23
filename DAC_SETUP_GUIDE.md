# HiFi DAC HAT Setup Guide

Complete setup guide for the Inno-Maker HiFi DAC HAT with MPD (Music Player Daemon) and MPC (Music Player Client) on Raspberry Pi.

## Table of Contents

1. [Hardware Overview](#hardware-overview)
2. [Hardware Installation](#hardware-installation)
3. [Software Setup](#software-setup)
4. [MPD Configuration](#mpd-configuration)
5. [Testing the DAC](#testing-the-dac)
6. [Troubleshooting](#troubleshooting)

---

## Hardware Overview

**Inno-Maker HiFi DAC HAT** features:
- PCM5122 DAC chip
- 32-bit 384kHz high-resolution audio
- Hardware volume mixer
- 3.5mm headphone jack
- RCA stereo output
- Compatible with Raspberry Pi 40-pin GPIO

### Specifications
- DAC Chip: Texas Instruments PCM5122
- Sample Rate: Up to 384kHz
- Bit Depth: 32-bit
- Interface: I2S
- Power: 5V via Raspberry Pi GPIO

---

## Hardware Installation

### Step 1: Physical Installation

1. **Power off** your Raspberry Pi completely
2. **Align the DAC HAT** with the 40-pin GPIO header
3. **Press down firmly** to ensure all pins are connected
4. **Secure with spacers** (optional but recommended)

### Step 2: Connect Audio Output

Choose one of the following:

**Option A: Headphones/Speakers**
- Connect to the 3.5mm headphone jack

**Option B: RCA Output**
- Connect RCA cables to the stereo output
- White = Left channel, Red = Right channel

---

## Software Setup

### Step 1: Enable I2C and I2S

1. **Edit boot configuration:**
   ```bash
   sudo nano /boot/config.txt
   ```
   
   If using Raspberry Pi OS Bookworm or newer:
   ```bash
   sudo nano /boot/firmware/config.txt
   ```

2. **Add the Allo Boss DAC overlay (for PCM5122):**
   ```
   dtoverlay=allo-boss-dac-pcm512x-audio
   ```
   
   **Note:** The Inno-Maker HiFi DAC uses the PCM5122 chip, which is compatible with the Allo Boss DAC overlay.

3. **Disable onboard audio** (comment out or remove):
   ```
   # dtparam=audio=on
   ```

4. **Save and exit** (Ctrl+X, then Y, then Enter)

5. **Reboot:**
   ```bash
   sudo reboot
   ```

### Step 2: Verify Hardware Detection

After reboot, check if the DAC is detected:

```bash
# Check sound cards
cat /proc/asound/cards
```

You should see output like:
```
 0 [sndrpihifiberry]: HifiberryDacp - snd_rpi_hifiberry_dacplus
                      snd_rpi_hifiberry_dacplus
```

**Note:** The card name may appear as `sndrpihifiberry` even when using the Allo Boss overlay, as both use compatible drivers.

Check ALSA devices:
```bash
aplay -l
```

### Step 3: Test ALSA Audio (Optional)

Test basic audio output:
```bash
speaker-test -t wav -c 2
```

Press Ctrl+C to stop.

---

## MPD Configuration

### Step 1: Install MPD and MPC

```bash
sudo apt-get update
sudo apt-get install mpd mpc
```

### Step 2: Configure MPD

1. **Edit MPD configuration:**
   ```bash
   sudo nano /etc/mpd.conf
   ```

2. **Set the music directory:**
   ```
   music_directory     "/home/pi/Music"
   ```
   
   Or use a different location:
   ```
   music_directory     "/var/lib/mpd/music"
   ```

3. **Configure audio output for the DAC:**
   
   Find the ALSA audio output section and modify it:
   ```
   audio_output {
    type            "alsa"
    name            "HiFi DAC HAT"
    device          "hw:0,0"        # Use hw:0,0 for the DAC
    mixer_type      "hardware"      # Use hardware mixer
       mixer_device    "default"
       mixer_control   "Digital"       # PCM5122 uses "Digital" control
       mixer_index     "0"
   }
   ```

4. **Optional: Enable HTTP streaming** (for web clients):
   ```
   audio_output {
       type            "httpd"
       name            "HTTP Stream"
       encoder         "lame"          # MP3 streaming
       port            "8000"
       bitrate         "320"
       format          "44100:16:2"
       always_on       "yes"
       tags            "yes"
   }
   ```

5. **Save and exit** (Ctrl+X, then Y, then Enter)

### Step 3: Set Up Music Directory

Create and populate the music directory:

```bash
# Create Music directory in your home folder
mkdir -p ~/Music

# Set proper permissions
sudo chown -R $USER:$USER ~/Music
```

**Copy your music files:**
```bash
# From USB drive
cp -r /media/usb/music/* ~/Music/

# Or from network
scp -r user@computer:/path/to/music/* ~/Music/
```

**Supported formats:**
- MP3 (.mp3)
- FLAC (.flac)
- WAV (.wav)
- OGG Vorbis (.ogg)
- AAC (.m4a, .aac)
- ALAC (.m4a)

### Step 4: Configure MPD Permissions

If using `/home/pi/Music`:
```bash
sudo usermod -a -G audio mpd
sudo systemctl restart mpd
```

If using `/var/lib/mpd/music`:
```bash
sudo mkdir -p /var/lib/mpd/music
sudo cp -r ~/Music/* /var/lib/mpd/music/
sudo chown -R mpd:audio /var/lib/mpd/music
```

### Step 5: Start MPD Service

```bash
# Start MPD
sudo systemctl start mpd

# Enable MPD on boot
sudo systemctl enable mpd

# Check status
sudo systemctl status mpd
```

### Step 6: Update MPD Database

After adding music files:
```bash
mpc update
```

Wait a few seconds for the database to update, then check:
```bash
mpc stats
```

---

## Testing the DAC

### Method 1: Automated Test Script

Run the comprehensive DAC test:

```bash
# First, run diagnostic to check setup
python app.py dac-diag

# Then run the interactive test
python app.py dac
```

The test script will:
- ✓ Check MPD/MPC installation
- ✓ Verify audio configuration
- ✓ Update music database
- ✓ Play music through the DAC
- ✓ Provide interactive controls

### Method 2: Manual MPC Commands

**Basic playback:**
```bash
# Clear playlist
mpc clear

# Add all music
mpc add /

# Play first track
mpc play 1

# Show current track
mpc current

# Show status
mpc status
```

**Playback controls:**
```bash
mpc play          # Play
mpc pause         # Pause
mpc toggle        # Toggle play/pause
mpc stop          # Stop

mpc next          # Next track
mpc prev          # Previous track

mpc volume +5     # Increase volume by 5%
mpc volume -5     # Decrease volume by 5%
mpc volume 50     # Set volume to 50%
```

**Playlist management:**
```bash
mpc playlist      # Show current playlist
mpc listall       # List all music files
mpc clear         # Clear playlist
mpc add <file>    # Add specific file
mpc shuffle       # Shuffle playlist
```

**Search and filter:**
```bash
mpc search artist "Artist Name"
mpc search album "Album Name"
mpc search title "Song Title"
```

---

## Troubleshooting

### Issue: DAC Not Detected

**Check boot configuration:**
```bash
cat /boot/config.txt | grep dtoverlay
```

Should show:
```
dtoverlay=allo-boss-dac-pcm512x-audio
```

**Check kernel messages:**
```bash
dmesg | grep snd
```

**Verify GPIO connection:**
- Power off and reseat the DAC HAT
- Ensure all 40 pins are properly connected

### Issue: No Sound Output

**Test ALSA directly:**
```bash
speaker-test -D hw:0,0 -c 2
```

**Check ALSA mixer:**
```bash
alsamixer
```
- Press F6 to select sound card
- Use arrow keys to adjust volume
- Press M to unmute if needed

**Check MPD audio output:**
```bash
mpc outputs
```

**Enable/disable outputs:**
```bash
mpc enable 1      # Enable output 1
mpc disable 2     # Disable output 2
```

### Issue: MPD Won't Start

**Check MPD logs:**
```bash
sudo journalctl -u mpd -n 50
```

**Check configuration syntax:**
```bash
mpd --no-daemon --verbose /etc/mpd.conf
```

**Common issues:**
- Music directory doesn't exist or has wrong permissions
- Audio device is wrong (try `hw:0,0`, `hw:1,0`, or `default`)
- Port already in use (check if another MPD instance is running)

### Issue: Music Files Not Found

**Update MPD database:**
```bash
mpc update
mpc rescan      # Force complete rescan
```

**Check music directory permissions:**
```bash
ls -la ~/Music
```

Should show your user as owner, or `mpd:audio` if using `/var/lib/mpd/music`

**Check MPD log for errors:**
```bash
tail -f /var/log/mpd/mpd.log
```

### Issue: Poor Audio Quality

**Check sample rate:**
```bash
mpc status
cat /proc/asound/card0/pcm0p/sub0/hw_params
```

**Force high-quality output in `/etc/mpd.conf`:**
```
audio_output {
    type            "alsa"
    name            "HiFi DAC"
    device          "hw:0,0"
    format          "44100:24:2"    # 44.1kHz, 24-bit, stereo
    auto_resample   "no"
    auto_format     "no"
}
```

### Issue: Volume Too Low/High

**Adjust ALSA mixer:**
```bash
alsamixer -c 0
```

**Adjust MPD volume:**
```bash
mpc volume 75
```

**Check hardware volume control:**
```bash
amixer -c 0 sget Digital
amixer -c 0 sset Digital 90%
```

---

## Advanced Configuration

### Set Default Audio Device

Create `~/.asoundrc`:
```bash
nano ~/.asoundrc
```

Add:
```
defaults.pcm.card 0
defaults.ctl.card 0
```

### Auto-Play on Boot

Create systemd service:
```bash
sudo nano /etc/systemd/system/mpd-autoplay.service
```

Add:
```ini
[Unit]
Description=MPD Auto-Play
After=mpd.service

[Service]
Type=oneshot
ExecStartPre=/bin/sleep 5
ExecStart=/usr/bin/mpc play

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable mpd-autoplay.service
```

### Web-Based Control

Install a web client like Rompr or myMPD:

```bash
# Install Rompr (web-based MPD client)
sudo apt-get install apache2 php php-gd php-xml php-mbstring
cd /var/www/html
sudo git clone https://github.com/fatg3erman/RompR.git rompr
```

Access at: `http://raspberrypi.local/rompr`

---

## Quick Reference

### Essential Commands

```bash
# Service management
sudo systemctl start mpd
sudo systemctl stop mpd
sudo systemctl restart mpd
sudo systemctl status mpd

# Playback
mpc play
mpc pause
mpc toggle
mpc stop

# Volume
mpc volume +10
mpc volume -10

# Navigation
mpc next
mpc prev

# Playlist
mpc add /
mpc clear
mpc shuffle

# Information
mpc current
mpc status
mpc stats

# Database
mpc update
mpc rescan
```

### Testing Scripts

```bash
# Run diagnostic
python app.py dac-diag

# Run interactive test
python app.py dac

# List all available tests
python app.py --list
```

---

## Additional Resources

- [Inno-Maker HiFi DAC HAT Manual](https://www.inno-maker.com/wp-content/uploads/2017/11/HIFI-DAC-User-Manual-V1.2.pdf)
- [MPD Documentation](https://www.musicpd.org/doc/html/)
- [MPC Manual](https://www.musicpd.org/clients/mpc/)
- [HiFiBerry Documentation](https://www.hifiberry.com/docs/)
- [ALSA Documentation](https://www.alsa-project.org/wiki/Main_Page)

---

## Support

If you encounter issues:

1. Run the diagnostic: `python app.py dac-diag`
2. Check MPD logs: `sudo journalctl -u mpd -n 50`
3. Verify hardware: `cat /proc/asound/cards`
4. Test ALSA: `speaker-test -D hw:0,0 -c 2`

For hardware-specific issues, refer to the [official manual](https://www.inno-maker.com/wp-content/uploads/2017/11/HIFI-DAC-User-Manual-V1.2.pdf).

