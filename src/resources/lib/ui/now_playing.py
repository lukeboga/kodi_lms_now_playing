import xbmc
import xbmcgui
from resources.lib.api.fetch_now_playing import get_now_playing
from resources.lib.api.log_now_playing import log_now_playing
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
        
        self.Meta = self.getControl(999);
        self.Meta.setLabel(f"{WINDOW_ID}");
        
        self.TrackTitle = self.getControl(1);
        self.TrackTitle_width = self.TrackTitle.getWidth();
        self.TrackTitle_height = self.TrackTitle.getHeight();
        
        # self.TrackTitle.setPosition(10, 10)

        log_message(f"{self.TrackTitle_width} x {self.TrackTitle_height}")
        

    def get_elem_size(self, elem):
        width = elem.getWidth()
        height = elem.getheight()

        return { width, height }
        
    def set_now_playing(self):
        now_playing = get_now_playing()
        if now_playing:
            log_now_playing(now_playing)
        else:
            log_message("No 'now playing' information available.", xbmc.LOGWARNING)
    
    def onClick(self, controlId):
        pass

    def onAction(self, action):
        # This method is called when an action is performed
        if action == xbmcgui.ACTION_PREVIOUS_MENU or action == xbmcgui.ACTION_NAV_BACK:
            self.close()
