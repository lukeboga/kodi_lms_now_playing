import xbmc
import xbmcgui
from resources.lib.api.fetch_lms_status import fetch_lms_status
from resources.lib.api.lms_data_processing import get_now_playing, get_playlist
from resources.lib.utils.log_message import log_message
from resources.lib.api.telnet_handler import telnet_handler  # Import the telnet handler instance
from resources.lib.ui.ui_updates import update_now_playing, update_playlist  # Import the UI update functions
from resources.lib.utils.constants import (
    LOG_LEVEL_INFO,
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
        telnet_handler.set_update_ui_callback(self.update_ui)  # Set the update UI callback

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
        self.artwork_background = self.getControl(CONTROL_ID_ARTWORK_BACKGROUND)
        self.artwork = self.getControl(CONTROL_ID_ARTWORK)
        self.now_playing_title = self.getControl(CONTROL_ID_NOW_PLAYING_TITLE)
        self.now_playing_album = self.getControl(CONTROL_ID_NOW_PLAYING_ALBUM)
        self.now_playing_artist = self.getControl(CONTROL_ID_NOW_PLAYING_ARTIST)
        self.playlist = self.getControl(CONTROL_ID_PLAYLIST)

        self.update_ui(self.lms_data)

    def update_ui(self, lms_data):
        """
        Update the UI based on the LMS data received.
        
        Args:
            lms_data (dict): The LMS data received from the telnet handler.
        """
        self.lms_data = lms_data
        update_now_playing(self, self.lms_data)
        update_playlist(self, self.lms_data)

    def onClick(self, controlId):
        pass

    def onAction(self, action):
        """
        Handle action events in the UI.

        Args:
            action: The action that was performed.
        """
        if action == xbmcgui.ACTION_PREVIOUS_MENU or action == xbmcgui.ACTION_NAV_BACK:
            self.close()

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for various Kodi functionalities.
   - `xbmcgui`: Part of the Kodi API, used for GUI functionalities.
   - `fetch_lms_status`, `get_now_playing`, `get_playlist`, `log_message`, `telnet_handler`: Custom utility functions and modules.
   - `update_now_playing`, `update_playlist`: Functions from `ui_updates.py` for updating the UI elements.
   - `LOG_LEVEL_INFO`, `CONTROL_ID_ARTWORK_BACKGROUND`, `CONTROL_ID_ARTWORK`, `CONTROL_ID_NOW_PLAYING_TITLE`, `CONTROL_ID_NOW_PLAYING_ALBUM`, `CONTROL_ID_NOW_PLAYING_ARTIST`, `CONTROL_ID_PLAYLIST`: Constants imported from `constants.py`.

2. **NowPlaying Class:**
   - **Purpose:** Manages the 'Now Playing' window in the Kodi addon.
   - **Inheritance:** Inherits from `xbmcgui.WindowXML`.

3. **__init__ Method:**
   - **Purpose:** Initializes the class and sets the update UI callback.
   - **Args:** `*args`, `**kwargs`: Variable arguments for the class initialization.

4. **onInit Method:**
   - **Purpose:** Called when the window is initialized. Fetches and displays 'now playing' information.
   - **Steps:** Fetches LMS data and initializes UI elements.

5. **init_elems Method:**
   - **Purpose:** Initializes controls and populates UI elements.
   - **Steps:** Gets references to UI controls and populates them with data.

6. **update_ui Method:**
   - **Purpose:** Updates the UI based on the LMS data received.
   - **Args:** `lms_data (dict)`: The LMS data received from the telnet handler.
   - **Steps:** Updates the LMS data and populates the UI elements using `update_now_playing` and `update_playlist` functions.

7. **onClick Method:**
   - **Purpose:** Handles click events on the UI controls.
   - **Args:** `controlId`: The ID of the control that was clicked.

8. **onAction Method:**
   - **Purpose:** Handles action events in the UI.
   - **Args:** `action`: The action that was performed.
   - **Steps:** Closes the window if the action is to go back or exit.
"""


