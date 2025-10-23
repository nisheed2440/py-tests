# MPC Quick Reference Guide

Quick reference for using MPC (Music Player Client) with your HiFi DAC HAT.

## Basic Playback Commands

```bash
# Start playback
mpc play

# Pause playback
mpc pause

# Toggle play/pause
mpc toggle

# Stop playback
mpc stop

# Play next track
mpc next

# Play previous track
mpc prev

# Seek forward 10 seconds
mpc seek +10

# Seek backward 10 seconds
mpc seek -10

# Seek to specific position (2 minutes 30 seconds)
mpc seek 2:30
```

## Volume Control

```bash
# Set volume to 50%
mpc volume 50

# Increase volume by 10%
mpc volume +10

# Decrease volume by 10%
mpc volume -10

# Show current volume
mpc volume
```

## Playlist Management

```bash
# Show current playlist
mpc playlist

# Clear playlist
mpc clear

# Add all music to playlist
mpc add /

# Add specific file or folder
mpc add "Artist/Album"
mpc add "Artist/Album/Song.mp3"

# Shuffle playlist
mpc shuffle

# Remove track 5 from playlist
mpc del 5

# Play specific track number
mpc play 3

# Move track 2 to position 5
mpc move 2 5
```

## Information & Status

```bash
# Show current playing track
mpc current

# Show detailed status (playing/paused, time, etc.)
mpc status

# Show statistics (total songs, artists, albums, etc.)
mpc stats

# List all music files
mpc listall

# Show version information
mpc version
```

## Search Commands

```bash
# Search by artist
mpc search artist "Artist Name"

# Search by album
mpc search album "Album Name"

# Search by song title
mpc search title "Song Title"

# Search by genre
mpc search genre "Rock"

# Find exact matches (case-sensitive)
mpc find artist "Artist Name"
```

## Database Management

```bash
# Update music database (scan for new files)
mpc update

# Force complete database rescan
mpc rescan

# Wait for database update to finish
mpc idle update
```

## Playback Modes

```bash
# Enable repeat mode
mpc repeat on

# Disable repeat mode
mpc repeat off

# Enable random/shuffle mode
mpc random on

# Disable random mode
mpc random off

# Enable single mode (stop after current song)
mpc single on

# Disable single mode
mpc single off

# Enable consume mode (remove songs after playing)
mpc consume on

# Disable consume mode
mpc consume off
```

## Playlist Saving & Loading

```bash
# Save current playlist
mpc save "My Playlist"

# Load a saved playlist
mpc load "My Playlist"

# Delete a saved playlist
mpc rm "My Playlist"

# List all saved playlists
mpc lsplaylists
```

## Output Control

```bash
# List available outputs
mpc outputs

# Enable output 1
mpc enable 1

# Disable output 1
mpc disable 1

# Toggle output 1
mpc toggleoutput 1
```

## Advanced Usage

```bash
# Play tracks by specific artist
mpc clear
mpc search artist "Artist Name" | mpc add
mpc play

# Create a genre-based playlist
mpc clear
mpc search genre "Jazz" | mpc add
mpc shuffle
mpc play

# Queue a song after current track
mpc insert "Artist/Album/Song.mp3"

# Show current queue with formatting
mpc playlist --format "[%artist% - %title%]|[%file%]"

# Get current track filename
mpc current -f %file%

# Get current track position and total time
mpc status | grep -o "[0-9]*:[0-9]*/[0-9]*:[0-9]*"
```

## Scripting Examples

### Create a Simple Alarm Clock

```bash
#!/bin/bash
# alarm.sh - Start music at specific time

# Wait until 7:00 AM
while [ $(date +%H:%M) != "07:00" ]; do
    sleep 30
done

# Start playback
mpc clear
mpc add /
mpc shuffle
mpc volume 30
mpc play
```

### Random Album Playback

```bash
#!/bin/bash
# random_album.sh - Play a random album

# Get random album
ALBUM=$(mpc list album | shuf -n 1)

# Play it
mpc clear
mpc search album "$ALBUM" | mpc add
mpc play

echo "Now playing: $ALBUM"
```

### Now Playing Display

```bash
#!/bin/bash
# nowplaying.sh - Continuously display current track

watch -n 1 'mpc current -f "♫ %artist% - %title%\n   Album: %album% (%date%)"'
```

## Keyboard Shortcuts (for scripts)

You can create a script to control MPD with keyboard shortcuts:

```bash
#!/bin/bash
# mpd_control.sh

case "$1" in
    play)     mpc toggle ;;
    next)     mpc next ;;
    prev)     mpc prev ;;
    stop)     mpc stop ;;
    volup)    mpc volume +5 ;;
    voldown)  mpc volume -5 ;;
    *)        echo "Usage: $0 {play|next|prev|stop|volup|voldown}" ;;
esac
```

## Troubleshooting Commands

```bash
# Check if MPD is running
systemctl status mpd

# Restart MPD service
sudo systemctl restart mpd

# Check MPD logs
sudo journalctl -u mpd -n 50

# Test connection to MPD
mpc status

# Check music directory permissions
ls -la ~/Music

# Verify audio output device
aplay -l

# Test audio playback
speaker-test -D hw:0,0 -c 2
```

## Format Specifiers

When using `-f` or `--format` with `mpc current` or `mpc playlist`:

```
%artist%      - Artist name
%album%       - Album name
%title%       - Song title
%track%       - Track number
%name%        - Stream name
%genre%       - Genre
%date%        - Release date
%composer%    - Composer
%performer%   - Performer
%comment%     - Comment
%disc%        - Disc number
%file%        - File path
%time%        - Duration (MM:SS)
%position%    - Position in playlist
```

Example:
```bash
mpc current -f "Now playing: %artist% - %title% from %album% (%date%)"
```

## Useful Aliases

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# MPC shortcuts
alias play='mpc toggle'
alias next='mpc next'
alias prev='mpc prev'
alias stop='mpc stop'
alias volup='mpc volume +5'
alias voldown='mpc volume -5'
alias np='mpc current'
alias addall='mpc clear && mpc add / && mpc shuffle'
```

## Tips

1. **Tab Completion**: Use tab completion for file/folder names
2. **Pipe Commands**: Combine commands with pipes for powerful operations
3. **Background Playback**: MPD runs as a daemon, so music continues even if you log out
4. **Multiple Clients**: Multiple devices can control the same MPD instance
5. **Network Streaming**: Enable HTTP output in MPD to stream to other devices

## Getting Help

```bash
# Show all MPC commands
mpc help

# Show MPD manual
man mpd

# Show MPC manual
man mpc

# Check MPD configuration
cat /etc/mpd.conf
```

## Related Resources

- [MPD Documentation](https://www.musicpd.org/doc/html/)
- [MPC Manual Page](https://www.musicpd.org/clients/mpc/)
- [MPD Wiki](https://mpd.fandom.com/wiki/Music_Player_Daemon_Wiki)
- [MPD Forum](https://forum.musicpd.org/)

