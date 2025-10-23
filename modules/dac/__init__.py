"""
DAC HAT module for testing HiFi DAC HAT with MPD/MPC
"""

from .dac_test import run_test
from .dac_diagnostic import run_diagnostic

__all__ = ['run_test', 'run_diagnostic']

