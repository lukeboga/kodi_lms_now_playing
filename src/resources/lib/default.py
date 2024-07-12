# Import necessary modules from the Kodi API and the custom libraries
import xbmcplugin  # Module for managing plugin behavior in Kodi
import xbmcgui  # Module for creating GUI elements in Kodi
import sys  # Module for interacting with the Python runtime environment
import xbmc  # Module for Kodi logging and other functionalities
import xbmcaddon
from resources.lib.ui.ui import list_items  # Custom function to list 'now playing' items
from resources.lib.player import player  # Custom player control functions
from resources.lib.utils.log_message import log_message  # Custom function for logging messages
from resources.lib.utils.initialization import initialize, on_shutdown  # Custom functions for initialization and shutdown
from resources.lib.ui.hello_world import HelloWorldWindow

def main():
    """
    Main entry point for the addon.
    This function determines the action to take based on the arguments passed to the script.
    """
    addon = xbmcaddon.Addon()
    window = HelloWorldWindow("HelloWorld.xml", addon.getAddonInfo('path'))
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
        # Call the main function to execute the addon's primary functionality
        main()
    except Exception as e:
        # Log any exceptions that occur during execution for debugging purposes
        log_message(f"Error in main: {e}", xbmc.LOGERROR)
    finally:
        # Ensure the addon shuts down cleanly, closing any open connections and cleaning up resources
        on_shutdown()

