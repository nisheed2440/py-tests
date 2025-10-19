"""
NFC Module for MFRC522 RFID/NFC Reader
Supports reading MIFARE Classic cards and tags
"""

from .mfrc522 import MFRC522
from .nfc_test import run_test

__all__ = ['MFRC522', 'run_test']

