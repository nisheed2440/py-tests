# MPD Database Troubleshooting Guide

This guide helps resolve the common issue where MPC finds music files but the database doesn't update.

## Quick Diagnosis

Run the troubleshooting script first:
```bash
./check_mpd_music.sh
```

This will check:
- MPD configuration
- Music directory location and permissions
- Database status
- MPC statistics

## Common Issues and Solutions

### Issue 1: Music Directory Path Mismatch

**Symptoms:**
- Script finds music in `~/Music`
- But MPD is configured to use a different path (e.g., `/home/pi/Music` when your user is different)
- `mpc stats` shows 0 songs

**Solution:**
```bash
# Check MPD config
grep music_directory /etc/mpd.conf

# If it shows wrong path (e.g., /home/pi/Music but you're user "john"), edit config:
sudo nano /etc/mpd.conf

# Change music_directory to match YOUR username:
music_directory    "/home/john/Music"

# Or run the setup script which automatically detects your username:
./setup_dac.sh

# Restart MPD and update:
sudo systemctl restart mpd
mpc update
sleep 5
mpc stats
```

**Note:** The `setup_dac.sh` script now automatically detects your actual username (even if run with sudo) and configures MPD to use `/home/yourusername/Music`, not `/home/pi/Music`.

### Issue 2: Permission Problems

**Symptoms:**
- Music directory exists
- Files are present
- But MPD database is empty
- MPD logs show permission errors

**Solution:**
```bash
# Check who MPD runs as:
grep "^user" /etc/mpd.conf

# Usually it's 'mpd' user. Make files readable:
sudo chmod -R a+rX ~/Music

# Or change ownership (better for system-wide setup):
sudo chown -R mpd:audio ~/Music

# Restart and update:
sudo systemctl restart mpd
mpc update
```

**Check permissions manually:**
```bash
# As mpd user, try to read the directory:
sudo -u mpd ls ~/Music

# If you get "Permission denied", fix with:
sudo chmod -R a+rX ~/Music
```

### Issue 3: Database Not Updating After Configuration Change

**Symptoms:**
- Changed music_directory in config
- Restarted MPD
- Database still empty

**Solution:**
```bash
# Stop MPD
sudo systemctl stop mpd

# Clear old database
sudo rm /var/lib/mpd/tag_cache
sudo rm -rf /var/lib/mpd/db

# Start MPD
sudo systemctl start mpd

# Wait for MPD to initialize
sleep 3

# Update database
mpc update

# Wait for scan to complete
sleep 5

# Check results
mpc stats
```

### Issue 4: Timing Issue (Database Update Too Fast)

**Symptoms:**
- Setup script runs `mpc update`
- But checks stats immediately
- Database appears empty because scan hasn't completed

**Solution:**

The improved `setup_dac.sh` script now:
1. Waits for MPD to restart (2 seconds)
2. Triggers database update
3. Waits for scan to complete (3 seconds)
4. Checks database stats
5. Shows actual song count

If running manually:
```bash
mpc update
sleep 5  # Wait longer for large music collections
mpc stats
```

### Issue 5: Wrong Music Directory Being Scanned

**Symptoms:**
- Multiple Music directories exist
- Script finds music in one location
- MPD configured to use another location

**Solution:**

1. **Find where your music actually is:**
```bash
find ~ -name "*.mp3" -o -name "*.flac" 2>/dev/null | head -5
```

2. **Check MPD configuration:**
```bash
grep music_directory /etc/mpd.conf
```

3. **Either move music to MPD's directory:**
```bash
MUSIC_DIR=$(grep music_directory /etc/mpd.conf | cut -d'"' -f2)
mv ~/Music/* "$MUSIC_DIR/"
```

4. **Or change MPD config to match your music location:**
```bash
sudo sed -i 's|^music_directory.*|music_directory    "/home/pi/Music"|' /etc/mpd.conf
sudo systemctl restart mpd
mpc update
```

## Verification Steps

After any fix, verify with these commands:

### 1. Check MPD is running
```bash
systemctl status mpd
```

### 2. Check database stats
```bash
mpc stats
```

Should show:
```
Songs:      42
Albums:     10
Artists:    5
...
```

### 3. Try listing files
```bash
mpc listall
```

Should show your music files.

### 4. Try playing
```bash
mpc clear
mpc add /
mpc play
mpc current
```

## Detailed Diagnostic Commands

