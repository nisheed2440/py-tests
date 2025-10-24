#!/bin/bash
# Quick fix for MPD "sndio" audio output error

echo "Fixing MPD audio output configuration..."
echo ""

# Detect sound card
echo "Detecting sound cards..."
if [ -f /proc/asound/cards ]; then
    cat /proc/asound/cards
    echo ""
fi

# Find the correct device
DEVICE="hw:0,0"
if aplay -l 2>/dev/null | grep -qi "Allo Boss DAC"; then
    DEVICE="hw:CARD=BossDAC,DEV=0"
    echo "✓ Detected Allo Boss DAC, using: $DEVICE"
elif aplay -l 2>/dev/null | grep -qi "boss"; then
    DEVICE="hw:CARD=BossDAC,DEV=0"
    echo "✓ Detected Boss DAC, using: $DEVICE"
elif aplay -l 2>/dev/null | grep -qi "hifiberry"; then
    DEVICE="hw:CARD=sndrpihifiberry,DEV=0"
    echo "✓ Detected HiFiBerry, using: $DEVICE"
else
    echo "Using default: $DEVICE"
fi
echo ""

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

# Remove old audio_output if exists
if grep -q "^audio_output" "$MPD_CONF"; then
    echo "Removing old audio output configuration..."
    sudo sed -i '/^audio_output/,/^}/d' "$MPD_CONF"
fi

echo "Adding ALSA audio output with 32-bit format..."
sudo bash -c "cat >> $MPD_CONF" <<EOF

# Audio output for DAC HAT (PCM5122 requires 24/32-bit)
audio_output {
    type            "alsa"
    name            "HiFi DAC HAT"
    device          "$DEVICE"
    mixer_type      "hardware"
    mixer_device    "default"
    mixer_control   "Digital"
    format          "44100:32:2"
    auto_resample   "no"
    auto_format     "no"
}
EOF
echo "✓ Added ALSA configuration with 32-bit format"

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

