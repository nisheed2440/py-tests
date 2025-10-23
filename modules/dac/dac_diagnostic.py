#!/usr/bin/env python3
"""
HiFi DAC HAT Diagnostic Tool

Comprehensive diagnostic to check:
1. Hardware detection (I2C/sound cards)
2. MPD installation and configuration
3. MPC installation
4. Audio output configuration
5. Music directory setup
"""

import subprocess
import os
import sys


class DACDiagnostic:
    """Diagnostic tool for HiFi DAC HAT setup"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
    
    def print_header(self, text):
        """Print section header"""
        print(f"\n{'=' * 60}")
        print(f"{text}")
        print('=' * 60)
    
    def print_success(self, text):
        """Print success message"""
        print(f"✓ {text}")
    
    def print_warning(self, text):
        """Print warning message"""
        print(f"⚠ {text}")
        self.warnings.append(text)
    
    def print_error(self, text):
        """Print error message"""
        print(f"✗ {text}")
        self.issues.append(text)
    
    def check_i2c_devices(self):
        """Check I2C devices for DAC detection"""
        self.print_header("1. Hardware Detection")
        
        try:
            # Check if i2c-tools is available
            result = subprocess.run(['which', 'i2cdetect'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            
            if result.returncode != 0:
                self.print_warning("i2c-tools not installed (optional)")
                print("  Install with: sudo apt-get install i2c-tools")
                return
            
            # Try to detect I2C devices
            result = subprocess.run(['sudo', 'i2cdetect', '-y', '1'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            
            if result.returncode == 0:
                self.print_success("I2C bus accessible")
                if '4b' in result.stdout or '4a' in result.stdout:
                    self.print_success("PCM5122 DAC chip detected on I2C bus")
                else:
                    self.print_warning("DAC chip not detected on I2C (may be normal)")
            
        except Exception as e:
            self.print_warning(f"Could not check I2C devices: {e}")
    
    def check_sound_cards(self):
        """Check available sound cards"""
        self.print_header("2. Sound Card Detection")
        
        try:
            # Check /proc/asound/cards
            if os.path.exists('/proc/asound/cards'):
                with open('/proc/asound/cards', 'r') as f:
                    cards = f.read()
                
                if 'sndrpihifiberry' in cards.lower() or 'hifiberry' in cards.lower():
                    self.print_success("HiFiBerry DAC detected")
                    print("\n" + cards.strip())
                elif cards.strip():
                    self.print_warning("Sound card detected, but not HiFiBerry")
                    print("\n" + cards.strip())
                else:
                    self.print_error("No sound cards detected")
                    print("  Check /boot/config.txt for DAC overlay")
            else:
                self.print_error("/proc/asound/cards not found")
                
        except Exception as e:
            self.print_error(f"Error checking sound cards: {e}")
    
    def check_alsa_devices(self):
        """Check ALSA audio devices"""
        print("\nALSA Devices:")
        
        try:
            result = subprocess.run(['aplay', '-l'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                print(result.stdout)
                if 'sndrpihifiberry' in result.stdout.lower():
                    self.print_success("DAC appears in ALSA devices")
                else:
                    self.print_warning("DAC not found in ALSA devices list")
            else:
                self.print_error("No ALSA playback devices found")
                
        except Exception as e:
            self.print_error(f"Error checking ALSA devices: {e}")
    
    def check_mpd_installation(self):
        """Check if MPD is installed"""
        self.print_header("3. MPD Installation")
        
        try:
            result = subprocess.run(['which', 'mpd'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            
            if result.returncode == 0:
                self.print_success(f"MPD found at: {result.stdout.strip()}")
                
                # Check version
                result = subprocess.run(['mpd', '--version'], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=5)
                version_line = result.stdout.split('\n')[0]
                print(f"  Version: {version_line}")
            else:
                self.print_error("MPD not installed")
                print("  Install with: sudo apt-get install mpd")
                
        except Exception as e:
            self.print_error(f"Error checking MPD: {e}")
    
    def check_mpd_service(self):
        """Check MPD service status"""
        print("\nMPD Service Status:")
        
        try:
            result = subprocess.run(['systemctl', 'is-active', 'mpd'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            
            if result.stdout.strip() == 'active':
                self.print_success("MPD service is running")
            else:
                self.print_error(f"MPD service status: {result.stdout.strip()}")
                print("  Start with: sudo systemctl start mpd")
                print("  Enable on boot: sudo systemctl enable mpd")
            
            # Show detailed status
            result = subprocess.run(['systemctl', 'status', 'mpd'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            
            # Show last few lines of status
            lines = result.stdout.split('\n')
            for line in lines[:8]:
                if line.strip():
                    print(f"  {line}")
                    
        except Exception as e:
            self.print_error(f"Error checking MPD service: {e}")
    
    def check_mpd_config(self):
        """Check MPD configuration"""
        print("\nMPD Configuration:")
        
        config_paths = [
            '/etc/mpd.conf',
            os.path.expanduser('~/.config/mpd/mpd.conf'),
            os.path.expanduser('~/.mpdconf')
        ]
        
        config_found = False
        for config_path in config_paths:
            if os.path.exists(config_path):
                config_found = True
                self.print_success(f"Config found: {config_path}")
                
                try:
                    with open(config_path, 'r') as f:
                        config = f.read()
                    
                    # Check music directory
                    for line in config.split('\n'):
                        if line.strip().startswith('music_directory'):
                            print(f"  {line.strip()}")
                        elif line.strip().startswith('audio_output'):
                            print(f"  {line.strip()}")
                        elif 'device' in line and not line.strip().startswith('#'):
                            print(f"    {line.strip()}")
                            
                except Exception as e:
                    self.print_warning(f"Could not read config: {e}")
                
                break
        
        if not config_found:
            self.print_warning("No MPD config file found")
            print("  Expected locations:")
            for path in config_paths:
                print(f"    - {path}")
    
    def check_mpc_installation(self):
        """Check if MPC is installed"""
        self.print_header("4. MPC Installation")
        
        try:
            result = subprocess.run(['which', 'mpc'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            
            if result.returncode == 0:
                self.print_success(f"MPC found at: {result.stdout.strip()}")
                
                # Check version
                result = subprocess.run(['mpc', 'version'], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=5)
                version_info = result.stdout.split('\n')
                if version_info:
                    print(f"  Version: {version_info[0]}")
            else:
                self.print_error("MPC not installed")
                print("  Install with: sudo apt-get install mpc")
                
        except Exception as e:
            self.print_error(f"Error checking MPC: {e}")
    
    def check_music_directory(self):
        """Check music directory setup"""
        self.print_header("5. Music Directory")
        
        # First, get MPD's configured music directory
        mpd_music_dir = None
        config_paths = ['/etc/mpd.conf', os.path.expanduser('~/.config/mpd/mpd.conf')]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        for line in f:
                            if line.strip().startswith('music_directory'):
                                mpd_music_dir = line.split('"')[1] if '"' in line else line.split()[1]
                                mpd_music_dir = os.path.expanduser(mpd_music_dir)
                                print(f"MPD configured music directory: {mpd_music_dir}")
                                break
                except Exception as e:
                    pass
        
        music_dirs = [
            os.path.expanduser('~/Music'),
            '/var/lib/mpd/music',
            '/home/pi/Music'
        ]
        
        # Add MPD's configured directory if different
        if mpd_music_dir and mpd_music_dir not in music_dirs:
            music_dirs.insert(0, mpd_music_dir)
        
        found_music = False
        for music_dir in music_dirs:
            if os.path.isdir(music_dir):
                # Count music files
                music_files = []
                try:
                    for root, dirs, files in os.walk(music_dir):
                        for f in files:
                            if f.endswith(('.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac')):
                                music_files.append(f)
                                if len(music_files) >= 10:
                                    break
                        if len(music_files) >= 10:
                            break
                    
                    if music_files:
                        self.print_success(f"Music found in: {music_dir}")
                        print(f"  Found {len(music_files)}+ music file(s)")
                        
                        # Check if this matches MPD's configured directory
                        if mpd_music_dir and music_dir != mpd_music_dir:
                            self.print_warning(f"Music found in {music_dir} but MPD is configured to use {mpd_music_dir}")
                        
                        found_music = True
                        
                        # Show first few files
                        for i, f in enumerate(music_files[:3], 1):
                            print(f"    {i}. {f}")
                        
                        break
                except Exception as e:
                    self.print_warning(f"Error scanning {music_dir}: {e}")
        
        if not found_music:
            self.print_error("No music files found")
            print("  Expected locations:")
            for music_dir in music_dirs:
                print(f"    - {music_dir}")
            print("\n  Supported formats: .mp3, .flac, .wav, .ogg, .m4a, .aac")
        
        # Check MPD database stats
        print("\nMPD Database Status:")
        try:
            result = subprocess.run(['mpc', 'stats'], 
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Songs:' in line or 'Artists:' in line or 'Albums:' in line:
                        print(f"  {line.strip()}")
                
                # Check if database has songs
                if 'Songs: 0' in result.stdout or not any('Songs:' in line for line in result.stdout.split('\n')):
                    self.print_warning("MPD database is empty")
                    print("  Run: mpc update")
                else:
                    self.print_success("MPD database has indexed music")
            else:
                self.print_warning("Could not check MPD database stats")
        except Exception as e:
            self.print_warning(f"Error checking database: {e}")
    
    def check_boot_config(self):
        """Check boot configuration for DAC overlay"""
        self.print_header("6. Boot Configuration")
        
        # Check new location first (Bookworm+), then fall back to old location
        boot_config = '/boot/firmware/config.txt'
        if not os.path.exists(boot_config):
            boot_config = '/boot/config.txt'
        
        if os.path.exists(boot_config):
            try:
                with open(boot_config, 'r') as f:
                    config = f.read()
                
                if 'dtoverlay=allo-boss-dac-pcm512x-audio' in config:
                    self.print_success("Allo Boss DAC overlay enabled (PCM512x)")
                elif 'dtoverlay=hifiberry-dacplus' in config:
                    self.print_warning("HiFiBerry overlay found, but Allo Boss is recommended for PCM5122")
                    print("  Consider changing to: dtoverlay=allo-boss-dac-pcm512x-audio")
                elif 'dtoverlay=' in config and 'dac' in config.lower():
                    self.print_success("DAC overlay found in config")
                    for line in config.split('\n'):
                        if 'dtoverlay=' in line and 'dac' in line.lower():
                            print(f"  {line.strip()}")
                else:
                    self.print_warning("No DAC overlay found in boot config")
                    print(f"  Add to {boot_config}:")
                    print("    dtoverlay=allo-boss-dac-pcm512x-audio")
                    
            except Exception as e:
                self.print_warning(f"Could not read boot config: {e}")
        else:
            self.print_warning("Boot config not found")
            print("  Expected locations:")
            print("    - /boot/firmware/config.txt (Bookworm 2023+)")
            print("    - /boot/config.txt (older versions)")
    
    def print_summary(self):
        """Print diagnostic summary"""
        self.print_header("Diagnostic Summary")
        
        if not self.issues and not self.warnings:
            print("\n✓ All checks passed! Your DAC HAT setup looks good.")
            print("\nYou can now run the DAC test:")
            print("  python app.py dac")
            
        else:
            if self.issues:
                print(f"\n✗ Found {len(self.issues)} issue(s):")
                for i, issue in enumerate(self.issues, 1):
                    print(f"  {i}. {issue}")
            
            if self.warnings:
                print(f"\n⚠ Found {len(self.warnings)} warning(s):")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"  {i}. {warning}")
            
            print("\nRefer to DAC_SETUP_GUIDE.md for detailed setup instructions.")
    
    def run_full_diagnostic(self):
        """Run complete diagnostic"""
        print("=" * 60)
        print("HiFi DAC HAT - Comprehensive Diagnostic")
        print("=" * 60)
        
        self.check_i2c_devices()
        self.check_sound_cards()
        self.check_alsa_devices()
        self.check_mpd_installation()
        self.check_mpd_service()
        self.check_mpd_config()
        self.check_mpc_installation()
        self.check_music_directory()
        self.check_boot_config()
        
        self.print_summary()


def run_diagnostic():
    """Main entry point for diagnostic"""
    diagnostic = DACDiagnostic()
    try:
        diagnostic.run_full_diagnostic()
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_diagnostic()

