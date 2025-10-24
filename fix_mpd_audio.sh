#!/bin/bash
# Quick fix for MPD "sndio" audio output error

echo "Fixing MPD audio output configuration..."

MPD_CONF="/etc/mpd.conf"
if [ ! -f "$MPD_CONF" ]; then
    echo "✗ MPD config not found at $MPD_CONF"
    exit 1
fi

# Backup config
if [ ! -f "$MPD_CONF.backup" ]; then
    sudo cp "$MPD_CONF" "$MPD_CONF.backup"
    echo "✓ Backed up config"
fi

# Check if ALSA audio output already configured
if grep -q "type.*\"alsa\"" "$MPD_CONF"; then
    echo "✓ ALSA audio output already configured"
else
    echo "Adding ALSA audio output..."
    sudo bash -c "cat >> $MPD_CONF" <<'EOF'

# Audio output for DAC HAT
audio_output {
    type            "alsa"
    name            "HiFi DAC HAT"
    device          "hw:0,0"
    mixer_type      "hardware"
    mixer_device    "default"
    mixer_control   "Digital"
}
EOF
    echo "✓ Added ALSA configuration"
fi

# Restart MPD
echo "Restarting MPD..."
sudo systemctl restart mpd
sleep 2

if systemctl is-active --quiet mpd; then
    echo "✓ MPD restarted successfully"
    echo ""
    echo "Test with: mpc play"
else
    echo "✗ MPD failed to start"
    echo "Check logs: sudo journalctl -u mpd -n 20"
fi

