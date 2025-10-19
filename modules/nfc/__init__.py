"""
NFC Module for MFRC522 RFID/NFC Reader
Supports reading MIFARE Classic cards and tags
Uses the mfrc522-python library
"""

from .nfc_test import run_test
from .diagnostic import run_diagnostic

__all__ = ['run_test', 'run_diagnostic']

