# Import necessary modules from the Kodi API and the custom libraries
import xbmcplugin
import xbmcgui
import sys
import xbmc
from resources.lib.ui.ui import list_items
from resources.lib.player import player
from resources.lib.utils.log_message import log_message
from resources.lib.utils.initialization import initialize, on_shutdown

def main():
    """
    Main entry point for the addon.
    """
    handle = int(sys.argv[1])
    action = sys.argv[2] if len(sys.argv) > 2 else None

    if action == 'play':
        player.play()
    else:
        list_items(handle)

if __name__ == '__main__':
    try:
        initialize()
        main()
    except Exception as e:
        log_message(f"Error in main: {e}", xbmc.LOGERROR)
    finally:
        on_shutdown()

