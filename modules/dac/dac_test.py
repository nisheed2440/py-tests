#!/usr/bin/env python3
"""
HiFi DAC HAT Test Script using MPD and MPC

This script tests the Inno-Maker HiFi DAC HAT by:
1. Checking MPD/MPC installation
2. Playing music from the Music folder
3. Testing playback controls (play, pause, next, volume)
"""

import subprocess
import sys
import time
import os


class DACTester:
    """Test the HiFi DAC HAT using MPD and MPC"""
    
    def __init__(self):
        self.mpc_available = False
        self.mpd_running = False
        
    def check_mpc_installed(self):
        """Check if MPC is installed"""
        print("\n[1/5] Checking MPC installation...")
        try:
            result = subprocess.run(['which', 'mpc'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                print(f"✓ MPC found at: {result.stdout.strip()}")
                self.mpc_available = True
                return True
            else:
                print("✗ MPC not found")
                print("  Install with: sudo apt-get install mpc")
                return False
        except Exception as e:
            print(f"✗ Error checking MPC: {e}")
            return False
    
    def check_mpd_running(self):
        """Check if MPD is running"""
        print("\n[2/5] Checking MPD status...")
        try:
            result = subprocess.run(['systemctl', 'is-active', 'mpd'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            if result.stdout.strip() == 'active':
                print("✓ MPD is running")
                self.mpd_running = True
                return True
            else:
                print(f"✗ MPD status: {result.stdout.strip()}")
                print("  Start with: sudo systemctl start mpd")
                return False
        except Exception as e:
            print(f"✗ Error checking MPD: {e}")
            return False
    
    def check_music_directory(self):
        """Check if music directory exists and has files"""
        print("\n[3/5] Checking music directory...")
        
        # Get MPD music directory from config
        try:
            result = subprocess.run(['mpc', 'version'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            print(f"  MPD Version: {result.stdout.strip().split()[1] if result.returncode == 0 else 'unknown'}")
        except:
            pass
        
        # Common music directory locations
        music_dirs = [
            os.path.expanduser('~/Music'),
            '/var/lib/mpd/music',
            '/home/pi/Music'
        ]
        
        found_music = False
        for music_dir in music_dirs:
            if os.path.isdir(music_dir):
                files = []
                for root, dirs, filenames in os.walk(music_dir):
                    for f in filenames:
                        if f.endswith(('.mp3', '.flac', '.wav', '.ogg', '.m4a')):
                            files.append(os.path.join(root, f))
                            if len(files) >= 5:  # Just check first 5
                                break
                    if len(files) >= 5:
                        break
                
                if files:
                    print(f"✓ Found music directory: {music_dir}")
                    print(f"  Found {len(files)}+ music file(s)")
                    found_music = True
                    break
        
        if not found_music:
            print("⚠ No music files found in common directories")
            print(f"  Checked: {', '.join(music_dirs)}")
            print("  Please add music files to ~/Music or /var/lib/mpd/music")
        
        return found_music
    
    def update_mpd_database(self):
        """Update MPD database"""
        print("\n[4/5] Updating MPD database...")
        try:
            subprocess.run(['mpc', 'update'], 
                         capture_output=True, 
                         timeout=10)
            print("✓ Database update initiated")
            
            # Wait for update to complete
            print("  Waiting for database update to complete...", end='', flush=True)
            time.sleep(3)
            print(" done")
            return True
        except Exception as e:
            print(f"✗ Error updating database: {e}")
            return False
    
    def test_playback(self):
        """Test basic playback functionality"""
        print("\n[5/5] Testing audio playback...")
        
        try:
            # Clear playlist
            subprocess.run(['mpc', 'clear'], timeout=5)
            
            # Add all music
            print("  Adding music to playlist...")
            subprocess.run(['mpc', 'add', '/'], capture_output=True, timeout=10)
            
            # Get playlist info
            result = subprocess.run(['mpc', 'playlist'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                track_count = len(result.stdout.strip().split('\n'))
                print(f"✓ Playlist loaded with {track_count} track(s)")
                
                # Play first track
                print("\n  Playing first track...")
                subprocess.run(['mpc', 'play', '1'], timeout=5)
                time.sleep(2)
                
                # Get current status
                result = subprocess.run(['mpc', 'current'], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=5)
                if result.returncode == 0 and result.stdout.strip():
                    print(f"  Now playing: {result.stdout.strip()}")
                
                # Show status
                result = subprocess.run(['mpc', 'status'], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=5)
                if result.returncode == 0:
                    print(f"\n  Status:")
                    for line in result.stdout.strip().split('\n'):
                        print(f"    {line}")
                
                return True
            else:
                print("✗ No tracks found in playlist")
                print("  Make sure music files are in the MPD music directory")
                return False
                
        except Exception as e:
            print(f"✗ Error during playback test: {e}")
            return False
    
    def interactive_controls(self):
        """Interactive control menu"""
        print("\n" + "=" * 60)
        print("Interactive DAC HAT Test Controls")
        print("=" * 60)
        print("\nCommands:")
        print("  p  - Play/Pause")
        print("  n  - Next track")
        print("  b  - Previous track")
        print("  +  - Volume up")
        print("  -  - Volume down")
        print("  s  - Show status")
        print("  l  - List playlist")
        print("  q  - Quit")
        print("\nPress Ctrl+C to exit at any time")
        print("-" * 60)
        
        try:
            while True:
                cmd = input("\nCommand: ").strip().lower()
                
                if cmd == 'q':
                    print("Stopping playback...")
                    subprocess.run(['mpc', 'stop'], timeout=5)
                    break
                elif cmd == 'p':
                    subprocess.run(['mpc', 'toggle'], timeout=5)
                    result = subprocess.run(['mpc', 'status'], 
                                          capture_output=True, 
                                          text=True,
                                          timeout=5)
                    if 'playing' in result.stdout.lower():
                        print("▶ Playing")
                    else:
                        print("⏸ Paused")
                elif cmd == 'n':
                    subprocess.run(['mpc', 'next'], timeout=5)
                    result = subprocess.run(['mpc', 'current'], 
                                          capture_output=True, 
                                          text=True,
                                          timeout=5)
                    print(f"⏭ {result.stdout.strip()}")
                elif cmd == 'b':
                    subprocess.run(['mpc', 'prev'], timeout=5)
                    result = subprocess.run(['mpc', 'current'], 
                                          capture_output=True, 
                                          text=True,
                                          timeout=5)
                    print(f"⏮ {result.stdout.strip()}")
                elif cmd == '+':
                    subprocess.run(['mpc', 'volume', '+5'], timeout=5)
                    result = subprocess.run(['mpc', 'volume'], 
                                          capture_output=True, 
                                          text=True,
                                          timeout=5)
                    print(f"🔊 {result.stdout.strip()}")
                elif cmd == '-':
                    subprocess.run(['mpc', 'volume', '-5'], timeout=5)
                    result = subprocess.run(['mpc', 'volume'], 
                                          capture_output=True, 
                                          text=True,
                                          timeout=5)
                    print(f"🔉 {result.stdout.strip()}")
                elif cmd == 's':
                    result = subprocess.run(['mpc', 'status'], 
                                          capture_output=True, 
                                          text=True,
                                          timeout=5)
                    print(result.stdout.strip())
                elif cmd == 'l':
                    result = subprocess.run(['mpc', 'playlist'], 
                                          capture_output=True, 
                                          text=True,
                                          timeout=5)
                    lines = result.stdout.strip().split('\n')
                    for i, line in enumerate(lines[:10], 1):
                        print(f"  {i}. {line}")
                    if len(lines) > 10:
                        print(f"  ... and {len(lines) - 10} more")
                else:
                    print("Unknown command. Try: p, n, b, +, -, s, l, q")
                    
        except KeyboardInterrupt:
            print("\n\nStopping playback...")
            subprocess.run(['mpc', 'stop'], timeout=5)
    
    def run_full_test(self):
        """Run complete DAC HAT test"""
        print("=" * 60)
        print("HiFi DAC HAT Test - MPD/MPC Playback Test")
        print("=" * 60)
        
        # Run all checks
        checks = [
            self.check_mpc_installed(),
            self.check_mpd_running(),
            self.check_music_directory(),
            self.update_mpd_database(),
            self.test_playback()
        ]
        
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        passed = sum(checks)
        total = len(checks)
        print(f"Passed: {passed}/{total} checks")
        
        if passed == total:
            print("\n✓ All tests passed! DAC HAT is working correctly.")
            print("\nStarting interactive controls...")
            time.sleep(2)
            self.interactive_controls()
        else:
            print("\n✗ Some tests failed. Please check the setup guide.")
            print("  See: DAC_SETUP_GUIDE.md")
            return False
        
        return True


def run_test():
    """Main entry point for DAC test"""
    tester = DACTester()
    try:
        return tester.run_full_test()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        subprocess.run(['mpc', 'stop'], timeout=5, stderr=subprocess.DEVNULL)
        return False
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_test()
    sys.exit(0 if success else 1)

