#!/usr/bin/env python3
"""
Main application entry point with modular test selection
"""

import sys
import argparse


def run_lcd_test():
    """Run the LCD hardware test"""
    from modules.lcd import run_test
    print("=" * 50)
    print("Starting LCD Test")
    print("=" * 50)
    run_test()


def run_music_player():
    """Run the music player UI"""
    from modules.music_player import run_player
    print("=" * 50)
    print("Starting Music Player")
    print("=" * 50)
    run_player()


def list_tests():
    """Display available tests"""
    print("\nAvailable tests:")
    print("  lcd          - Test the 1.3inch LCD HAT (ST7789)")
    print("  music        - Run the music player UI")
    print("\nUsage examples:")
    print("  python app.py lcd")
    print("  python app.py music")
    print("  python app.py --list")


def main():
    parser = argparse.ArgumentParser(
        description='Raspberry Pi Project Test Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app.py lcd           Run LCD hardware test
  python app.py music         Run music player
  python app.py --list        Show all available tests
        """
    )
    
    parser.add_argument(
        'test',
        nargs='?',
        choices=['lcd', 'music'],
        help='Test module to run'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available tests'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_tests()
        return
    
    if not args.test:
        parser.print_help()
        print()
        list_tests()
        return
    
    try:
        if args.test == 'lcd':
            run_lcd_test()
        elif args.test == 'music':
            run_music_player()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
    except ImportError as e:
        print(f"\nError: Missing dependencies - {e}")
        print("Make sure you're running on Raspberry Pi with required hardware")
        sys.exit(1)
    except Exception as e:
        print(f"\nError running test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

