import xbmc
import xbmcgui
from resources.lib.api.fetch_now_playing import get_now_playing
from resources.lib.api.log_now_playing import log_now_playing
from resources.lib.utils.log_message import log_message

class NowPlaying(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def onInit(self):
        now_playing = get_now_playing()

        if now_playing:
            log_now_playing(now_playing)
        else:
            log_message("No 'now playing' information available.", xbmc.LOGWARNING)
        pass

    def onClick(self, controlId):
        pass

    def onAction(self, action):
        # This method is called when an action is performed
        if action == xbmcgui.ACTION_PREVIOUS_MENU or action == xbmcgui.ACTION_NAV_BACK:
            self.close()

