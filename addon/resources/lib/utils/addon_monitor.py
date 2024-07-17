import xbmc  # Kodi API module for logging and monitoring
from resources.lib.utils.log_message import log_message  # Custom function for logging messages
from resources.lib.api.fetch_lms_status import requests_session  # Import the global requests session
from resources.lib.api.telnet_handler import telnet_handler  # Import the telnet handler instance
from resources.lib.utils.read_settings import read_settings  # Import the settings reader function
from resources.lib.utils.constants import (
    LOG_LEVEL_INFO,
    INIT_MSG_START,
    INIT_MSG_COMPLETE,
    SHUTDOWN_MSG_START,
    SHUTDOWN_MSG_COMPLETE,
    ABORT_MSG
)

class AddonMonitor(xbmc.Monitor):
    """
    Custom monitor class to handle addon-specific events, including initialization and shutdown.
    """

    def __init__(self):
        super().__init__()
        self.settings = None
        self.initialize()

    def initialize(self):
        """
        Initialize the KLMS Addon.
        Load settings and establish necessary connections.
        """
        log_message(INIT_MSG_START, LOG_LEVEL_INFO)
        self.settings = read_settings()
        # Add other initialization tasks here
        telnet_handler.start_telnet_subscriber()
        log_message(INIT_MSG_COMPLETE, LOG_LEVEL_INFO)

    def onAbortRequested(self):
        """
        Called when an abort (exit) request is made.
        This method handles cleanup tasks before the addon is exited.
        """
        log_message(ABORT_MSG, LOG_LEVEL_INFO)
        self.shutdown()

    def shutdown(self):
        """
        Handle the clean shutdown of the KLMS Addon.
        Close any open connections and clean up resources.
        """
        log_message(SHUTDOWN_MSG_START, LOG_LEVEL_INFO)
        
        # Close the requests session
        if requests_session:
            requests_session.close()
        
        # Close the telnet connection
        telnet_handler.close_telnet_connection()
        
        log_message(SHUTDOWN_MSG_COMPLETE, LOG_LEVEL_INFO)

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for logging and monitoring.
   - `log_message`: A custom function to log messages to the Kodi log.
   - `requests_session`: The global requests session used for HTTP requests.
   - `telnet_handler`: The instance of the TelnetHandler class to manage the telnet connection.
   - `read_settings`: A function to read addon settings.
   - Constants imported from `constants.py`.

2. **AddonMonitor Class:**
   - **Purpose:** This class is designed to handle addon-specific events, particularly initialization and shutdown.

3. **__init__ Method:**
   - **Purpose:** This method initializes the class and starts the addon initialization process.
   - **Steps:**
     - Calls the `initialize` method to load settings and establish connections.

4. **initialize Method:**
   - **Purpose:** This method initializes the KLMS Addon by loading settings and establishing necessary connections.
   - **Steps:**
     - Logs that the initialization process has started.
     - Reads settings using the `read_settings` function.
     - Starts the telnet subscriber using `telnet_handler.start_telnet_subscriber()`.
     - Logs that the initialization process is complete.

5. **onAbortRequested Method:**
   - **Purpose:** This method is called when an abort (exit) request is made. It handles necessary cleanup tasks before the addon is fully exited.
   - **Steps:**
     - Logs that an abort request has been made and the addon is shutting down.
     - Calls the `shutdown` method to perform cleanup.

6. **shutdown Method:**
   - **Purpose:** This method handles the clean shutdown of the KLMS Addon by closing any open connections and cleaning up resources.
   - **Steps:**
     - Logs that the shutdown process has started.
     - Closes the requests session if it is open.
     - Closes the telnet connection using `telnet_handler.close_telnet_connection()`.
     - Logs that the shutdown process is complete.
"""

