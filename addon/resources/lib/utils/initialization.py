import xbmc  # Kodi API module for logging
from resources.lib.utils.log_message import log_message
from resources.lib.api.fetch_lms_status import requests_session
from resources.lib.utils.read_settings import read_settings

def initialize():
    """
    Initialize the KLMS Addon.
    Load settings and establish necessary connections.
    """
    log_message("Initializing KLMS Addon...", xbmc.LOGINFO)
    settings = read_settings()
    # Add any other initialization steps here
    log_message("Initialization complete.", xbmc.LOGINFO)

def on_shutdown():
    """
    Handle the clean shutdown of the KLMS Addon.
    Close any open connections and clean up resources.
    """
    log_message("Shutting down KLMS Addon.", xbmc.LOGINFO)

    # Close the requests session
    if requests_session:
        requests_session.close()

    log_message("Shutdown complete.", xbmc.LOGINFO)

