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

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for logging.
   - `log_message`: A custom function to log messages to the Kodi log.
   - `requests_session`: The global requests session used for HTTP requests.
   - `read_settings`: A function to read addon settings.

2. **initialize Function:**
   - **Purpose:** This function initializes the KLMS Addon by loading settings and establishing necessary connections.
   
   - **Steps:**
     - Logs that the initialization process has started.
     - Reads settings using the `read_settings` function.
     - Logs that the initialization process is complete.
   
   - **Detailed Steps:**
     - `log_message("Initializing KLMS Addon...", xbmc.LOGINFO)`: Logs the message indicating the start of initialization.
     - `settings = read_settings()`: Reads the settings and stores them in the `settings` variable.
     - `log_message("Initialization complete.", xbmc.LOGINFO)`: Logs the message indicating that initialization is complete.

3. **on_shutdown Function:**
   - **Purpose:** This function handles the clean shutdown of the KLMS Addon by closing any open connections and cleaning up resources.
   
   - **Steps:**
     - Logs that the shutdown process has started.
     - Closes the requests session if it is open.
     - Logs that the shutdown process is complete.
   
   - **Detailed Steps:**
     - `log_message("Shutting down KLMS Addon.", xbmc.LOGINFO)`: Logs the message indicating the start of shutdown.
     - `if requests_session: requests_session.close()`: Checks if the requests session is open and closes it.
     - `log_message("Shutdown complete.", xbmc.LOGINFO)`: Logs the message indicating that shutdown is complete.
"""

