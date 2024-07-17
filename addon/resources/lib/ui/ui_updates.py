import xbmc
import xbmcgui
from resources.lib.api.lms_data_processing import get_now_playing, get_playlist
from resources.lib.utils.log_message import log_message
from resources.lib.utils.constants import (
    LOG_LEVEL_WARNING,
    CONTROL_ID_ARTWORK_BACKGROUND,
    CONTROL_ID_ARTWORK,
    CONTROL_ID_NOW_PLAYING_TITLE,
    CONTROL_ID_NOW_PLAYING_ALBUM,
    CONTROL_ID_NOW_PLAYING_ARTIST,
    CONTROL_ID_PLAYLIST,
    DEFAULT_ARTWORK_PATH,
    LISTITEM_ID_PREFIX
)

def update_now_playing(window, lms_data):
    """
    Update the 'now playing' UI elements with the current track's information.
    
    Args:
        window (xbmcgui.WindowXML): The window object containing the UI elements.
        lms_data (dict): The LMS data to use for updating the UI.
    """
    now_playing_data = get_now_playing(lms_data)
    
    if now_playing_data:
        set_now_playing_labels(window, now_playing_data)
        set_now_playing_artwork(window, now_playing_data['artwork_url'])
    else:
        log_message("No 'now playing' information available.", LOG_LEVEL_WARNING)
        clear_now_playing_labels(window)
        set_default_artwork(window)

def update_playlist(window, lms_data):
    """
    Update the playlist UI element with the current playlist's information.
    
    Args:
        window (xbmcgui.WindowXML): The window object containing the UI elements.
        lms_data (dict): The LMS data to use for updating the UI.
    """
    playlist_data = get_playlist(lms_data)
    
    if playlist_data:
        update_playlist_items(window, playlist_data)
    else:
        log_message("No playlist information available.", LOG_LEVEL_WARNING)

def set_now_playing_labels(window, now_playing_data):
    """
    Set the 'now playing' labels with the current track's information.

    Args:
        window (xbmcgui.WindowXML): The window object containing the UI elements.
        now_playing_data (dict): The 'now playing' data to use for updating the UI.
    """
    window.getControl(CONTROL_ID_NOW_PLAYING_TITLE).setLabel(now_playing_data['title'])
    window.getControl(CONTROL_ID_NOW_PLAYING_ALBUM).setLabel(now_playing_data['album'])
    window.getControl(CONTROL_ID_NOW_PLAYING_ARTIST).setLabel(now_playing_data['artist'])

def set_now_playing_artwork(window, artwork_url):
    """
    Set the 'now playing' artwork with the current track's artwork.

    Args:
        window (xbmcgui.WindowXML): The window object containing the UI elements.
        artwork_url (str): The URL of the artwork to display.
    """
    artwork_url = artwork_url or DEFAULT_ARTWORK_PATH
    window.getControl(CONTROL_ID_ARTWORK_BACKGROUND).setImage(artwork_url)
    window.getControl(CONTROL_ID_ARTWORK).setImage(artwork_url)

def clear_now_playing_labels(window):
    """
    Clear the 'now playing' labels.

    Args:
        window (xbmcgui.WindowXML): The window object containing the UI elements.
    """
    window.getControl(CONTROL_ID_NOW_PLAYING_TITLE).setLabel("")
    window.getControl(CONTROL_ID_NOW_PLAYING_ALBUM).setLabel("")
    window.getControl(CONTROL_ID_NOW_PLAYING_ARTIST).setLabel("")

def set_default_artwork(window):
    """
    Set the default artwork.

    Args:
        window (xbmcgui.WindowXML): The window object containing the UI elements.
    """
    window.getControl(CONTROL_ID_ARTWORK_BACKGROUND).setImage(DEFAULT_ARTWORK_PATH)
    window.getControl(CONTROL_ID_ARTWORK).setImage(DEFAULT_ARTWORK_PATH)

def update_playlist_items(window, playlist_data):
    """
    Update the playlist items in the UI.

    Args:
        window (xbmcgui.WindowXML): The window object containing the UI elements.
        playlist_data (list): The playlist data to use for updating the UI.
    """
    playlist_control = window.getControl(CONTROL_ID_PLAYLIST)
    playlist_control.reset()
    
    for index, item in enumerate(playlist_data):
        li = xbmcgui.ListItem(label=item['title'])
        li.setProperty("id", str(LISTITEM_ID_PREFIX + index))
        info_tag = li.getMusicInfoTag()
        info_tag.setAlbum(item['album'])
        info_tag.setArtist(item['artist'])
        
        playlist_control.addItem(li)

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`, `xbmcgui`: Part of the Kodi API, used for various Kodi functionalities.
   - `get_now_playing`, `get_playlist`: Custom utility functions for getting now playing and playlist data.
   - `log_message`: Custom function for logging messages.
   - Constants imported from `constants.py`.

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

4. **Helper Functions:**
   - **set_now_playing_labels:** Sets the 'now playing' labels with the current track's information.
   - **set_now_playing_artwork:** Sets the 'now playing' artwork with the current track's artwork.
   - **clear_now_playing_labels:** Clears the 'now playing' labels.
   - **set_default_artwork:** Sets the default artwork.
   - **update_playlist_items:** Updates the playlist items in the UI.
"""


