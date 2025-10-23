#!/bin/bash
# Quick troubleshooting script to check MPD music directory configuration
# This helps diagnose why MPC finds music files but the database isn't updated

echo "==========================================================="
echo "MPD Music Directory Troubleshooting"
echo "==========================================================="
echo ""

# Get MPD config location
MPD_CONF="/etc/mpd.conf"
if [ ! -f "$MPD_CONF" ]; then
    MPD_CONF="$HOME/.config/mpd/mpd.conf"
fi

if [ ! -f "$MPD_CONF" ]; then
    echo "✗ Could not find MPD config file"
    echo "  Checked: /etc/mpd.conf and ~/.config/mpd/mpd.conf"
    exit 1
fi

echo "[1] MPD Configuration"
echo "------------------------------------------------------------"
echo "Config file: $MPD_CONF"
echo ""

# Extract key settings
MUSIC_DIR=$(grep "^music_directory" "$MPD_CONF" | sed 's/music_directory[[:space:]]*"\(.*\)"/\1/' | sed "s|~|$HOME|")
MPD_USER=$(grep "^user" "$MPD_CONF" | awk '{print $2}' | tr -d '"')
DB_FILE=$(grep "^db_file" "$MPD_CONF" | sed 's/db_file[[:space:]]*"\(.*\)"/\1/')

echo "Music Directory: $MUSIC_DIR"
echo "MPD User: ${MPD_USER:-not specified}"
echo "Database File: ${DB_FILE:-not specified}"
echo ""

# Check if music directory exists
echo "[2] Music Directory Check"
echo "------------------------------------------------------------"
if [ -d "$MUSIC_DIR" ]; then
    echo "✓ Music directory exists: $MUSIC_DIR"
    
    # Count music files
    MUSIC_COUNT=$(find "$MUSIC_DIR" -type f \( -iname "*.mp3" -o -iname "*.flac" -o -iname "*.wav" -o -iname "*.ogg" -o -iname "*.m4a" \) 2>/dev/null | wc -l)
    echo "  Found $MUSIC_COUNT music file(s)"
    
    if [ "$MUSIC_COUNT" -gt 0 ]; then
        echo ""
        echo "  Sample files:"
        find "$MUSIC_DIR" -type f \( -iname "*.mp3" -o -iname "*.flac" -o -iname "*.wav" -o -iname "*.ogg" -o -iname "*.m4a" \) 2>/dev/null | head -3 | while read file; do
            echo "    - $(basename "$file")"
        done
    fi
else
    echo "✗ Music directory does not exist: $MUSIC_DIR"
fi
echo ""

# Check permissions
echo "[3] Permission Check"
echo "------------------------------------------------------------"
if [ -d "$MUSIC_DIR" ]; then
    echo "Directory permissions:"
    ls -ld "$MUSIC_DIR"
    echo ""
    
    if [ -n "$MPD_USER" ]; then
        echo "Checking if MPD user '$MPD_USER' can access directory..."
        
        # Check if user exists
        if id "$MPD_USER" &>/dev/null; then
            # Check read permission
            if sudo -u "$MPD_USER" test -r "$MUSIC_DIR" 2>/dev/null; then
                echo "✓ MPD user can read music directory"
            else
                echo "✗ MPD user CANNOT read music directory"
                echo "  Fix with: sudo chmod -R a+rX $MUSIC_DIR"
            fi
            
            # Try to list files
            FILE_COUNT=$(sudo -u "$MPD_USER" find "$MUSIC_DIR" -type f 2>/dev/null | wc -l)
            echo "  MPD user can see $FILE_COUNT file(s)"
        else
            echo "⚠ MPD user '$MPD_USER' does not exist"
        fi
    else
        echo "⚠ No user specified in MPD config"
        echo "  MPD will run as system user 'mpd'"
    fi
fi
echo ""

# Check MPD database
echo "[4] MPD Database Check"
echo "------------------------------------------------------------"
if [ -n "$DB_FILE" ] && [ -f "$DB_FILE" ]; then
    echo "Database file exists: $DB_FILE"
    DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
    echo "Database size: $DB_SIZE"
    DB_TIME=$(stat -c %y "$DB_FILE" 2>/dev/null || stat -f "%Sm" "$DB_FILE" 2>/dev/null)
    echo "Last modified: $DB_TIME"
else
    echo "⚠ Database file not found or not specified"
fi
echo ""

# Check MPC stats
echo "[5] MPC Database Statistics"
echo "------------------------------------------------------------"
if command -v mpc &> /dev/null; then
    MPC_STATS=$(mpc stats 2>&1)
    if [ $? -eq 0 ]; then
        echo "$MPC_STATS"
        echo ""
        
        SONG_COUNT=$(echo "$MPC_STATS" | grep "Songs:" | awk '{print $2}')
        if [ -z "$SONG_COUNT" ] || [ "$SONG_COUNT" = "0" ]; then
            echo "⚠ Database is EMPTY!"
            echo ""
            echo "Possible causes:"
            echo "  1. MPD hasn't scanned the music directory yet"
            echo "  2. Permission issue (MPD user can't read files)"
            echo "  3. Music directory path is incorrect in config"
            echo "  4. Music files are in unsupported format"
        else
            echo "✓ Database has $SONG_COUNT song(s)"
        fi
    else
        echo "✗ Could not get MPC stats (is MPD running?)"
        echo "$MPC_STATS"
    fi
else
    echo "✗ MPC not installed"
fi
echo ""

# Check MPD service status
echo "[6] MPD Service Status"
echo "------------------------------------------------------------"
if systemctl is-active --quiet mpd; then
    echo "✓ MPD service is running"
    
    # Check for errors in logs
    echo ""
    echo "Recent MPD log entries:"
    sudo journalctl -u mpd -n 10 --no-pager 2>/dev/null | tail -5
else
    echo "✗ MPD service is NOT running"
    echo "  Start with: sudo systemctl start mpd"
fi
echo ""

# Summary and recommendations
echo "==========================================================="
echo "RECOMMENDATIONS"
echo "==========================================================="
echo ""

if [ ! -d "$MUSIC_DIR" ]; then
    echo "1. Create or fix music directory:"
    echo "   mkdir -p $MUSIC_DIR"
    echo ""
fi

if [ -d "$MUSIC_DIR" ] && [ -n "$MPD_USER" ]; then
    if ! sudo -u "$MPD_USER" test -r "$MUSIC_DIR" 2>/dev/null; then
        echo "2. Fix permissions:"
        echo "   sudo chmod -R a+rX $MUSIC_DIR"
        echo "   sudo chown -R $MPD_USER:audio $MUSIC_DIR"
        echo ""
    fi
fi

SONG_COUNT=$(mpc stats 2>/dev/null | grep "Songs:" | awk '{print $2}')
if [ -z "$SONG_COUNT" ] || [ "$SONG_COUNT" = "0" ]; then
    echo "3. Update MPD database:"
    echo "   mpc update"
    echo "   sleep 5"
    echo "   mpc stats"
    echo ""
fi

echo "4. If issues persist, check MPD logs:"
echo "   sudo journalctl -u mpd -f"
echo ""

echo "5. For detailed diagnostics, run:"
echo "   python app.py dac-diag"
echo ""


