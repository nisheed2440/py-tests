# DAC Module Changelog

## Update - Corrected Device Tree Overlay (October 23, 2024)

### Issue Identified
The initial implementation recommended using `dtoverlay=hifiberry-dacplus`, but the official Inno-Maker HiFi DAC HAT manual specifies `dtoverlay=allo-boss-dac-pcm512x-audio` as the correct overlay for the PCM5122 chip.

### Changes Made

#### 1. Documentation Updates
All documentation has been updated to use the correct overlay:

**Files Updated:**
- ✅ `README.md` - Updated hardware configuration section
- ✅ `DAC_SETUP_GUIDE.md` - Updated all references to the overlay
- ✅ `DAC_TESTING_SUMMARY.md` - Updated quick start instructions
- ✅ `DAC_IMPLEMENTATION_NOTES.md` - Updated technical specifications
- ✅ `modules/dac/README.md` - Updated configuration section
- ✅ `OVERLAY_NOTE.md` - **NEW**: Detailed explanation of overlay choice

**Changes:**
- Old: `dtoverlay=hifiberry-dacplus`
- New: `dtoverlay=allo-boss-dac-pcm512x-audio`

#### 2. Code Updates

**`modules/dac/dac_diagnostic.py`**
- Updated to check for `allo-boss-dac-pcm512x-audio` as the primary overlay
- Added helpful warning if `hifiberry-dacplus` is detected
- Suggests the correct overlay if neither is found

Before:
```python
if 'dtoverlay=hifiberry-dacplus' in config:
    self.print_success("HiFiBerry DAC overlay enabled")
```

After:
```python
if 'dtoverlay=allo-boss-dac-pcm512x-audio' in config:
    self.print_success("Allo Boss DAC overlay enabled (PCM512x)")
elif 'dtoverlay=hifiberry-dacplus' in config:
    self.print_warning("HiFiBerry overlay found, but Allo Boss is recommended for PCM5122")
    print("  Consider changing to: dtoverlay=allo-boss-dac-pcm512x-audio")
```

#### 3. Setup Script Updates

**`setup_dac.sh`**
- Updated to install the correct overlay
- Changed all detection logic to look for `allo-boss-dac-pcm512x-audio`
- Updated user-facing messages

Before:
```bash
echo 'dtoverlay=hifiberry-dacplus' >> $BOOT_CONFIG
```

After:
```bash
echo 'dtoverlay=allo-boss-dac-pcm512x-audio' >> $BOOT_CONFIG
```

### Why This Change?

#### Technical Reasons
1. **Chip Compatibility**: The Inno-Maker HiFi DAC HAT uses the PCM5122 chip, which is part of the PCM512x family
2. **Allo Boss Compatibility**: The Allo Boss DAC uses the same PCM512x chipset
3. **Optimized Driver**: The `allo-boss-dac-pcm512x-audio` overlay is specifically designed for this chip family
4. **Better Hardware Support**: Provides proper mixer controls and volume management

#### Source
- Official Inno-Maker HiFi DAC HAT User Manual (V1.2)
- Page reference: Device tree overlay configuration section
- Manual URL: https://www.inno-maker.com/wp-content/uploads/2017/11/HIFI-DAC-User-Manual-V1.2.pdf

### Backward Compatibility

The `hifiberry-dacplus` overlay may still work for basic functionality, but:
- The diagnostic tool will now warn users about it
- Recommends switching to the correct overlay
- Both overlays use compatible drivers

### Impact on Users

#### Existing Users
If you previously set up your DAC with `hifiberry-dacplus`:
1. Your DAC should still work
2. Run `python app.py dac-diag` to see the recommendation
3. To update, edit `/boot/config.txt`:
   ```bash
   sudo nano /boot/config.txt
   # Change: dtoverlay=hifiberry-dacplus
   # To: dtoverlay=allo-boss-dac-pcm512x-audio
   sudo reboot
   ```

#### New Users
Follow the updated documentation:
- Start with: [DAC_TESTING_SUMMARY.md](DAC_TESTING_SUMMARY.md)
- Or run: `./setup_dac.sh` (uses correct overlay automatically)

### Files Modified

#### Documentation (7 files)
1. `README.md`
2. `DAC_SETUP_GUIDE.md`
3. `DAC_TESTING_SUMMARY.md`
4. `DAC_IMPLEMENTATION_NOTES.md`
5. `modules/dac/README.md`
6. `OVERLAY_NOTE.md` (NEW)
7. `CHANGELOG_DAC.md` (NEW - this file)

#### Code (2 files)
1. `modules/dac/dac_diagnostic.py`
2. `setup_dac.sh`

#### Total Changes
- **Lines modified**: ~30 across all files
- **New files**: 2 (OVERLAY_NOTE.md, CHANGELOG_DAC.md)
- **Breaking changes**: None (backward compatible with warning)

### Testing Recommendations

After updating the overlay:

1. **Verify detection:**
   ```bash
   cat /proc/asound/cards
   ```

2. **Run diagnostic:**
   ```bash
   python app.py dac-diag
   ```

3. **Test playback:**
   ```bash
   python app.py dac
   ```

### Additional Resources

- **[OVERLAY_NOTE.md](OVERLAY_NOTE.md)** - Detailed explanation of overlay choice
- **[DAC_SETUP_GUIDE.md](DAC_SETUP_GUIDE.md)** - Complete setup guide
- **[Inno-Maker Manual (PDF)](https://www.inno-maker.com/wp-content/uploads/2017/11/HIFI-DAC-User-Manual-V1.2.pdf)** - Official documentation

### Credits

Thanks to the user for catching this discrepancy and referring to the official manual!

### Version History

- **v1.0** (Initial) - Used `hifiberry-dacplus` overlay
- **v1.1** (Current) - Corrected to `allo-boss-dac-pcm512x-audio` overlay

---

## Summary

✅ All documentation updated with correct overlay
✅ Diagnostic tool enhanced to detect and warn
✅ Setup script uses correct overlay
✅ Backward compatibility maintained
✅ User guidance provided for migration
✅ Additional documentation created (OVERLAY_NOTE.md)

The DAC testing module is now fully aligned with the official Inno-Maker documentation and will provide users with the optimal configuration for their HiFi DAC HAT.

