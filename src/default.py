# Import necessary modules from the Kodi API and the custom libraries
import xbmc
import xbmcplugin
import xbmcgui
import sys
from resources.lib.api.fetch_now_playing import get_now_playing
from resources.lib.api.log_now_playing import log_now_playing
from resources.lib.player import player
from resources.lib.utils.log_message import log_message

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
    now_playing = get_now_playing()
    if now_playing:
        # Create a list item with the 'now playing' title
        li = xbmcgui.ListItem(now_playing['title'])
        
        # Create an InfoTagMusic object and set music properties
        info_tag = li.getMusicInfoTag()
        info_tag.setTitle(now_playing['title'])
        info_tag.setArtist(now_playing['artist'])
        info_tag.setAlbum(now_playing['album'])
        
        # Add the list item to the directory
        xbmcplugin.addDirectoryItem(handle, '', li, False)
        # Log the displayed information
        log_now_playing(now_playing)
    else:
        log_message("No 'now playing' information available.", xbmc.LOGWARNING)
    # End the directory listing
    xbmcplugin.endOfDirectory(handle)

def play_audio_file(handle, url, title):
    """
    Play an audio file using the PAPlayer.
    
    Parameters:
        handle (int): The unique identifier for the plugin instance.
        url (str): The URL of the audio file to play.
        title (str): The title of the audio file.
    """
    # Create a list item with the provided title
    li = xbmcgui.ListItem(title)
    
    # Set the path for the list item to the URL of the audio file
    li.setPath(url)
    
    # Set the info type to 'music' to ensure the correct player is used
    li.setInfo('music', {'title': title})
    
    # Play the item using the PAPlayer
    xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(url, li)

# If this script is executed directly, call the main function
if __name__ == '__main__':
    main()

