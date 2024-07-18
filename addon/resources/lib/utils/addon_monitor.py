import xbmc  # Kodi API module for logging and monitoring
from resources.lib.utils.log_message import log_message  # Custom function for logging messages
from resources.lib.api.telnet_handler import telnet_handler  # Import the telnet handler instance
from resources.lib.utils.read_settings import read_settings  # Import the settings reader function
from resources.lib.utils.constants import (
    LOG_LEVEL_INFO,
    LOG_LEVEL_ERROR,
    INIT_MSG_START,
    INIT_MSG_COMPLETE,
    ABORT_MSG
)
from resources.lib.utils.shutdown_handler import shutdown_addon  # Import the shutdown function

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
        try:
            log_message(INIT_MSG_START, LOG_LEVEL_INFO)
            self.settings = read_settings()
            # Add other initialization tasks here
            telnet_handler.start_telnet_subscriber()
            log_message(INIT_MSG_COMPLETE, LOG_LEVEL_INFO)
        except Exception as e:
            log_message(f"Initialization error: {e}", LOG_LEVEL_ERROR)

    def onAbortRequested(self):
        """
        Called when an abort (exit) request is made.
        This method handles cleanup tasks before the addon is exited.
        """
        log_message(ABORT_MSG, LOG_LEVEL_INFO)
        shutdown_addon()

