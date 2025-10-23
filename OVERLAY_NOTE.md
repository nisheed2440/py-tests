# Device Tree Overlay Note

## Important: Correct Overlay for Inno-Maker HiFi DAC HAT

The **Inno-Maker HiFi DAC HAT** uses the **PCM5122** DAC chip from Texas Instruments.

### Correct Overlay

Add this overlay to your boot configuration:
```
dtoverlay=allo-boss-dac-pcm512x-audio
```

**Config file location:**
- `/boot/firmware/config.txt` (Raspberry Pi OS Bookworm 2023+)
- `/boot/config.txt` (older versions)

### Why This Overlay?

1. **PCM512x Family**: The PCM5122 is part of the PCM512x series
2. **Allo Boss Compatibility**: The Allo Boss DAC also uses PCM512x chips
3. **Optimized Driver**: This overlay provides optimized settings for the PCM512x series
4. **Better Hardware Support**: Includes proper mixer controls and volume management

### Alternative Overlays

While the following overlay may also work:
```
dtoverlay=hifiberry-dacplus
```

The `allo-boss-dac-pcm512x-audio` overlay is **recommended** because:
- It's specifically designed for PCM512x chips
- Provides better hardware volume control
- More accurate chip initialization
- Follows the manufacturer's recommendations

### Configuration Example

Complete boot configuration:

**Edit the config file:**
```bash
# For Bookworm (2023+) or newer
sudo nano /boot/firmware/config.txt

# For older OS versions
sudo nano /boot/config.txt
```

**Add these lines:**
```bash
# Disable onboard audio
#dtparam=audio=on

# Enable Inno-Maker HiFi DAC HAT (PCM5122)
dtoverlay=allo-boss-dac-pcm512x-audio
```

After editing, reboot:
```bash
sudo reboot
```

### Verification

After reboot, verify the DAC is detected:

```bash
# Check sound cards
cat /proc/asound/cards

# Check ALSA devices
aplay -l

# List available device tree overlays
dtoverlay -l

# View current overlays
vcgencmd get_config int
```

### Source

This information is based on:
- [Inno-Maker HiFi DAC HAT Manual](https://www.inno-maker.com/wp-content/uploads/2017/11/HIFI-DAC-User-Manual-V1.2.pdf)
- PCM5122 datasheet specifications
- Raspberry Pi device tree overlay documentation
- Community testing and feedback

### Need Help?

Run the diagnostic tool to check your configuration:
```bash
python app.py dac-diag
```

It will verify that the correct overlay is configured and provide guidance if issues are found.

