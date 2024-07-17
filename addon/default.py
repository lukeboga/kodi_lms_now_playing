import xbmc
import xbmcaddon
from resources.lib.utils.log_message import log_message
from resources.lib.utils.initialization import initialize
from resources.lib.ui.now_playing import NowPlaying
from resources.lib.utils.custom_monitor import AddonMonitor  # Import the custom monitor
from resources.lib.api.telnet_handler import start_telnet_subscriber  # Import the telnet subscriber

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

