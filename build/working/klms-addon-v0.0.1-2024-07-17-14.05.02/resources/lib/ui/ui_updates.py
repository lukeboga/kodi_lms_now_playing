import xbmc
import xbmcgui
from resources.lib.api.get_now_playing import get_now_playing
from resources.lib.api.get_playlist import get_playlist
from resources.lib.utils.log_message import log_message

def update_now_playing(window, lms_data):
    """
    Update the 'now playing' UI elements with the current track's information.
    
    Args:
        window (xbmcgui.WindowXML): The window object containing the UI elements.
        lms_data (dict): The LMS data to use for updating the UI.
    """
    now_playing_data = get_now_playing(lms_data)
    
    if now_playing_data:
        # Update the labels with the now playing data
        window.getControl(3).setLabel(now_playing_data['title'])
        window.getControl(4).setLabel(now_playing_data['album'])
        window.getControl(5).setLabel(now_playing_data['artist'])

        # Update the artwork images
        artwork_url = now_playing_data.get('artwork_url', 'special://home/addons/plugin.program.klmsaddon/resources/media/demo-cover.jpg')
        window.getControl(1).setImage(artwork_url)
        window.getControl(2).setImage(artwork_url)
    else:
        log_message("No 'now playing' information available.", xbmc.LOGWARNING)
        # Clear the labels if no data is available
        window.getControl(3).setLabel("")
        window.getControl(4).setLabel("")
        window.getControl(5).setLabel("")
        # Set default artwork
        default_artwork = 'special://home/addons/plugin.program.klmsaddon/resources/media/demo-cover.jpg'
        window.getControl(1).setImage(default_artwork)
        window.getControl(2).setImage(default_artwork)

def update_playlist(window, lms_data):
    """
    Update the playlist UI element with the current playlist's information.
    
    Args:
        window (xbmcgui.WindowXML): The window object containing the UI elements.
        lms_data (dict): The LMS data to use for updating the UI.
    """
    playlist_data = get_playlist(lms_data)
    
    if playlist_data:
        # Update playlist items
        playlist_control = window.getControl(6)
        playlist_control.reset()
        
        for index, item in enumerate(playlist_data):
            li = xbmcgui.ListItem(label=item['title'])
            li.setProperty("id", str(100 + index))
            info_tag = li.getMusicInfoTag()
            info_tag.setAlbum(item['album'])
            info_tag.setArtist(item['artist'])
            
            playlist_control.addItem(li)
    else:
        log_message("No 'now playing' information available.", xbmc.LOGWARNING)

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`, `xbmcgui`: Part of the Kodi API, used for various Kodi functionalities.
   - `get_now_playing`, `get_playlist`: Custom utility functions for getting now playing and playlist data.
   - `log_message`: Custom function for logging messages.

2. **update_now_playing Function:**
   - **Purpose:** Updates the 'now playing' UI elements with the current track's information.
   - **Args:** 
     - `window (xbmcgui.WindowXML)`: The window object containing the UI elements.
     - `lms_data (dict)`: The LMS data to use for updating the UI.
   - **Steps:**
     - Gets the now playing data using the `get_now_playing` function.
     - Updates the UI elements (title, album, artist, artwork) with the now playing data.
     - If no data is available, clears the UI elements and sets default artwork.

3. **update_playlist Function:**
   - **Purpose:** Updates the playlist UI element with the current playlist's information.
   - **Args:** 
     - `window (xbmcgui.WindowXML)`: The window object containing the UI elements.
     - `lms_data (dict)`: The LMS data to use for updating the UI.
   - **Steps:**
     - Gets the playlist data using the `get_playlist` function.
     - Updates the playlist control with the playlist items.
     - If no data is available, logs a message.

"""

