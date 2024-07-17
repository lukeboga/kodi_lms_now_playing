# Import necessary modules from the Kodi API
import xbmc
import xbmcaddon
from resources.lib.utils.log_message import log_message
from resources.lib.utils.constants import (
    ADDON_SETTING_LMS_SERVER,
    ADDON_SETTING_LMS_PORT,
    ADDON_SETTING_LMS_PLAYER_ID,
    ADDON_SETTING_LMS_TELNET_PORT,
    SETTINGS_ERROR_MSG,
    LOG_LEVEL_ERROR
)

def read_settings():
    """
    Read and return the addon's settings from the Kodi configuration.
    
    This function retrieves settings such as LMS server address, port, and player ID from the Kodi addon settings.
    
    Returns:
        dict: A dictionary containing the addon settings.
    """
    try:
        # Retrieve the addon instance
        addon = xbmcaddon.Addon()
        # Read settings from the addon configuration
        settings = {
            ADDON_SETTING_LMS_SERVER: addon.getSetting(ADDON_SETTING_LMS_SERVER),
            ADDON_SETTING_LMS_PORT: addon.getSetting(ADDON_SETTING_LMS_PORT),
            ADDON_SETTING_LMS_PLAYER_ID: addon.getSetting(ADDON_SETTING_LMS_PLAYER_ID),
            ADDON_SETTING_LMS_TELNET_PORT: addon.getSetting(ADDON_SETTING_LMS_TELNET_PORT)
        }
        return settings
    except Exception as e:
        # Log any errors encountered during settings retrieval
        log_message(SETTINGS_ERROR_MSG.format(error=e), LOG_LEVEL_ERROR)
        return {}

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc` and `xbmcaddon` are part of the Kodi API. They provide functionalities to interact with Kodi.
   - `log_message` is a custom function defined in another module to log messages.
   - Constants imported from `constants.py`.

2. **read_settings Function:**
   - **Purpose:** This function reads and returns the addon's settings from Kodi's configuration.
   
   - **Steps:**
     - The function tries to retrieve settings such as LMS server address, port, player ID, and telnet port from Kodi's addon settings.
     - If successful, it returns these settings as a dictionary.
     - If an error occurs, it logs the error message and returns an empty dictionary.
   
   - **Detailed Steps:**
     - `addon = xbmcaddon.Addon()`: This line gets the current instance of the addon, allowing access to its settings.
     - `settings = { ... }`: This block reads specific settings using `addon.getSetting('setting_id')` and stores them in a dictionary.
     - `return settings`: Returns the dictionary containing the settings.
     - `except Exception as e`: If any error occurs during this process, it is caught and handled here.
     - `log_message(SETTINGS_ERROR_MSG.format(error=e), LOG_LEVEL_ERROR)`: Logs the error message.
     - `return {}`: Returns an empty dictionary if an error occurs.
"""

