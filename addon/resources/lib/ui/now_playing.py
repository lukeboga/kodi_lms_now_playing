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
        self.init_elems();

    def init_elems(self):
        WINDOW_ID = xbmcgui.getCurrentWindowId()
        VW = xbmcgui.getScreenWidth()
        VH = xbmcgui.getScreenHeight()
        VW_50 = round(VW * 0.5)
        VH_50 = round(VH * 0.5)
        
        self.now_playing_title = self.getControl(1)
        self.now_playing_album = self.getControl(2)
        self.now_playing_artist = self.getControl(3)

        self.set_now_playing()

    def set_now_playing(self):
        lms_status = fetch_lms_status()
        now_playing = get_now_playing(lms_status)
        playlist = get_playlist(lms_status)
        
        if now_playing:
            pass
            # log_now_playing(now_playing)
        else:
            log_message("No 'now playing' information available.", xbmc.LOGWARNING)
    
    def onClick(self, controlId):
        pass

    def onAction(self, action):
        # This method is called when an action is performed
        if action == xbmcgui.ACTION_PREVIOUS_MENU or action == xbmcgui.ACTION_NAV_BACK:
            self.close()
