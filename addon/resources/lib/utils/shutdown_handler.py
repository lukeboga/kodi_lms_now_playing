import xbmc
from resources.lib.api.fetch_lms_status import requests_session  # Import the global requests session
from resources.lib.api.telnet_handler import telnet_handler  # Import the telnet handler instance
from resources.lib.utils.log_message import log_message  # Custom function for logging messages
from resources.lib.utils.constants import (
    LOG_LEVEL_INFO,
    LOG_LEVEL_ERROR,
    SHUTDOWN_MSG_START,
    SHUTDOWN_MSG_COMPLETE,
)

def shutdown_addon():
    """
    Handle the clean shutdown of the KLMS Addon.
    Close any open connections and clean up resources.
    """
    try:
        log_message(SHUTDOWN_MSG_START, LOG_LEVEL_INFO)
        
        # Close the requests session
        if requests_session:
            requests_session.close()
        
        # Close the telnet connection
        telnet_handler.close_telnet_connection()
        
        log_message(SHUTDOWN_MSG_COMPLETE, LOG_LEVEL_INFO)
    except Exception as e:
        log_message(f"Shutdown error: {e}", LOG_LEVEL_ERROR)

