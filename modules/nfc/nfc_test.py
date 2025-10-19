"""
Test suite for the MFRC522 NFC/RFID reader
"""

import time
from .mfrc522 import MFRC522


def format_uid(uid):
    """Format UID as hex string"""
    return ':'.join([f'{x:02X}' for x in uid[:4]])


def run_test():
    """
    Run comprehensive NFC reader tests.
    
    This test will:
    1. Initialize the MFRC522 reader
    2. Continuously scan for NFC cards/tags
    3. Display card UID when detected
    4. Show card type information
    """
    print("Initializing MFRC522 NFC/RFID Reader...")
    
    # Initialize reader
    reader = MFRC522()
    
    print("\n" + "=" * 50)
    print("NFC/RFID Reader Test")
    print("=" * 50)
    print("\nPlace an NFC card or tag near the reader...")
    print("Press Ctrl+C to exit\n")
    
    # Default key for MIFARE Classic
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    
    try:
        last_uid = None
        
        while True:
            # Scan for cards
            (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
            
            # If a card is found
            if status == reader.MI_OK:
                print("Card detected!")
            
            # Get the UID of the card
            (status, uid) = reader.MFRC522_Anticoll()
            
            # If we have the UID, continue
            if status == reader.MI_OK:
                uid_str = format_uid(uid)
                
                # Only print if this is a new card (debounce)
                if uid != last_uid:
                    print("\n" + "-" * 50)
                    print(f"Card UID: {uid_str}")
                    print(f"UID (decimal): {uid[:4]}")
                    
                    # Select the scanned tag
                    size = reader.MFRC522_SelectTag(uid)
                    
                    if size > 0:
                        print(f"Card Size: {size}")
                    
                    # Try to authenticate and read a block
                    status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, 8, key, uid)
                    
                    if status == reader.MI_OK:
                        print("Authentication successful!")
                        
                        # Read block 8
                        data = reader.MFRC522_Read(8)
                        if data:
                            print(f"Block 8 Data: {' '.join([f'{x:02X}' for x in data])}")
                            
                            # Try to decode as ASCII (if printable)
                            try:
                                text = ''.join([chr(x) for x in data if 32 <= x <= 126])
                                if text:
                                    print(f"Block 8 Text: '{text}'")
                            except:
                                pass
                        
                        reader.MFRC522_StopCrypto1()
                    else:
                        print("Authentication failed (this is normal for non-MIFARE Classic cards)")
                    
                    print("-" * 50)
                    print("Waiting for next card...\n")
                    
                    last_uid = uid
                    time.sleep(1)  # Debounce delay
            else:
                # Reset last_uid when no card is present
                last_uid = None
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    finally:
        print("Cleaning up...")
        reader.close()
        print("NFC test done!")


def run_continuous_scan():
    """
    Simple continuous scan mode - just displays UIDs
    """
    print("Starting continuous NFC scan...")
    reader = MFRC522()
    
    print("Place cards near the reader. Press Ctrl+C to exit.\n")
    
    try:
        last_uid = None
        
        while True:
            (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
            
            if status == reader.MI_OK:
                (status, uid) = reader.MFRC522_Anticoll()
                
                if status == reader.MI_OK and uid != last_uid:
                    print(f"Card detected: {format_uid(uid)}")
                    last_uid = uid
                    time.sleep(0.5)
            else:
                last_uid = None
            
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
        raise

