"""
MFRC522 Diagnostic and Hardware Test
Tests board connectivity, SPI communication, and basic functionality
"""

import time
import sys


def test_gpio():
    """Test GPIO module import and setup"""
    print("\n1. Testing GPIO Module...")
    try:
        import RPi.GPIO as GPIO
        print("   ✓ RPi.GPIO imported successfully")
        
        # Test GPIO mode setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        print("   ✓ GPIO mode set to BCM")
        
        return True
    except ImportError:
        print("   ✗ Failed to import RPi.GPIO")
        print("   → Install with: pip install RPi.GPIO")
        return False
    except Exception as e:
        print(f"   ✗ GPIO Error: {e}")
        return False


def test_spi():
    """Test SPI module and device"""
    print("\n2. Testing SPI Interface...")
    try:
        import spidev
        print("   ✓ spidev module imported")
        
        # Try to open SPI device
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 1000000
        print("   ✓ SPI device opened (bus=0, device=0)")
        
        # Test basic SPI communication
        spi.xfer2([0x00])
        print("   ✓ SPI communication test passed")
        
        spi.close()
        return True
    except ImportError:
        print("   ✗ Failed to import spidev")
        print("   → Install with: pip install spidev")
        return False
    except FileNotFoundError:
        print("   ✗ SPI device not found")
        print("   → Enable SPI interface:")
        print("      sudo raspi-config")
        print("      → Interfacing Options → SPI → Enable")
        return False
    except PermissionError:
        print("   ✗ Permission denied accessing SPI")
        print("   → Run with sudo: sudo python ...")
        return False
    except Exception as e:
        print(f"   ✗ SPI Error: {e}")
        return False


def test_mfrc522_library():
    """Test mfrc522 library import"""
    print("\n3. Testing MFRC522 Library...")
    try:
        import mfrc522
        print("   ✓ mfrc522 module imported")
        
        from mfrc522 import SimpleMFRC522
        print("   ✓ SimpleMFRC522 class available")
        
        return True
    except ImportError as e:
        print(f"   ✗ Failed to import mfrc522: {e}")
        print("   → Install with: pip install mfrc522")
        return False
    except Exception as e:
        print(f"   ✗ Library Error: {e}")
        return False


def test_reader_init():
    """Test MFRC522 reader initialization"""
    print("\n4. Testing MFRC522 Reader Initialization...")
    try:
        from mfrc522 import SimpleMFRC522
        
        print("   Initializing reader...")
        reader = SimpleMFRC522()
        print("   ✓ Reader initialized successfully")
        
        # Test if we can access the reader's internal MFRC522 object
        if hasattr(reader, 'READER'):
            print("   ✓ Internal MFRC522 object accessible")
        
        reader.READER.GPIO.cleanup()
        return True
    except Exception as e:
        print(f"   ✗ Initialization failed: {e}")
        print("\n   Common issues:")
        print("   → Check wiring connections")
        print("   → Ensure RST pin is connected to GPIO 25 (pin 22)")
        print("   → Verify 3.3V power supply")
        return False


def test_version_register():
    """Test reading MFRC522 version register"""
    print("\n5. Testing MFRC522 Version Register...")
    try:
        from mfrc522 import SimpleMFRC522
        
        reader = SimpleMFRC522()
        
        # Try to read version register (0x37)
        # This is a low-level test to verify SPI communication with the chip
        version = reader.READER.Read_MFRC522(0x37)
        
        print(f"   Version register value: 0x{version:02X}")
        
        # Common version values:
        # 0x91 or 0x92 for genuine NXP MFRC522
        # 0x88 or other values for clones
        if version in [0x91, 0x92]:
            print("   ✓ Genuine NXP MFRC522 detected")
        elif version == 0x88:
            print("   ✓ MFRC522 clone detected (should work fine)")
        elif version == 0x00 or version == 0xFF:
            print("   ✗ Invalid version (no communication with chip)")
            print("   → Check wiring, especially SPI pins")
            reader.READER.GPIO.cleanup()
            return False
        else:
            print(f"   ⚠ Unusual version value (0x{version:02X})")
            print("   → May be a clone or different chip variant")
        
        reader.READER.GPIO.cleanup()
        return True
    except Exception as e:
        print(f"   ✗ Version register read failed: {e}")
        return False


def test_card_detection():
    """Test card detection (quick 5-second test)"""
    print("\n6. Testing Card Detection (5 seconds)...")
    print("   Place a card near the reader now...")
    
    try:
        from mfrc522 import SimpleMFRC522
        
        reader = SimpleMFRC522()
        detected = False
        
        # Try for 5 seconds
        start_time = time.time()
        attempts = 0
        
        while time.time() - start_time < 5:
            attempts += 1
            try:
                # Quick non-blocking check
                uid, text = reader.read_no_block()
                if uid is not None:
                    print(f"\n   ✓ Card detected!")
                    print(f"   UID: {uid}")
                    detected = True
                    break
            except:
                pass
            
            # Show progress
            if attempts % 10 == 0:
                elapsed = int(time.time() - start_time)
                print(f"   Scanning... ({elapsed}/5 seconds)")
            
            time.sleep(0.1)
        
        reader.READER.GPIO.cleanup()
        
        if not detected:
            print("\n   ✗ No card detected in 5 seconds")
            print("   → Try holding card closer to reader")
            print("   → Ensure card is compatible (MIFARE Classic, etc.)")
            print("   → Check antenna connections on MFRC522 board")
            return False
        
        return True
    except Exception as e:
        print(f"   ✗ Card detection test failed: {e}")
        return False


def run_diagnostic():
    """Run complete diagnostic test suite"""
    print("=" * 60)
    print("MFRC522 Hardware Diagnostic Test")
    print("=" * 60)
    print("\nThis will test your MFRC522 NFC reader setup.")
    print("Make sure you have a card ready for the final test.\n")
    
    results = []
    
    # Run all tests
    results.append(("GPIO Module", test_gpio()))
    results.append(("SPI Interface", test_spi()))
    results.append(("MFRC522 Library", test_mfrc522_library()))
    results.append(("Reader Initialization", test_reader_init()))
    results.append(("Version Register", test_version_register()))
    results.append(("Card Detection", test_card_detection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✓ All tests passed! Your MFRC522 reader is working correctly.")
        print("  You can now use: sudo python app.py nfc")
    elif passed_count >= total_count - 1:
        print("\n⚠ Most tests passed. Try the card detection test again with:")
        print("  - Card held closer to reader")
        print("  - Different card type")
    else:
        print("\n✗ Multiple tests failed. Please check:")
        print("  1. Wiring connections")
        print("  2. SPI is enabled (sudo raspi-config)")
        print("  3. Running with sudo")
        print("  4. Power supply to MFRC522 (3.3V)")
    
    print("\nWiring Reference:")
    print("-" * 60)
    print("MFRC522    Raspberry Pi")
    print("-" * 60)
    print("SDA/NSS    → GPIO 8  (CE0, physical pin 24)")
    print("SCK        → GPIO 11 (SCLK, physical pin 23)")
    print("MOSI       → GPIO 10 (physical pin 19)")
    print("MISO       → GPIO 9  (physical pin 21)")
    print("GND        → Ground  (physical pin 6, 9, 14, 20, 25, 30, 34, or 39)")
    print("RST        → GPIO 25 (BCM) / physical pin 22")
    print("3.3V       → 3.3V    (physical pin 1 or 17)")
    print("-" * 60)


if __name__ == '__main__':
    try:
        run_diagnostic()
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

