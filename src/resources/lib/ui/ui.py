# Import necessary modules from the Kodi API and the custom libraries
import xbmcgui  # Module for creating GUI elements in Kodi
import xbmcplugin  # Module for managing plugin behavior in Kodi
import xbmc  # Module for Kodi logging and other functionalities
from resources.lib.api.fetch_now_playing import get_now_playing  # Custom function to fetch 'now playing' data from LMS
from resources.lib.api.log_now_playing import log_now_playing  # Custom function to log 'now playing' data
from resources.lib.utils.log_message import log_message  # Custom function for logging messages

def list_items(handle):
    """
    Lists the 'now playing' information in the Kodi interface.
    
    Parameters:
        handle (int): The unique identifier for the plugin instance.
    """
    # Fetch the current 'now playing' information from LMS
    now_playing = get_now_playing()
    
    # Check if 'now playing' data is available
    if now_playing:
        # Create a new ListItem object with the title of the currently playing track
        li = xbmcgui.ListItem('Hello, World!')
        
        # Add the ListItem to the directory
        # addDirectoryItem(handle, url, listitem, isFolder) adds a list item to the directory
        xbmcplugin.addDirectoryItem(handle, '', li, False)
        
        # Log the 'now playing' information for debugging and monitoring purposes
        log_now_playing(now_playing)
    else:
        # Log a warning message if no 'now playing' information is available
        log_message("No 'now playing' information available.", xbmc.LOGWARNING)
    
    # End the directory listing process
    # endOfDirectory(handle) signals that the directory listing is complete
    xbmcplugin.endOfDirectory(handle)

