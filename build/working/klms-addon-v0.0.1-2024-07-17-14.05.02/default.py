import xbmc
import xbmcaddon
from resources.lib.utils.log_message import log_message
from resources.lib.utils.initialization import initialize, on_shutdown
from resources.lib.ui.now_playing import NowPlaying
from resources.lib.utils.custom_monitor import AddonMonitor  # Import the custom monitor
from resources.lib.api.telnet_handler import start_telnet_subscriber, close_telnet_connection  # Import the telnet handler functions

def main():
    """
    Main entry point for the addon.
    This function determines the action to take based on the arguments passed to the script.
    """
    addon = xbmcaddon.Addon()
    window = NowPlaying("NowPlaying.xml", addon.getAddonInfo('path'))
    window.doModal()
    del window

if __name__ == '__main__':
    """
    Entry point of the script when run directly.
    This block ensures that initialization occurs before the main function is called,
    and that cleanup is performed after the main function completes.
    """
    try:
        # Initialize the addon, loading settings and establishing necessary connections
        initialize()
        # Create and initialize the custom monitor
        monitor = AddonMonitor()
        # Start the telnet subscriber
        start_telnet_subscriber()
        # Call the main function to execute the addon's primary functionality
        main()
        # Wait for abort (exit) request
        monitor.waitForAbort()
    except Exception as e:
        # Log any exceptions that occur during execution for debugging purposes
        log_message(f"Error in main: {e}", xbmc.LOGERROR)
    finally:
        # Ensure the addon shuts down cleanly, closing any open connections and cleaning up resources
        monitor.onAbortRequested()
        # Close the telnet connection
        close_telnet_connection()

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Purpose of the Script:**
   - This script serves as the main entry point for the KLMS Addon.

2. **Main Function (`main`):**
   - The `main` function is responsible for creating and displaying the `NowPlaying` window, which shows the 'now playing' information from the Logitech Media Server (LMS).

3. **Initialization Block (`if __name__ == '__main__'`):**
   - This block is executed when the script is run directly.
   - It initializes the addon, creates a custom monitor for handling events, starts the telnet subscriber for receiving LMS events, and calls the `main` function to display the `NowPlaying` window.
   - It also ensures that any resources are cleaned up properly when the addon is closed.

4. **Error Handling and Logging:**
   - The script includes error handling to log any exceptions that occur during execution, making it easier to debug issues.

5. **Clean Shutdown:**
   - The `finally` block ensures that the addon shuts down cleanly by calling the `onAbortRequested` method of the custom monitor and closing the telnet connection.
"""