### Check Music Directory Contents
```bash
# From config
MUSIC_DIR=$(grep music_directory /etc/mpd.conf | cut -d'"' -f2)
echo "MPD Music Dir: $MUSIC_DIR"

# Count files
find "$MUSIC_DIR" -type f \( -name "*.mp3" -o -name "*.flac" -o -name "*.wav" \) | wc -l
```

### Check MPD User Permissions
```bash
# Get MPD user
MPD_USER=$(grep "^user" /etc/mpd.conf | awk '{print $2}' | tr -d '"')
echo "MPD User: $MPD_USER"

# Test read access
sudo -u "$MPD_USER" test -r "$MUSIC_DIR" && echo "Can read" || echo "Cannot read"

# List files as MPD user
sudo -u "$MPD_USER" ls -la "$MUSIC_DIR"
```

### Check MPD Logs
```bash
# Live log monitoring
sudo journalctl -u mpd -f

# Last 50 lines
sudo journalctl -u mpd -n 50

# Look for errors
sudo journalctl -u mpd -p err -n 50
```

### Check Database File
```bash
# Find database location
DB_FILE=$(grep db_file /etc/mpd.conf | cut -d'"' -f2)
echo "Database: $DB_FILE"

# Check if exists
ls -lh "$DB_FILE"

# Check last modified time
stat "$DB_FILE"

# If empty or old, force rebuild
sudo systemctl stop mpd
sudo rm "$DB_FILE"
sudo systemctl start mpd
mpc update
```

## Common Error Messages

### "error: No such directory"
```
✗ Error: No such directory
```
**Fix:** Music directory path in MPD config doesn't exist
```bash
MUSIC_DIR=$(grep music_directory /etc/mpd.conf | cut -d'"' -f2)
mkdir -p "$MUSIC_DIR"
sudo systemctl restart mpd
```

### "error: Permission denied"
```
✗ Error: Permission denied
```
**Fix:** MPD user can't read directory
```bash
sudo chmod -R a+rX ~/Music
sudo systemctl restart mpd
```

### "database: No updates found"
```
mpc update
Updating DB (#1) ...
```
But `mpc stats` shows Songs: 0

**Fix:** MPD scanned but found nothing - check directory and permissions

## Prevention Tips

1. **Use absolute paths** in MPD config, not relative paths
2. **Make files world-readable** for simplicity: `chmod -R a+rX ~/Music`
3. **Wait after updating** - give MPD time to scan
4. **Check logs** when things don't work: `sudo journalctl -u mpd -n 50`
5. **Run diagnostics** before and after changes: `python app.py dac-diag`

## Quick Fix Script

If all else fails, run this:

```bash
#!/bin/bash
# Nuclear option: complete MPD reset

# Stop MPD
sudo systemctl stop mpd

# Clear database
sudo rm -f /var/lib/mpd/tag_cache
sudo rm -rf /var/lib/mpd/db

# Set music directory
sudo sed -i 's|^music_directory.*|music_directory    "/home/pi/Music"|' /etc/mpd.conf

# Fix permissions
sudo chmod -R a+rX /home/pi/Music

# Start MPD
sudo systemctl start mpd
sleep 3

# Update database
mpc update
sleep 10

# Check results
mpc stats
mpc listall | head -10
```

## Getting Help

If you've tried everything and it still doesn't work:

1. Run full diagnostic:
   ```bash
   python app.py dac-diag > diagnostic.txt
   ```

2. Collect logs:
   ```bash
   sudo journalctl -u mpd -n 100 > mpd.log
   ```

3. Check configuration:
   ```bash
   cat /etc/mpd.conf > mpd_config.txt
   ```

4. Test manually:
   ```bash
   # Stop system MPD
   sudo systemctl stop mpd
   
   # Run MPD in foreground with verbose output
   mpd --no-daemon --verbose /etc/mpd.conf
   
   # Press Ctrl+C after a few seconds
   # Look for errors in output
   ```

## Related Files

- `setup_dac.sh` - Main setup script (now includes better database checking)
- `check_mpd_music.sh` - Quick troubleshooting script
- `modules/dac/dac_diagnostic.py` - Python diagnostic tool
- `modules/dac/dac_test.py` - Test script with better database validation
- `DAC_SETUP_GUIDE.md` - Complete setup instructions
- `MPC_QUICK_REFERENCE.md` - MPC command reference

