"""
Music player logic and state management
"""

import os
from PIL import Image, ImageDraw


class MusicPlayer:
    """Music player with playlist management and playback state"""
    
    def __init__(self, lcd_width=240, lcd_height=240):
        self.lcd_width = lcd_width
        self.lcd_height = lcd_height
        self.is_playing = False
        self.current_track = 0
        self.volume = 75
        self.progress = 0
        
        # Sample playlist with cover art
        self.playlist = [
            {"title": "Midnight Dreams", "artist": "Luna Eclipse", "duration": 245, "cover": "album_cover_vinyl.png"},
            {"title": "Electric Waves", "artist": "Neon Pulse", "duration": 198, "cover": "album_cover_neon.png"},
            {"title": "Sunset Boulevard", "artist": "Jazz Collective", "duration": 312, "cover": "album_cover_gradient.png"},
            {"title": "Digital Love", "artist": "Synthwave 84", "duration": 267, "cover": "album_cover_abstract.png"},
        ]
        
        # Load album covers
        self.covers = {}
        for track in self.playlist:
            if os.path.exists(track["cover"]):
                self.covers[track["cover"]] = Image.open(track["cover"]).convert('RGB')
            else:
                self.covers[track["cover"]] = None
    
    def draw_album_art(self, image, x, y, size, cover_file):
        """Draw album art - either from file or placeholder"""
        cover = self.covers.get(cover_file)
        
        if cover:
            # Paste the actual album cover
            image.paste(cover, (x, y))
        else:
            # Draw placeholder if cover not found
            draw = ImageDraw.Draw(image)
            # Gradient background
            for i in range(size):
                color_val = 180 - int(i * 0.5)
                draw.rectangle([(x, y + i), (x + size, y + i + 1)], fill=(color_val, 60, 120))
            
            # Musical note icon
            draw.ellipse([x + size//2 - 15, y + size//2 + 10, x + size//2 + 5, y + size//2 + 30], fill=(255, 255, 255))
            draw.rectangle([x + size//2 + 15, y + size//2 - 20, x + size//2 + 20, y + size//2 + 20], fill=(255, 255, 255))
            draw.ellipse([x + size//2 + 5, y + size//2 + 10, x + size//2 + 25, y + size//2 + 30], fill=(255, 255, 255))
        
        # Border
        draw = ImageDraw.Draw(image)
        draw.rectangle([x, y, x + size, y + size], outline=(255, 255, 255), width=2)
    
    def draw_progress_bar(self, draw, x, y, width, height, progress):
        """Draw progress bar"""
        # Background
        draw.rectangle([x, y, x + width, y + height], fill=(40, 40, 40), outline=(100, 100, 100))
        
        # Progress fill
        fill_width = int(width * progress)
        if fill_width > 0:
            draw.rectangle([x, y, x + fill_width, y + height], fill=(100, 200, 255))
    
    def draw_control_button(self, draw, x, y, size, icon_type, active=False):
        """Draw control buttons"""
        color = (100, 200, 255) if active else (200, 200, 200)
        
        # Circle background
        draw.ellipse([x, y, x + size, y + size], outline=color, width=2)
        
        center_x = x + size // 2
        center_y = y + size // 2
        
        if icon_type == "prev":
            # Previous track (double left arrow)
            draw.polygon([
                (center_x + 5, center_y - 8), (center_x - 3, center_y), (center_x + 5, center_y + 8)
            ], fill=color)
            draw.polygon([
                (center_x - 3, center_y - 8), (center_x - 11, center_y), (center_x - 3, center_y + 8)
            ], fill=color)
        elif icon_type == "play":
            # Play button (triangle)
            draw.polygon([
                (center_x - 5, center_y - 8), (center_x + 8, center_y), (center_x - 5, center_y + 8)
            ], fill=color)
        elif icon_type == "pause":
            # Pause button (two bars)
            draw.rectangle([center_x - 6, center_y - 8, center_x - 2, center_y + 8], fill=color)
            draw.rectangle([center_x + 2, center_y - 8, center_x + 6, center_y + 8], fill=color)
        elif icon_type == "next":
            # Next track (double right arrow)
            draw.polygon([
                (center_x - 5, center_y - 8), (center_x + 3, center_y), (center_x - 5, center_y + 8)
            ], fill=color)
            draw.polygon([
                (center_x + 3, center_y - 8), (center_x + 11, center_y), (center_x + 3, center_y + 8)
            ], fill=color)
    
    def format_time(self, seconds):
        """Convert seconds to MM:SS format"""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"
    
    def draw_ui(self):
        """Draw the complete music player UI"""
        # Create image
        image = Image.new('RGB', (self.lcd_width, self.lcd_height), (20, 20, 30))
        draw = ImageDraw.Draw(image)
        
        track = self.playlist[self.current_track]
        
        # Header - Now Playing
        draw.text((10, 5), "NOW PLAYING", fill=(150, 150, 150))
        
        # Album art (centered)
        art_size = 100
        art_x = (self.lcd_width - art_size) // 2
        self.draw_album_art(image, art_x, 25, art_size, track["cover"])
        
        # Track title (bold/larger)
        title_y = 135
        title = track["title"]
        if len(title) > 18:
            title = title[:18] + "..."
        draw.text((10, title_y), title, fill=(255, 255, 255))
        
        # Artist name
        artist = track["artist"]
        if len(artist) > 20:
            artist = artist[:20] + "..."
        draw.text((10, title_y + 16), artist, fill=(180, 180, 180))
        
        # Progress bar
        current_time = int(track["duration"] * self.progress)
        self.draw_progress_bar(draw, 10, 175, 220, 6, self.progress)
        
        # Time stamps
        time_text = f"{self.format_time(current_time)} / {self.format_time(track['duration'])}"
        draw.text((10, 185), time_text, fill=(150, 150, 150))
        
        # Control buttons
        button_y = 205
        button_size = 28
        spacing = 60
        start_x = (self.lcd_width - (button_size * 3 + spacing * 2)) // 2
        
        self.draw_control_button(draw, start_x, button_y, button_size, "prev")
        play_pause = "pause" if self.is_playing else "play"
        self.draw_control_button(draw, start_x + spacing, button_y, button_size, play_pause, active=True)
        self.draw_control_button(draw, start_x + spacing * 2, button_y, button_size, "next")
        
        # Volume indicator (small)
        vol_text = f"Vol: {self.volume}%"
        draw.text((190, 5), vol_text, fill=(150, 150, 150))
        
        return image
    
    def update_progress(self):
        """Simulate playback progress"""
        if self.is_playing:
            track = self.playlist[self.current_track]
            self.progress += 1.0 / track["duration"]
            if self.progress >= 1.0:
                self.progress = 0.0
                self.next_track()
    
    def toggle_play_pause(self):
        """Toggle play/pause state"""
        self.is_playing = not self.is_playing
    
    def next_track(self):
        """Skip to next track"""
        self.current_track = (self.current_track + 1) % len(self.playlist)
        self.progress = 0.0
    
    def prev_track(self):
        """Go to previous track"""
        if self.progress > 0.05:
            self.progress = 0.0
        else:
            self.current_track = (self.current_track - 1) % len(self.playlist)
            self.progress = 0.0
    
    def volume_up(self):
        """Increase volume"""
        self.volume = min(100, self.volume + 5)
    
    def volume_down(self):
        """Decrease volume"""
        self.volume = max(0, self.volume - 5)

