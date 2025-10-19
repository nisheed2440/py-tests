"""
Music player UI main loop
"""

import time
from PIL import Image
from modules.lcd import LCD_1in3, LCD_WIDTH, LCD_HEIGHT
from .player import MusicPlayer
from .controls import InputHandler


def run_player():
    """
    Run the music player UI with full controls.
    
    Controls:
    - KEY1 (GPIO 21)    - Play/Pause
    - Joystick LEFT     - Previous Track
    - Joystick RIGHT    - Next Track
    - Joystick UP       - Volume Up
    - Joystick DOWN     - Volume Down
    - KEY3 (GPIO 16)    - Exit
    """
    print("Initializing Music Player UI...")
    
    # Initialize LCD with button support
    lcd = LCD_1in3(setup_buttons=True)
    lcd.init()
    
    # Initialize music player
    player = MusicPlayer(LCD_WIDTH, LCD_HEIGHT)
    
    # Initialize input handler
    input_handler = InputHandler(lcd.GPIO)
    
    print("\nMusic Player Controls:")
    print("  KEY1 (GPIO 21)    - Play/Pause")
    print("  Joystick LEFT     - Previous Track")
    print("  Joystick RIGHT    - Next Track")
    print("  Joystick UP       - Volume Up")
    print("  Joystick DOWN     - Volume Down")
    print("  KEY3 (GPIO 16)    - Exit")
    print("\nPress Ctrl+C to exit\n")
    
    try:
        while True:
            # Update and display UI
            image = player.draw_ui()
            lcd.display(image)
            
            # Handle button inputs
            presses = input_handler.read_buttons()
            
            # Process button presses
            if presses['key1']:
                player.toggle_play_pause()
                print(f"{'Playing' if player.is_playing else 'Paused'}")
            
            if presses['key3']:
                print("Exiting...")
                break
            
            if presses['joy_left']:
                player.prev_track()
                print(f"Previous: {player.playlist[player.current_track]['title']}")
            
            if presses['joy_right']:
                player.next_track()
                print(f"Next: {player.playlist[player.current_track]['title']}")
            
            if presses['joy_up']:
                player.volume_up()
                print(f"Volume: {player.volume}%")
            
            if presses['joy_down']:
                player.volume_down()
                print(f"Volume: {player.volume}%")
            
            # Update progress animation
            player.update_progress()
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nMusic Player stopped")
    finally:
        # Clear display
        image = Image.new('RGB', (LCD_WIDTH, LCD_HEIGHT), (0, 0, 0))
        lcd.display(image)
        print("Display cleared. Goodbye!")


if __name__ == '__main__':
    run_player()

