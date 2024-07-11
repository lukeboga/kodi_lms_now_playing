# Changelog

## 2024-07-11 08:31:29
- Added addon.xml: Define core metadata for the KLMS Addon
- Added default.py: Main script for handling addon core functionality
- Added nowplaying.xml: Define static UI layout for 'now playing' window
- Added lms_api.py: Handle interactions with LMS API
- Added player.py: Provide playback control functions
- Added format_time.py: Utility function to format time
- Added log_message.py: Utility function for logging messages
- Added read_settings.py: Utility function to read addon settings
- Added validate_ip.py: Utility function to validate IP address format

## 2024-07-11 11:01:07
- Updated addon.xml: Add script.module.requests dependency for LMS API requests
- Added settings.xml: Define LMS configuration options with defaults

## 2024-07-11 13:00:12
- Updated fetch_now_playing.py: Replace xbmc.log with log_message
- Updated log_now_playing.py: Replace xbmc.log with log_message
- Updated player.py: Replace xbmc.log with log_message
- Updated read_settings.py: Replace xbmc.log with log_message
- Updated validate_ip.py: Replace xbmc.log with log_message
- Updated default.py: Replace xbmc.log with log_message
- Updated format_time.py: Replace xbmc.log with log_message
- Updated log_message.py: Include '[KLMS Addon]' prefix

## 2024-07-11 13:25:51
- Fixed default.py: Use InfoTagMusic for setting music properties to address deprecation warning

## 2024-07-11 14:14:41
- Fixed default.py: Ensure xbmc is imported

## 2024-07-11 14:47:18
- Fixed default.py: Ensure correct player (PAPlayer) is explicitly used for audio playback
- Fixed player.py: Ensure correct player (PAPlayer) is explicitly used for playback control
