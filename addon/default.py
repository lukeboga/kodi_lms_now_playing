import xbmc
import xbmcaddon
from resources.lib.utils.log_message import log_message
from resources.lib.ui.now_playing import NowPlaying
from resources.lib.utils.addon_monitor import AddonMonitor
from resources.lib.utils.shutdown_handler import shutdown_addon  # Import the shutdown function
from resources.lib.utils.constants import (
    LOG_LEVEL_ERROR,
    NOW_PLAYING_XML,
    LOG_MSG_FORMAT,
    ADDON_NAME
)

def main():
    """
    Main entry point for the addon.
    This function determines the action to take based on the arguments passed to the script.
    """
    addon = xbmcaddon.Addon()
    window = NowPlaying(NOW_PLAYING_XML, addon.getAddonInfo('path'))
    window.doModal()
    del window

def run_addon():
    """
    Initialize the addon, run the main functionality, and handle shutdown.
    """
    monitor = AddonMonitor()
    try:
        # Call the main function to execute the addon's primary functionality
        main()
        # Wait for abort (exit) request
        monitor.waitForAbort()
    except Exception as e:
        # Log any exceptions that occur during execution for debugging purposes
        log_message(f"Error in run_addon: {e}", LOG_LEVEL_ERROR)
    finally:
        # Ensure the addon shuts down cleanly, closing any open connections and cleaning up resources
        shutdown_addon()

if __name__ == '__main__':
    """
    Entry point of the script when run directly.
    This block ensures that initialization occurs before the main function is called,
    and that cleanup is performed after the main function completes.
    """
    run_addon()

