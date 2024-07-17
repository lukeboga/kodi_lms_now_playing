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

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Purpose of the Script:**
   - This script serves as the main entry point for the KLMS Addon.

2. **Main Function (`main`):**
   - The `main` function is responsible for creating and displaying the `NowPlaying` window, which shows the 'now playing' information from the Logitech Media Server (LMS).

3. **Run Addon Function (`run_addon`):**
   - This function handles the initialization, running, and cleanup of the addon.
   - It initializes the addon by creating an `AddonMonitor` instance, which also starts the telnet subscriber for receiving LMS events, and calls the `main` function to display the `NowPlaying` window.
   - It waits for the abort request and ensures that any resources are cleaned up properly when the addon is closed.

4. **Initialization Block (`if __name__ == '__main__'`):**
   - This block is executed when the script is run directly.
   - It calls the `run_addon` function to handle the complete lifecycle of the addon.

5. **Error Handling and Logging:**
   - The script includes error handling to log any exceptions that occur during execution, making it easier to debug issues.

6. **Clean Shutdown:**
   - The `finally` block in the `run_addon` function ensures that the addon shuts down cleanly by calling the `shutdown_addon` function.
"""
