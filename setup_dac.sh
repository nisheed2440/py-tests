#!/bin/bash
# Quick setup script for HiFi DAC HAT
# Run this on your Raspberry Pi to set up the DAC

set -e  # Exit on error

echo "================================================"
echo "HiFi DAC HAT Setup Script"
echo "================================================"
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "⚠ Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: Install MPD and MPC
echo "[1/5] Installing MPD and MPC..."
if command -v mpd &> /dev/null && command -v mpc &> /dev/null; then
    echo "✓ MPD and MPC already installed"
else
    sudo apt-get update
    sudo apt-get install -y mpd mpc
    echo "✓ MPD and MPC installed"
fi

# Step 2: Create music directory
echo ""
echo "[2/5] Setting up music directory..."

# Get the actual user (not root, even if run with sudo)
ACTUAL_USER="${SUDO_USER:-$USER}"
ACTUAL_HOME=$(eval echo ~$ACTUAL_USER)
MUSIC_DIR="$ACTUAL_HOME/Music"

echo "  Current user: $ACTUAL_USER"
echo "  Music directory: $MUSIC_DIR"

if [ -d "$MUSIC_DIR" ]; then
    echo "✓ Music directory already exists"
else
    mkdir -p "$MUSIC_DIR"
    # Ensure ownership is correct if created with sudo
    if [ -n "$SUDO_USER" ]; then
        chown "$SUDO_USER:$SUDO_USER" "$MUSIC_DIR"
    fi
    echo "✓ Created music directory"
fi

# Check for music files
MUSIC_COUNT=$(find "$MUSIC_DIR" -type f \( -iname "*.mp3" -o -iname "*.flac" -o -iname "*.wav" -o -iname "*.ogg" -o -iname "*.m4a" \) 2>/dev/null | wc -l)
if [ "$MUSIC_COUNT" -eq 0 ]; then
    echo "⚠ No music files found in $MUSIC_DIR"
    echo "  Please add music files before running the test"
else
    echo "✓ Found $MUSIC_COUNT music file(s)"
fi

# Step 3: Configure boot config
echo ""
echo "[3/5] Checking boot configuration..."
# Check new location first (Bookworm+), then fall back to old location
BOOT_CONFIG="/boot/firmware/config.txt"
if [ ! -f "$BOOT_CONFIG" ]; then
    BOOT_CONFIG="/boot/config.txt"
fi

if [ -f "$BOOT_CONFIG" ]; then
    if grep -q "^dtoverlay=allo-boss-dac-pcm512x-audio" "$BOOT_CONFIG"; then
        echo "✓ Allo Boss DAC overlay already enabled (PCM512x)"
    else
        echo "Adding Allo Boss DAC overlay to $BOOT_CONFIG"
        sudo bash -c "echo '' >> $BOOT_CONFIG"
        sudo bash -c "echo '# HiFi DAC HAT (PCM5122)' >> $BOOT_CONFIG"
        sudo bash -c "echo 'dtoverlay=allo-boss-dac-pcm512x-audio' >> $BOOT_CONFIG"
        echo "✓ DAC overlay added"
        NEED_REBOOT=1
    fi
    
    # Check if onboard audio is disabled
    if grep -q "^dtparam=audio=on" "$BOOT_CONFIG"; then
        echo "Disabling onboard audio..."
        sudo sed -i 's/^dtparam=audio=on/# dtparam=audio=on/' "$BOOT_CONFIG"
        echo "✓ Onboard audio disabled"
        NEED_REBOOT=1
    else
        echo "✓ Onboard audio already disabled"
    fi
else
    echo "⚠ Boot config not found"
    echo "  Checked locations:"
    echo "    - /boot/firmware/config.txt (Bookworm 2023+)"
    echo "    - /boot/config.txt (older versions)"
    echo "  Please manually add: dtoverlay=allo-boss-dac-pcm512x-audio"
fi

# Step 4: Configure MPD
echo ""
echo "[4/5] Configuring MPD..."
MPD_CONF="/etc/mpd.conf"

if [ -f "$MPD_CONF" ]; then
    # Backup original config
    if [ ! -f "$MPD_CONF.backup" ]; then
        sudo cp "$MPD_CONF" "$MPD_CONF.backup"
        echo "✓ Backed up original config to $MPD_CONF.backup"
    fi
    
    # Update music directory
    if grep -q "^music_directory" "$MPD_CONF"; then
        sudo sed -i "s|^music_directory.*|music_directory    \"$MUSIC_DIR\"|" "$MPD_CONF"
        echo "✓ Updated music directory in MPD config to: $MUSIC_DIR"
    else
        echo "⚠ Could not find music_directory setting in config"
    fi
    
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
    
    echo "✓ MPD configuration updated"
    echo "  Note: You may want to review $MPD_CONF"
    echo "  Reference: mpd.conf.sample"
else
    echo "⚠ MPD config not found"
    echo "  Please configure manually using mpd.conf.sample as reference"
fi

# Step 5: Enable and start MPD
echo ""
echo "[5/5] Starting MPD service..."
sudo systemctl enable mpd
sudo systemctl restart mpd

if systemctl is-active --quiet mpd; then
    echo "✓ MPD service is running"
else
    echo "✗ MPD service failed to start"
    echo "  Check logs: sudo journalctl -u mpd -n 50"
fi

# Update MPD database
if command -v mpc &> /dev/null; then
    echo ""
    echo "Updating MPD database..."
    
    # Wait for MPD to fully restart before updating
    sleep 2
    
    # Run update and wait for completion
    mpc update &> /dev/null || true
    
    # Wait for update to process
    echo "  Waiting for database scan to complete..."
    sleep 3
    
    # Check database stats
    DB_STATS=$(mpc stats 2>/dev/null || echo "")
    if echo "$DB_STATS" | grep -q "Songs:"; then
        SONG_COUNT=$(echo "$DB_STATS" | grep "Songs:" | awk '{print $2}')
        if [ "$SONG_COUNT" -gt 0 ]; then
            echo "✓ Database updated successfully"
            echo "  Found $SONG_COUNT song(s) in database"
        else
            echo "⚠ Database updated but no songs found"
            echo "  Music directory may be empty or permissions issue"
            echo "  Check: ls -la $MUSIC_DIR"
        fi
    else
        echo "⚠ Could not verify database stats"
        echo "  Run 'mpc stats' manually to check"
    fi
    
    # Show database update status
    mpc status &> /dev/null || echo "  Note: MPD may still be indexing files"
fi

# Summary
echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""

if [ -n "$NEED_REBOOT" ]; then
    echo "⚠ REBOOT REQUIRED"
    echo ""
    echo "Changes have been made to boot configuration."
    echo "Please reboot your Raspberry Pi to enable the DAC:"
    echo ""
    echo "  sudo reboot"
    echo ""
    echo "After reboot, run the diagnostic:"
    echo "  python app.py dac-diag"
    echo ""
else
    echo "Next steps:"
    echo ""
    echo "1. Run the diagnostic to verify setup:"
    echo "   python app.py dac-diag"
    echo ""
    echo "2. If all checks pass, run the test:"
    echo "   python app.py dac"
    echo ""
fi

echo "Documentation:"
echo "  - DAC_TESTING_SUMMARY.md  - Quick start guide"
echo "  - DAC_SETUP_GUIDE.md      - Complete setup"
echo "  - MPC_QUICK_REFERENCE.md  - Command reference"
echo ""
echo "Enjoy your high-quality audio! 🎵"

