# MPD Database Fix Summary

## Problem

The setup script (`setup_dac.sh`) was finding music files in the Music directory, but when it ran `mpc update`, the MPD database wasn't getting populated with songs. Running `mpc stats` would show 0 songs.

## Root Causes

The issue could be caused by several factors:

1. **Timing Issue**: The script was running `mpc update` immediately after restarting MPD, not giving enough time for:
   - MPD service to fully initialize
   - Database update to complete
   - File system scan to finish

2. **Path Mismatch**: The script might find music in `~/Music`, but MPD could be configured to use a different path like `/var/lib/mpd/music` or `/home/pi/Music` (hardcoded) when the actual username is different

3. **User Detection Issue**: If run with sudo, `$HOME` might expand to `/root` instead of the actual user's home directory

4. **Permission Issue**: The MPD user (usually `mpd`) may not have permission to read the music directory

5. **No Verification**: The original script didn't verify that the database was actually populated after running `mpc update`

## Solutions Implemented

### 1. Improved `setup_dac.sh`

**Changes to user detection (lines 36-53):**

Now properly detects the actual user, even when run with sudo:

```bash
# OLD: Used $HOME which could be /root if run with sudo
MUSIC_DIR="$HOME/Music"

# NEW: Detects actual user and their home directory
ACTUAL_USER="${SUDO_USER:-$USER}"
ACTUAL_HOME=$(eval echo ~$ACTUAL_USER)
MUSIC_DIR="$ACTUAL_HOME/Music"

echo "  Current user: $ACTUAL_USER"
echo "  Music directory: $MUSIC_DIR"

# Creates directory with correct ownership
if [ -n "$SUDO_USER" ]; then
    chown "$SUDO_USER:$SUDO_USER" "$MUSIC_DIR"
fi
```

This ensures that:
- Even if you run `sudo ./setup_dac.sh`, it uses YOUR music directory, not root's
- The directory is owned by you, not root
- MPD config points to the correct user's Music folder

**Changes to database update section (lines 129-163):**

```bash
# OLD: Simple update with minimal wait
mpc update &> /dev/null || true
sleep 2
echo "✓ Database updated"

# NEW: Comprehensive update with verification
# Wait for MPD to fully restart before updating
sleep 2

# Run update and wait for completion
mpc update &> /dev/null || true

# Wait for update to process
echo "  Waiting for database scan to complete..."
sleep 3

# Check database stats and verify
DB_STATS=$(mpc stats 2>/dev/null || echo "")
if echo "$DB_STATS" | grep -q "Songs:"; then
    SONG_COUNT=$(echo "$DB_STATS" | grep "Songs:" | awk '{print $2}')
    if [ "$SONG_COUNT" -gt 0 ]; then
        echo "✓ Database updated successfully"
        echo "  Found $SONG_COUNT song(s) in database"
    else
        echo "⚠ Database updated but no songs found"
        echo "  Music directory may be empty or permissions issue"
    fi
fi
```

**Changes to MPD configuration section (lines 110-123):**

Added permission checking to detect if MPD user can access the music directory:

```bash
# Check permissions on music directory
if [ -d "$MUSIC_DIR" ]; then
    MPD_USER=$(grep "^user" "$MPD_CONF" | awk '{print $2}' | tr -d '"')
    if [ -n "$MPD_USER" ] && [ "$MPD_USER" != "$(whoami)" ]; then
        echo "  Note: MPD runs as user '$MPD_USER'"
        echo "  Checking if MPD user can access music directory..."
        if sudo -u "$MPD_USER" test -r "$MUSIC_DIR" 2>/dev/null; then
            echo "  ✓ MPD user can read music directory"
        else
            echo "  ⚠ MPD user may not have permission to read $MUSIC_DIR"
            echo "  Fix with: sudo chmod -R a+rX $MUSIC_DIR"
        fi
    fi
fi
```

### 2. Enhanced `modules/dac/dac_test.py`

**Changes to `update_mpd_database()` method (lines 111-179):**

