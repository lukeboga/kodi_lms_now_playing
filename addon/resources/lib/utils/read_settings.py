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

