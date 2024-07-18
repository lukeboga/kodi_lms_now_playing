import xbmc

"""
This module defines constants used throughout the KLMS Addon.
"""

# General Addon Information
ADDON_ID = "plugin.program.klmsaddon"
ADDON_NAME = "KLMS Addon"
ADDON_VERSION = "0.0.1"
PROVIDER_NAME = "LukeBM"

# LMS Server Settings Keys
LMS_SERVER_KEY = "lms_server"
LMS_PORT_KEY = "lms_port"
LMS_PLAYER_ID_KEY = "lms_player_id"
LMS_TELNET_PORT_KEY = "lms_telnet_port"

# Default LMS Server Settings
DEFAULT_LMS_SERVER = "192.168.1.201"
DEFAULT_LMS_PORT = 9000
DEFAULT_LMS_PLAYER_ID = "ab:7a:56:8b:fd:0f"
DEFAULT_LMS_TELNET_PORT = 59090

# Log Levels
LOG_LEVEL_INFO = xbmc.LOGINFO
LOG_LEVEL_WARNING = xbmc.LOGWARNING
LOG_LEVEL_ERROR = xbmc.LOGERROR

# Telnet Commands
TELNET_SUBSCRIBE_COMMAND = b"subscribe playlist\n"
TELNET_UNSUBSCRIBE_COMMAND = b"subscribe 0\n"

# File Paths
DEFAULT_ARTWORK_PATH = "special://home/addons/plugin.program.klmsaddon/resources/media/demo-cover.jpg"

# Debounce time in seconds
DEBOUNCE_TIME = 1.0

# Timeout in seconds for socket connection attempts
SOCKET_TIMEOUT = 2

# JSON-RPC Request Details
JSON_RPC_URL_TEMPLATE = "http://{server}:{port}/jsonrpc.js"
JSON_RPC_PAYLOAD_TEMPLATE = {
    "method": "slim.request",
    "params": None,  # To be filled dynamically
    "id": 1
}

# Content-Type Header
CONTENT_TYPE_HEADER = {"Content-Type": "application/json"}

# LMS JSON Keys
LMS_RESULT_KEY = "result"
LMS_PLAYLIST_LOOP_KEY = "playlist_loop"
LMS_TIME_KEY = "time"

# Connection Retry Interval in seconds
RETRY_INTERVAL = 5

# Control IDs for UI elements
CONTROL_ID_ARTWORK_BACKGROUND = 1
CONTROL_ID_ARTWORK = 2
CONTROL_ID_NOW_PLAYING_TITLE = 3
CONTROL_ID_NOW_PLAYING_ALBUM = 4
CONTROL_ID_NOW_PLAYING_ARTIST = 5
CONTROL_ID_PLAYLIST = 6

# Playlist ListItem Property ID Prefix
LISTITEM_ID_PREFIX = 100

# Initialization and Shutdown Messages
INIT_MSG_START = "Initializing KLMS Addon..."
INIT_MSG_COMPLETE = "Initialization complete."
SHUTDOWN_MSG_START = "Shutting down KLMS Addon."
SHUTDOWN_MSG_COMPLETE = "Shutdown complete."
ABORT_MSG = "Abort requested. Shutting down KLMS Addon..."

# Exception Logging Messages
EXCEPTION_LOG_MSG = "[KLMS Addon] Exception: {exc}"
TRACEBACK_LOG_MSG = "[KLMS Addon] Traceback: {traceback}"

# Log Message Format
LOG_MSG_FORMAT = "[KLMS Addon] {filename}:{lineno} - {message}"
LOG_ERROR_MSG_FORMAT = "[KLMS Addon] [Error] {error}"

# Network Constants
RETRY_COUNT = 3
BACKOFF_FACTOR = 0.3
STATUS_FORCE_LIST = (500, 502, 504)
SOCKET_TIMEOUT = 2

# Network Issue Logging Message
NETWORK_ISSUE_LOG_MSG = "Network issue: {message}"

# Addon Settings Keys
ADDON_SETTING_LMS_SERVER = "lms_server"
ADDON_SETTING_LMS_PORT = "lms_port"
ADDON_SETTING_LMS_PLAYER_ID = "lms_player_id"
ADDON_SETTING_LMS_TELNET_PORT = "lms_telnet_port"

# Settings Error Message
SETTINGS_ERROR_MSG = "Error reading settings: {error}"

# NowPlaying Window Filename
NOW_PLAYING_XML = "NowPlaying.xml"