```python
# OLD: Simple update
subprocess.run(['mpc', 'update'], capture_output=True, timeout=10)
print("✓ Database update initiated")
time.sleep(3)

# NEW: Check current status first, then update if needed
# First check current database stats
result = subprocess.run(['mpc', 'stats'], ...)

# Only update if database is empty
if songs_match and 'Songs: 0' not in songs_match:
    print("✓ Database already contains music")
    return True

# Update and verify
subprocess.run(['mpc', 'update'], ...)
time.sleep(4)  # Longer wait

# Check stats again and report results
result = subprocess.run(['mpc', 'stats'], ...)
if song_count > 0:
    print("✓ Database updated successfully")
else:
    print("⚠ Database updated but no songs found")
    print("  This may indicate:")
    print("    - Music directory is empty")
    print("    - MPD doesn't have permission to read music directory")
    print("    - Music directory path is incorrect in MPD config")
```

### 3. Enhanced `modules/dac/dac_diagnostic.py`

**Changes to `check_music_directory()` method (lines 251-343):**

Now includes:
- Detection of MPD's configured music directory from config file
- Comparison between where music is found vs. where MPD expects it
- Direct check of MPD database stats using `mpc stats`
- Warning if music directory mismatch is detected

### 4. New Tools

#### `check_mpd_music.sh` - Quick Diagnostic Script

A comprehensive bash script that checks:
1. MPD configuration file location and settings
2. Music directory existence and contents
3. Permission issues (whether MPD user can read directory)
4. Database file status
5. MPC statistics
6. MPD service status
7. Provides specific recommendations based on findings

**Usage:**
```bash
./check_mpd_music.sh
```

#### `MPD_DATABASE_TROUBLESHOOTING.md` - Complete Guide

A comprehensive troubleshooting guide covering:
- Quick diagnosis steps
- 5 common issues with solutions
- Verification steps
- Detailed diagnostic commands
- Common error messages and fixes
- Prevention tips
- Quick fix script for nuclear option

### 5. Documentation Updates

#### Updated `README.md`

Added new troubleshooting section with:
- Quick reference to diagnostic script
- Common fixes for the 3 most frequent issues
- Link to comprehensive troubleshooting guide

## How to Use

### If You Haven't Run Setup Yet

Just run the improved setup script:
```bash
./setup_dac.sh
```

It will now:
- Check permissions properly
- Wait for database to update
- Verify the database has songs
- Report actual song count

### If You're Experiencing Issues

1. **Quick diagnostic:**
   ```bash
   ./check_mpd_music.sh
   ```

2. **Follow recommendations** from the diagnostic output

3. **For detailed help:**
   ```bash
   cat MPD_DATABASE_TROUBLESHOOTING.md
   ```

4. **Run Python diagnostic:**
   ```bash
   python app.py dac-diag
   ```

## Testing the Fix

To verify the fix works:

```bash
# 1. Run setup
./setup_dac.sh

# 2. Check output for song count
# Should show: "Found X song(s) in database"

# 3. Verify manually
mpc stats

# Should show:
# Songs:      42
# Albums:     10
# Artists:    5
# ...

# 4. Try playing
mpc clear
mpc add /
mpc play
mpc current
```

## Key Improvements

1. **Better Timing**: Longer waits and verification loops
2. **Permission Checking**: Detects and reports permission issues
3. **Path Verification**: Compares where music is vs. where MPD looks
4. **Status Reporting**: Shows actual song count, not just "done"
5. **Error Detection**: Identifies common issues and provides fixes
6. **Comprehensive Tools**: Both shell and Python diagnostics
7. **Better Documentation**: Step-by-step troubleshooting guide

## Files Modified

- `setup_dac.sh` - Enhanced database update and permission checking
- `modules/dac/dac_test.py` - Better database verification
- `modules/dac/dac_diagnostic.py` - Added database checking
- `README.md` - Added troubleshooting section

## Files Created

- `check_mpd_music.sh` - Quick diagnostic script (executable)
- `MPD_DATABASE_TROUBLESHOOTING.md` - Comprehensive guide
- `MPD_FIX_SUMMARY.md` - This file

## Next Steps

1. Test the improved setup script on your Raspberry Pi
2. If you still see issues, run `./check_mpd_music.sh`
3. Follow the specific recommendations provided
4. Check the troubleshooting guide for your specific error

## Prevention

Going forward, the improved scripts will:
- Detect problems earlier
- Provide clearer error messages
- Suggest specific fixes
- Verify changes worked

This should eliminate the "music found but database empty" issue.

