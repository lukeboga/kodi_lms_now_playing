import xbmc
import xbmcaddon
from resources.lib.utils.log_message import log_message
from resources.lib.utils.initialization import initialize, on_shutdown 
from resources.lib.ui.now_playing import NowPlaying

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
        # Call the main function to execute the addon's primary functionality
        main()
    except Exception as e:
        # Log any exceptions that occur during execution for debugging purposes
        log_message(f"Error in main: {e}", xbmc.LOGERROR)
    finally:
        # Ensure the addon shuts down cleanly, closing any open connections and cleaning up resources
        on_shutdown()

