import xbmc
import xbmcgui
from resources.lib.api.fetch_lms_status import fetch_lms_status
from resources.lib.api.get_now_playing import get_now_playing
from resources.lib.api.get_playlist import get_playlist
from resources.lib.utils.log_message import log_message


WINDOW = "NowPlaying"
TRACK_TITLE_POS_X = "TrackTitlePosX"

class NowPlaying(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def onInit(self):
        """
        Called when the window is initialized.
        Fetches and displays 'now playing' information.
        """
        self.lms_data = fetch_lms_status()
        self.init_elems()

    def init_elems(self):
        self.now_playing_title = self.getControl(1)
        self.now_playing_album = self.getControl(2)
        self.now_playing_artist = self.getControl(3)
        self.playlist = self.getControl(4)

        self.populate_now_playing()
        self.populate_playlist()

    def populate_now_playing(self):
        now_playing_data = get_now_playing(self.lms_data)
        
        if now_playing_data:
            pass
        else:
            log_message("No 'now playing' information available.", xbmc.LOGWARNING)
    
    def populate_playlist(self):
        playlist_data = get_playlist(self.lms_data)
        
        if playlist_data:
            pass
        else:
            log_message("No 'now playing' information available.", xbmc.LOGWARNING)
    
    def onClick(self, controlId):
        pass

    def onAction(self, action):
        # This method is called when an action is performed
        if action == xbmcgui.ACTION_PREVIOUS_MENU or action == xbmcgui.ACTION_NAV_BACK:
            self.close()
