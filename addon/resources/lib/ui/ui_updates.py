import xbmcgui
from resources.lib.api.lms_data_processing import get_now_playing, get_playlist
from resources.lib.utils.log_message import log_message
from resources.lib.utils.constants import (
    LOG_LEVEL_WARNING,
    DEFAULT_ARTWORK_PATH,
    LISTITEM_ID_PREFIX
)

def update_now_playing(el, lms_data):
    """
    Update the 'now playing' UI elements with the current track's information.
    
    Args:
        el (UIElements): The object containing the UI elements.
        lms_data (dict): The LMS data to use for updating the UI.
    """
    now_playing_data = get_now_playing(lms_data)
    
    if now_playing_data:
        set_now_playing_labels(el, now_playing_data)
        set_now_playing_artwork(el, now_playing_data['artwork_url'])
    else:
        log_message("No 'now playing' information available.", LOG_LEVEL_WARNING)
        clear_now_playing_labels(el)
        set_default_artwork(el)

def update_playlist(el, lms_data):
    """
    Update the playlist UI element with the current playlist's information.
    
    Args:
        el (UIElements): The object containing the UI elements.
        lms_data (dict): The LMS data to use for updating the UI.
    """
    playlist_data = get_playlist(lms_data)
    
    if playlist_data:
        update_playlist_items(el, playlist_data)
    else:
        log_message("No playlist information available.", LOG_LEVEL_WARNING)

def set_now_playing_labels(el, now_playing_data):
    """
    Set the 'now playing' labels with the current track's information.

    Args:
        el (UIElements): The object containing the UI elements.
        now_playing_data (dict): The 'now playing' data to use for updating the UI.
    """
    el.now_playing_title.setLabel(now_playing_data['title'])
    el.now_playing_artist.setLabel(now_playing_data['artist'])
    el.now_playing_album.setLabel(now_playing_data['album'])

def set_now_playing_artwork(el, artwork_url):
    """
    Set the 'now playing' artwork with the current track's artwork.

    Args:
        el (UIElements): The object containing the UI elements.
        artwork_url (str): The URL of the artwork to display.
    """
    artwork_url = artwork_url or DEFAULT_ARTWORK_PATH
    el.artwork_background.setImage(artwork_url)
    el.artwork.setImage(artwork_url)

def clear_now_playing_labels(el):
    """
    Clear the 'now playing' labels.

    Args:
        el (UIElements): The object containing the UI elements.
    """
    el.now_playing_title.setLabel("")
    el.now_playing_artist.setLabel("")
    el.now_playing_album.setLabel("")

def set_default_artwork(el):
    """
    Set the default artwork.

    Args:
        el (UIElements): The object containing the UI elements.
    """
    el.artwork_background.setImage(DEFAULT_ARTWORK_PATH)
    el.artwork.setImage(DEFAULT_ARTWORK_PATH)

def update_playlist_items(el, playlist_data):
    """
    Update the playlist items in the UI.

    Args:
        el (UIElements): The object containing the UI elements.
        playlist_data (list): The playlist data to use for updating the UI.
    """
    playlist_control = el.playlist
    playlist_control.reset()
    
    for index, item in enumerate(playlist_data):
        li = xbmcgui.ListItem(label=item['title'])
        li.setProperty("id", str(LISTITEM_ID_PREFIX + index))
        info_tag = li.getMusicInfoTag()
        info_tag.setAlbum(item['album'])
        info_tag.setArtist(item['artist'])
        
        playlist_control.addItem(li)

