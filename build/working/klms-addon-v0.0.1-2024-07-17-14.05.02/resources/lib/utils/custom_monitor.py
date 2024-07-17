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


"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for logging and monitoring.
   - `log_message`: A custom function to log messages to the Kodi log.
   - `requests_session`: The global requests session used for HTTP requests.
   - `close_telnet_connection`: A function to close the telnet connection.

2. **AddonMonitor Class:**
   - **Purpose:** This class is designed to handle addon-specific events, particularly the shutdown process.

3. **onAbortRequested Method:**
   - **Purpose:** This method is called when an abort (exit) request is made. It handles necessary cleanup tasks before the addon is fully exited.
   
   - **Steps:**
     - Logs that an abort request has been made and the addon is shutting down.
     - Closes the requests session if it is open.
     - Closes the telnet connection.
     - Logs that the addon shutdown is complete.
   
   - **Detailed Steps:**
     - `log_message("Abort requested. Shutting down KLMS Addon...", xbmc.LOGINFO)`: Logs the message indicating an abort request.
     - `if requests_session: requests_session.close()`: Checks if the requests session is open and closes it.
     - `close_telnet_connection()`: Calls the function to close the telnet connection.
     - `log_message("KLMS Addon shutdown complete.", xbmc.LOGINFO)`: Logs the message indicating the shutdown is complete.
"""

