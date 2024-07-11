# Import necessary modules from the Kodi API and the custom libraries
import xbmc
import xbmcplugin
import xbmcgui
import sys
from resources.lib.api import lms_api
from resources.lib.player import player
from resources.lib.utils.log_message import log_message
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.validate_ip import validate_ip
from resources.lib.utils.format_time import format_time

# Main entry point for the addon
def main():
    """
    The main function serves as the entry point for the addon.
    It parses arguments passed to the script, determines the action to take, and executes the appropriate function.
    """
    # Handle is a unique identifier for the plugin instance
    handle = int(sys.argv[1])
    # Action specifies the operation to perform (e.g., 'play')
    action = sys.argv[2] if len(sys.argv) > 2 else None

    # Check the action and call the appropriate function
    if action == 'play':
        player.play()
    else:
        # If no specific action is provided, display the 'now playing' information
        list_items(handle)

# Function to display 'now playing' information
def list_items(handle):
    """
    Lists the 'now playing' information in the Kodi interface.
    
    Parameters:
        handle (int): The unique identifier for the plugin instance.
    """
    # Retrieve the current 'now playing' information from LMS
    now_playing = lms_api.get_now_playing()
    if now_playing:
        # Create a list item with the 'now playing' title
        li = xbmcgui.ListItem(now_playing['title'])
        # Set additional information for the list item (e.g., artist, album)
        li.setInfo('music', {'title': now_playing['title'], 'artist': now_playing['artist'], 'album': now_playing['album']})
        # Add the list item to the directory
        xbmcplugin.addDirectoryItem(handle, '', li, False)
        # Log the displayed information
        log_message(f"Displayed Now Playing: {now_playing['title']} by {now_playing['artist']} from the album {now_playing['album']}")
    else:
        log_message("No 'now playing' information available.", xbmc.LOGWARNING)
    # End the directory listing
    xbmcplugin.endOfDirectory(handle)

# If this script is executed directly, call the main function
if __name__ == '__main__':
    main()

