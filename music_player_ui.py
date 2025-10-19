#!/usr/bin/env python3
"""
Music Player UI for Waveshare 1.3inch LCD HAT
Displays a music player interface with album art, track info, and controls
"""

import time
import spidev as SPI
import os
from PIL import Image, ImageDraw, ImageFont

# LCD Configuration
LCD_WIDTH = 240
LCD_HEIGHT = 240

# Pin definitions (BCM)
RST_PIN = 27
DC_PIN = 25
BL_PIN = 24
CS_PIN = 8

# Button pins
KEY1 = 21
KEY2 = 20
KEY3 = 16
JOY_UP = 6
JOY_DOWN = 19
JOY_LEFT = 5
JOY_RIGHT = 26
JOY_PRESS = 13

# SPI Configuration
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED = 40000000  # 40 MHz

class LCD_1in3:
    def __init__(self):
        import RPi.GPIO as GPIO
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(RST_PIN, GPIO.OUT)
        self.GPIO.setup(DC_PIN, GPIO.OUT)
        self.GPIO.setup(BL_PIN, GPIO.OUT)
        self.GPIO.output(BL_PIN, GPIO.HIGH)
        
        # Setup button inputs
        for pin in [KEY1, KEY2, KEY3, JOY_UP, JOY_DOWN, JOY_LEFT, JOY_RIGHT, JOY_PRESS]:
            self.GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.spi = SPI.SpiDev(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_SPEED
        self.spi.mode = 0b00
        
    def reset(self):
        self.GPIO.output(RST_PIN, self.GPIO.HIGH)
        time.sleep(0.01)
        self.GPIO.output(RST_PIN, self.GPIO.LOW)
        time.sleep(0.01)
        self.GPIO.output(RST_PIN, self.GPIO.HIGH)
        time.sleep(0.01)
        
    def write_cmd(self, cmd):
        self.GPIO.output(DC_PIN, self.GPIO.LOW)
        self.spi.writebytes([cmd])
        
    def write_data(self, data):
        self.GPIO.output(DC_PIN, self.GPIO.HIGH)
        self.spi.writebytes([data])
        
    def init(self):
        self.reset()
        
        self.write_cmd(0x36)
        self.write_data(0x70)
        
        self.write_cmd(0x3A)
        self.write_data(0x05)
        
        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)
        
        self.write_cmd(0xB7)
        self.write_data(0x35)
        
        self.write_cmd(0xBB)
        self.write_data(0x19)
        
        self.write_cmd(0xC0)
        self.write_data(0x2C)
        
        self.write_cmd(0xC2)
        self.write_data(0x01)
        
        self.write_cmd(0xC3)
        self.write_data(0x12)
        
        self.write_cmd(0xC4)
        self.write_data(0x20)
        
        self.write_cmd(0xC6)
        self.write_data(0x0F)
        
        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)
        
        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)
        
        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)
        
        self.write_cmd(0x11)
        time.sleep(0.12)
        
        self.write_cmd(0x29)
        
    def set_window(self, x_start, y_start, x_end, y_end):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(x_start)
        self.write_data(0x00)
        self.write_data(x_end - 1)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(y_start)
        self.write_data(0x00)
        self.write_data(y_end - 1)
        
        self.write_cmd(0x2C)
        
    def display(self, image):
        img = image.rotate(0)
        pix = img.load()
        self.set_window(0, 0, LCD_WIDTH, LCD_HEIGHT)
        self.GPIO.output(DC_PIN, self.GPIO.HIGH)
        
        for y in range(LCD_HEIGHT):
            line = []
            for x in range(LCD_WIDTH):
                r, g, b = pix[x, y]
                rgb = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                line.append(rgb >> 8)
                line.append(rgb & 0xFF)
            self.spi.writebytes(line)

class MusicPlayer:
    def __init__(self, lcd):
        self.lcd = lcd
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
        image = Image.new('RGB', (LCD_WIDTH, LCD_HEIGHT), (20, 20, 30))
        draw = ImageDraw.Draw(image)
        
        track = self.playlist[self.current_track]
        
        # Header - Now Playing
        draw.text((10, 5), "NOW PLAYING", fill=(150, 150, 150))
        
        # Album art (centered)
        art_size = 100
        art_x = (LCD_WIDTH - art_size) // 2
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
        start_x = (LCD_WIDTH - (button_size * 3 + spacing * 2)) // 2
        
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

def main():
    print("Initializing Music Player UI...")
    lcd = LCD_1in3()
    lcd.init()
    
    player = MusicPlayer(lcd)
    
    print("Music Player Controls:")
    print("  KEY1 (GPIO 21)    - Play/Pause")
    print("  Joystick LEFT     - Previous Track")
    print("  Joystick RIGHT    - Next Track")
    print("  Joystick UP       - Volume Up")
    print("  Joystick DOWN     - Volume Down")
    print("  KEY3 (GPIO 16)    - Exit")
    print("\nPress Ctrl+C to exit")
    
    last_key1 = True
    last_key3 = True
    last_joy_left = True
    last_joy_right = True
    last_joy_up = True
    last_joy_down = True
    
    try:
        while True:
            # Update and display UI
            image = player.draw_ui()
            lcd.display(image)
            
            # Handle button inputs
            key1 = lcd.GPIO.input(KEY1)
            key3 = lcd.GPIO.input(KEY3)
            joy_left = lcd.GPIO.input(JOY_LEFT)
            joy_right = lcd.GPIO.input(JOY_RIGHT)
            joy_up = lcd.GPIO.input(JOY_UP)
            joy_down = lcd.GPIO.input(JOY_DOWN)
            
            # Detect button presses (active low)
            if not key1 and last_key1:
                player.toggle_play_pause()
                print(f"{'Playing' if player.is_playing else 'Paused'}")
            
            if not key3 and last_key3:
                print("Exiting...")
                break
            
            if not joy_left and last_joy_left:
                player.prev_track()
                print(f"Previous: {player.playlist[player.current_track]['title']}")
            
            if not joy_right and last_joy_right:
                player.next_track()
                print(f"Next: {player.playlist[player.current_track]['title']}")
            
            if not joy_up and last_joy_up:
                player.volume_up()
                print(f"Volume: {player.volume}%")
            
            if not joy_down and last_joy_down:
                player.volume_down()
                print(f"Volume: {player.volume}%")
            
            # Update last states
            last_key1 = key1
            last_key3 = key3
            last_joy_left = joy_left
            last_joy_right = joy_right
            last_joy_up = joy_up
            last_joy_down = joy_down
            
            # Update progress animation
            player.update_progress()
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nMusic Player stopped")
    
    # Clear display
    image = Image.new('RGB', (LCD_WIDTH, LCD_HEIGHT), (0, 0, 0))
    lcd.display(image)
    print("Display cleared. Goodbye!")

if __name__ == '__main__':
    main()

