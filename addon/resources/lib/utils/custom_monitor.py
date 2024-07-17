import xbmc  # Kodi API module for logging and monitoring
from resources.lib.utils.log_message import log_message  # Custom function for logging messages
from resources.lib.api.fetch_lms_status import requests_session  # Import the global requests session
from resources.lib.api.telnet_handler import close_telnet_connection  # Import the telnet close function

class AddonMonitor(xbmc.Monitor):
    """
    Custom monitor class to handle addon-specific events, including shutdown.
    """

    def onAbortRequested(self):
        """
        Called when an abort (exit) request is made.
        This method handles cleanup tasks before the addon is exited.
        """
        log_message("Abort requested. Shutting down KLMS Addon...", xbmc.LOGINFO)

        # Close the requests session
        if requests_session:
            requests_session.close()

        # Close the telnet connection
        close_telnet_connection()

        log_message("KLMS Addon shutdown complete.", xbmc.LOGINFO)

