"""
Music Player Module for Waveshare 1.3inch LCD HAT
Full-featured music player with album art and playback controls
"""

from .player import MusicPlayer
from .ui import run_player

__all__ = ['MusicPlayer', 'run_player']

