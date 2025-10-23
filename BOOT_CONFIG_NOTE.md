# Boot Configuration Location - Raspberry Pi OS

## Important: Config File Location Changed in Bookworm

Starting with **Raspberry Pi OS Bookworm (released 2023)**, the boot configuration file location has changed.

### New Location (Bookworm 2023+)
```
/boot/firmware/config.txt
```

### Old Location (Pre-Bookworm)
```
/boot/config.txt
```

## Why the Change?

The change aligns Raspberry Pi OS with standard Debian practices where firmware files are stored in `/boot/firmware/` rather than directly in `/boot/`.

## What This Means for DAC Setup

When configuring your HiFi DAC HAT, use the appropriate location for your OS version:

### On Raspberry Pi OS Bookworm (2023+)
```bash
sudo nano /boot/firmware/config.txt
```

### On Older Raspberry Pi OS
```bash
sudo nano /boot/config.txt
```

## How Our Scripts Handle This

All scripts and diagnostic tools automatically detect the correct location:

1. **Check new location first**: `/boot/firmware/config.txt`
2. **Fall back to old location**: `/boot/config.txt`
3. **Report both if neither found**

### Automatic Detection in Code

```python
# From dac_diagnostic.py
boot_config = '/boot/firmware/config.txt'
if not os.path.exists(boot_config):
    boot_config = '/boot/config.txt'
```

```bash
# From setup_dac.sh
BOOT_CONFIG="/boot/firmware/config.txt"
if [ ! -f "$BOOT_CONFIG" ]; then
    BOOT_CONFIG="/boot/config.txt"
fi
```

## Checking Your OS Version

To see which version of Raspberry Pi OS you're running:

```bash
cat /etc/os-release
```

Look for the `VERSION_CODENAME` field:
- `bookworm` → Use `/boot/firmware/config.txt`
- `bullseye` or older → Use `/boot/config.txt`

## Checking Which Config File Exists

```bash
# Check new location
ls -la /boot/firmware/config.txt

# Check old location
ls -la /boot/config.txt
```

## Complete DAC Configuration Example

### Step 1: Identify Your Config Location

```bash
# This command will show you which file exists
[ -f /boot/firmware/config.txt ] && echo "Found: /boot/firmware/config.txt (Bookworm+)" || \
[ -f /boot/config.txt ] && echo "Found: /boot/config.txt (older)" || \
echo "Warning: No config file found!"
```

### Step 2: Edit the Config File

**For Bookworm (2023+):**
```bash
sudo nano /boot/firmware/config.txt
```

**For older versions:**
```bash
sudo nano /boot/config.txt
```

### Step 3: Add DAC Configuration

Add these lines:
```
# Disable onboard audio
#dtparam=audio=on

# Enable Inno-Maker HiFi DAC HAT (PCM5122)
dtoverlay=allo-boss-dac-pcm512x-audio
```

### Step 4: Reboot
```bash
sudo reboot
```

## Using Our Automated Setup

The automated setup script handles both locations automatically:

```bash
./setup_dac.sh
```

It will:
1. ✅ Detect which config file exists
2. ✅ Add the correct overlay
3. ✅ Comment out onboard audio
4. ✅ Tell you which file was modified

## Verifying Configuration

After editing, verify the overlay was added:

**For Bookworm:**
```bash
grep dtoverlay /boot/firmware/config.txt
```

**For older versions:**
```bash
grep dtoverlay /boot/config.txt
```

Should show:
```
dtoverlay=allo-boss-dac-pcm512x-audio
```

## Diagnostic Tool

Run the diagnostic to check your configuration:
```bash
python app.py dac-diag
```

It will automatically:
- ✅ Detect which config file you have
- ✅ Check if the DAC overlay is configured
- ✅ Warn if the config file is not found
- ✅ Show both possible locations

## Troubleshooting

### Config file not found
If both locations are missing, your system may have a different configuration. Check:
```bash
# Show all files in /boot
ls -la /boot/

# Show all files in /boot/firmware (if it exists)
ls -la /boot/firmware/
```

### Changes not taking effect
1. Verify you edited the correct file for your OS version
2. Ensure you saved the file (Ctrl+X, then Y, then Enter in nano)
3. Reboot is required for changes to take effect
4. Check for typos in the overlay name

### Multiple config files exist
If both files exist:
- The system uses `/boot/firmware/config.txt` (new location)
- Edit the new location to ensure changes take effect
- The old location may be ignored on Bookworm

## Additional Resources

- **[DAC_SETUP_GUIDE.md](DAC_SETUP_GUIDE.md)** - Complete DAC setup instructions
- **[OVERLAY_NOTE.md](OVERLAY_NOTE.md)** - Information about the correct overlay
- **[setup_dac.sh](setup_dac.sh)** - Automated setup script
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)

## Summary

| OS Version | Config Location | Command |
|------------|----------------|---------|
| Bookworm (2023+) | `/boot/firmware/config.txt` | `sudo nano /boot/firmware/config.txt` |
| Bullseye & older | `/boot/config.txt` | `sudo nano /boot/config.txt` |

**All our scripts and tools automatically detect the correct location** - you don't need to worry about which version you have! 🎉

