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

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Purpose of the Module:**
   - This module defines constants used throughout the KLMS Addon to maintain consistency and avoid hardcoding values in multiple places.

2. **General Addon Information:**
   - `ADDON_ID`: The unique identifier for the addon.
   - `ADDON_NAME`: The name of the addon.
   - `ADDON_VERSION`: The version of the addon.
   - `PROVIDER_NAME`: The name of the provider.

3. **LMS Server Settings Keys:**
   - Keys used to retrieve LMS server settings from the configuration.

4. **Default LMS Server Settings:**
   - Default values for LMS server settings, used if not specified in the configuration.

5. **Log Levels:**
   - Constants for different log levels (INFO, WARNING, ERROR) to maintain consistent logging.

6. **Telnet Commands:**
   - Commands for subscribing and unsubscribing to LMS events via telnet.

7. **File Paths:**
   - Paths for default artwork and other resources.

8. **Debounce Time:**
   - Constant for the debounce time used in event processing.

9. **Socket Timeout:**
   - Constant for the timeout duration for socket connection attempts.

10. **JSON-RPC Request Details:**
    - Constants for constructing the JSON-RPC URL and payload templates.

11. **Content-Type Header:**
    - Constant for the Content-Type header used in HTTP requests.
"""

