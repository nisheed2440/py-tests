# User Detection Fix - Always Use Current User's Music Directory

## Issue Reported

The scripts were potentially creating or looking for a "root" music directory instead of the current user's Music folder.

## Root Cause

When using `$HOME` in bash scripts, if the script is run with `sudo`, `$HOME` expands to `/root/Music` instead of the actual user's home directory (e.g., `/home/john/Music`).

## Solution

Updated all scripts to detect the **actual user** (not root) even when run with sudo:

```bash
# Detect actual user
ACTUAL_USER="${SUDO_USER:-$USER}"
ACTUAL_HOME=$(eval echo ~$ACTUAL_USER)
MUSIC_DIR="$ACTUAL_HOME/Music"
```

This technique:
- Uses `$SUDO_USER` when script is run with sudo (gets the real user)
- Falls back to `$USER` when not using sudo
- Expands home directory correctly for that user
- Always points to `/home/yourusername/Music`, never `/root/Music`

## Files Updated

### 1. `setup_dac.sh`
**Lines 36-53:**
- Detects actual user and their home directory
- Creates Music directory with correct ownership
- Prints current user and music directory for verification
- Uses this throughout the script for MPD configuration

**Example output:**
```
[2/5] Setting up music directory...
  Current user: john
  Music directory: /home/john/Music
✓ Music directory already exists
```

### 2. `check_mpd_music.sh`
**Lines 27-32:**
- Detects actual user and home directory
- Shows this information in diagnostic output
- Uses it when checking paths and permissions

**Example output:**
```
[1] MPD Configuration
------------------------------------------------------------
Config file: /etc/mpd.conf

Current user: john
User home: /home/john

Music Directory: /home/john/Music
```

### 3. `modules/dac/dac_diagnostic.py`
**Lines 255-262:**
- Imports `pwd` module for user info
- Gets actual user from environment
- Prioritizes actual user's Music directory
- Shows user and home in diagnostic output

```python
import pwd
actual_user = os.environ.get('SUDO_USER') or os.environ.get('USER')
actual_home = pwd.getpwnam(actual_user).pw_dir if actual_user else os.path.expanduser('~')

print(f"Current user: {actual_user}")
print(f"User home: {actual_home}")
```

### 4. `modules/dac/dac_test.py`
**Lines 68-93:**
- Same user detection as diagnostic
- Prioritizes actual user's Music directory when searching
- Removes duplicate paths from search list

### 5. `mpd.conf.sample`
**Lines 7-13:**
- Added comment explaining to change "pi" to actual username
- Notes that setup script does this automatically
- Shows alternative directory locations

### 6. Documentation Updates
- `MPD_DATABASE_TROUBLESHOOTING.md` - Added note about username detection
- `MPD_FIX_SUMMARY.md` - Documented the user detection issue and fix

## Testing

To verify the fix works correctly:

### Test 1: Run without sudo
```bash
./setup_dac.sh
```
Should show:
```
Current user: yourusername
Music directory: /home/yourusername/Music
```

### Test 2: Run with sudo
```bash
sudo ./setup_dac.sh
```
Should STILL show:
```
Current user: yourusername
Music directory: /home/yourusername/Music
```
(NOT `/root/Music`)

### Test 3: Check MPD config
```bash
grep music_directory /etc/mpd.conf
```
Should show:
```
music_directory    "/home/yourusername/Music"
```

### Test 4: Run diagnostic
```bash
./check_mpd_music.sh
```
Should show your actual username and home directory.

## Benefits

1. **No more root directory issues** - Scripts always use the actual user's directory
2. **Works with sudo** - Correctly detects user even when run as root
3. **Better visibility** - Scripts now print the user and directory being used
4. **Consistent** - All scripts (bash and Python) use the same detection method
5. **Automatic** - No manual editing of usernames needed

## Examples

### Before (Potential Issues)
```bash
# If run with sudo
$ sudo ./setup_dac.sh
MUSIC_DIR="/root/Music"  # WRONG! Using root's home

# MPD config would be set to
music_directory "/root/Music"  # MPD can't read root's home
```

### After (Fixed)
```bash
# Even if run with sudo
$ sudo ./setup_dac.sh
Current user: john
Music directory: /home/john/Music  # CORRECT! Using actual user

# MPD config is set to
music_directory "/home/john/Music"  # MPD can read this
```

## When This Matters

This fix is important when:
- Running `setup_dac.sh` with sudo (which some steps require)
- Multiple users on the same Raspberry Pi
- Username is not "pi" (common with custom installations)
- Sharing configurations between different systems

## Summary

✅ Scripts now always detect and use the current user's Music directory
✅ Works correctly even when run with sudo
✅ No hardcoded "pi" username assumptions
✅ All scripts (bash and Python) updated consistently
✅ Better diagnostic output showing exactly what's being used

The Music directory is now always `/home/YOURUSERNAME/Music`, never `/root/Music` or hardcoded `/home/pi/Music`.

