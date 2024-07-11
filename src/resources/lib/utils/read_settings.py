# Import necessary modules from the Kodi API
import xbmc
import xbmcaddon
from resources.lib.utils.log_message import log_message

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
            'lms_server': addon.getSetting('lms_server'),
            'lms_port': addon.getSetting('lms_port'),
            'lms_player_id': addon.getSetting('lms_player_id')
        }
        return settings
    except Exception as e:
        # Log any errors encountered during settings retrieval
        log_message(f"Error reading settings: {e}", xbmc.LOGERROR)
        return {}

