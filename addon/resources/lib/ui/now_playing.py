import xbmcgui
from resources.lib.api.fetch_lms_status import fetch_lms_status
from resources.lib.api.telnet_handler import telnet_handler
from resources.lib.ui.ui_updates import update_now_playing, update_playlist
from resources.lib.utils.shutdown_handler import shutdown_addon
from resources.lib.ui.ui_elements import ui_elements
from resources.lib.utils.constants import (
    CONTROL_ID_ARTWORK_BACKGROUND,
    CONTROL_ID_ARTWORK,
    CONTROL_ID_NOW_PLAYING_TITLE,
    CONTROL_ID_NOW_PLAYING_ALBUM,
    CONTROL_ID_NOW_PLAYING_ARTIST,
    CONTROL_ID_PLAYLIST
)

class NowPlaying(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.el = ui_elements  # Use the imported instance
        telnet_handler.set_update_ui_callback(self.update_ui)

    def onInit(self):
        """
        Called when the window is initialized.
        Fetches and displays 'now playing' information.
        """
        self.lms_data = fetch_lms_status()
        self.init_elems()

    def init_elems(self):
        """
        Initialize UI controls and populate them with data.
        """
        self.el.artwork_background = self.getControl(CONTROL_ID_ARTWORK_BACKGROUND)
        self.el.artwork = self.getControl(CONTROL_ID_ARTWORK)
        self.el.now_playing_title = self.getControl(CONTROL_ID_NOW_PLAYING_TITLE)
        self.el.now_playing_artist = self.getControl(CONTROL_ID_NOW_PLAYING_ARTIST)
        self.el.now_playing_album = self.getControl(CONTROL_ID_NOW_PLAYING_ALBUM)
        self.el.playlist = self.getControl(CONTROL_ID_PLAYLIST)

        self.update_ui(self.lms_data)

    def update_ui(self, lms_data):
        """
        Update the UI based on the LMS data received.
        
        Args:
            lms_data (dict): The LMS data received from the telnet handler.
        """
        update_now_playing(self.el, lms_data)
        update_playlist(self.el, lms_data)

    def onClick(self, controlId):
        pass

    def onAction(self, action):
        """
        Handle action events in the UI.

        Args:
            action: The action that was performed.
        """
        if action == xbmcgui.ACTION_PREVIOUS_MENU or action == xbmcgui.ACTION_NAV_BACK:
            shutdown_addon()
            self.close()

