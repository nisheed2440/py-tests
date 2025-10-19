"""
Button and input control definitions for the music player
"""

# Button pins (BCM)
KEY1 = 21
KEY2 = 20
KEY3 = 16
JOY_UP = 6
JOY_DOWN = 19
JOY_LEFT = 5
JOY_RIGHT = 26
JOY_PRESS = 13


class InputHandler:
    """Handle button inputs for the music player"""
    
    def __init__(self, gpio):
        self.GPIO = gpio
        
        # Setup button inputs
        for pin in [KEY1, KEY2, KEY3, JOY_UP, JOY_DOWN, JOY_LEFT, JOY_RIGHT, JOY_PRESS]:
            self.GPIO.setup(pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        
        # Button state tracking
        self.last_states = {
            'key1': True,
            'key3': True,
            'joy_left': True,
            'joy_right': True,
            'joy_up': True,
            'joy_down': True,
        }
    
    def read_buttons(self):
        """Read all button states and detect presses (active low)"""
        current = {
            'key1': self.GPIO.input(KEY1),
            'key3': self.GPIO.input(KEY3),
            'joy_left': self.GPIO.input(JOY_LEFT),
            'joy_right': self.GPIO.input(JOY_RIGHT),
            'joy_up': self.GPIO.input(JOY_UP),
            'joy_down': self.GPIO.input(JOY_DOWN),
        }
        
        # Detect button presses (transition from high to low)
        presses = {}
        for key, value in current.items():
            presses[key] = not value and self.last_states[key]
        
        # Update last states
        self.last_states = current
        
        return presses

