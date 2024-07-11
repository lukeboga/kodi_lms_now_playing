import xbmc
import xbmcaddon

def read_settings():
    """
    Read and return the addon's settings from the Kodi configuration.
    
    Returns:
        dict: A dictionary containing the addon settings.
    """
    try:
        addon = xbmcaddon.Addon()
        settings = {
            'lms_server': addon.getSetting('lms_server'),
            'lms_port': addon.getSetting('lms_port'),
            'lms_player_id': addon.getSetting('lms_player_id')
        }
        return settings
    except Exception as e:
        # Log any errors encountered during settings retrieval
        xbmc.log(f"KLMS Addon: Error reading settings: {e}", level=xbmc.LOGERROR)
        return {}

