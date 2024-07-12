# Import necessary modules from the Kodi API and the custom libraries
import xbmcgui
import xbmcplugin
import xbmc
from resources.lib.api.fetch_now_playing import get_now_playing
from resources.lib.api.log_now_playing import log_now_playing
from resources.lib.utils.log_message import log_message

def list_items(handle):
    """
    Lists the 'now playing' information in the Kodi interface.
    
    Parameters:
        handle (int): The unique identifier for the plugin instance.
    """
    now_playing = get_now_playing()
    if now_playing:
        li = xbmcgui.ListItem(now_playing['title'])
        info_tag = li.getMusicInfoTag()
        info_tag.setTitle(now_playing['title'])
        info_tag.setArtist(now_playing['artist'])
        info_tag.setAlbum(now_playing['album'])
        xbmcplugin.addDirectoryItem(handle, '', li, False)
        log_now_playing(now_playing)
    else:
        log_message("No 'now playing' information available.", xbmc.LOGWARNING)
    xbmcplugin.endOfDirectory(handle)

