"""
Test suite for the MFRC522 NFC/RFID reader
Uses the mfrc522-python library
"""

import time
from mfrc522 import SimpleMFRC522


def format_uid(uid):
    """Format UID as hex string"""
    # Convert integer UID to hex string
    hex_str = f'{uid:012X}'
    # Format as XX:XX:XX:XX:XX:XX
    return ':'.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)])


def run_test():
    """
    Run comprehensive NFC reader tests.
    
    This test will:
    1. Initialize the MFRC522 reader
    2. Continuously scan for NFC cards/tags
    3. Display card UID (Unique Identifier)
    4. Display any text data stored on the card
    """
    print("Initializing MFRC522 NFC/RFID Reader...")
    
    # Initialize reader using SimpleMFRC522
    reader = SimpleMFRC522()
    
    print("\n" + "=" * 50)
    print("NFC/RFID Reader Test")
    print("=" * 50)
    print("\nPlace an NFC card or tag near the reader...")
    print("Press Ctrl+C to exit\n")
    
    try:
        last_uid = None
        
        while True:
            print("Waiting for card...")
            
            try:
                # Read card (this will block until a card is detected)
                uid, text = reader.read_no_block()
                
                if uid is not None:
                    # Only print if this is a new card (debounce)
                    if uid != last_uid:
                        print("\n" + "-" * 50)
                        print(f"Card Detected!")
                        print(f"UID (decimal): {uid}")
                        print(f"UID (hex): {format_uid(uid)}")
                        
                        # Display text data if present
                        if text and text.strip():
                            print(f"Text Data: '{text.strip()}'")
                        else:
                            print("Text Data: (empty)")
                        
                        print("-" * 50)
                        print("Waiting for next card...\n")
                        
                        last_uid = uid
                        time.sleep(1)  # Debounce delay
                else:
                    # Reset last_uid when no card is present
                    last_uid = None
                
            except Exception as e:
                # Handle read errors gracefully
                if "Timeout" not in str(e):
                    print(f"Read error: {e}")
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    finally:
        print("Cleaning up...")
        reader.close()
        print("NFC test done!")


def run_write_test(text_to_write):
    """
    Write text to an NFC card
    
    Args:
        text_to_write: String to write to the card (max ~700 characters)
    """
    print("Initializing MFRC522 NFC/RFID Reader...")
    reader = SimpleMFRC522()
    
    print("\n" + "=" * 50)
    print("NFC/RFID Write Test")
    print("=" * 50)
    print(f"\nReady to write: '{text_to_write}'")
    print("Place card near reader to write...")
    
    try:
        print("Writing...")
        reader.write(text_to_write)
        print("\n✓ Write successful!")
        print(f"Written: '{text_to_write}'")
    except KeyboardInterrupt:
        print("\n\nWrite cancelled by user")
    except Exception as e:
        print(f"\n✗ Write failed: {e}")
    finally:
        print("Cleaning up...")
        reader.close()
        print("Done!")


def run_continuous_scan():
    """
    Simple continuous scan mode - displays UIDs and text quickly
    """
    print("Starting continuous NFC scan...")
    reader = SimpleMFRC522()
    
    print("Place cards near the reader. Press Ctrl+C to exit.\n")
    
    try:
        last_uid = None
        
        while True:
            try:
                uid, text = reader.read_no_block()
                
                if uid is not None and uid != last_uid:
                    text_display = text.strip() if text and text.strip() else "(empty)"
                    print(f"Card: {format_uid(uid)} | Text: {text_display}")
                    last_uid = uid
                    time.sleep(0.5)
                elif uid is None:
                    last_uid = None
            except:
                pass
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        reader.close()


if __name__ == '__main__':
    try:
        run_test()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
