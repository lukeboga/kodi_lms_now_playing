import xbmc
import xbmcgui
from resources.lib.api.fetch_lms_status import fetch_lms_status
from resources.lib.api.get_now_playing import get_now_playing
from resources.lib.api.get_playlist import get_playlist
from resources.lib.utils.log_message import log_message
from resources.lib.api.telnet_handler import set_update_ui_callback  # Import the callback setter

class NowPlaying(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_update_ui_callback(self.update_ui)  # Set the update UI callback

    def onInit(self):
        """
        Called when the window is initialized.
        Fetches and displays 'now playing' information.
        """
        self.lms_data = fetch_lms_status()
        self.init_elems()

    def init_elems(self):
        # Initialize controls
        self.artwork_background = self.getControl(1)
        self.artwork = self.getControl(2)
        self.now_playing_title = self.getControl(3)
        self.now_playing_album = self.getControl(4)
        self.now_playing_artist = self.getControl(5)
        self.playlist = self.getControl(6)

        # Populate UI elements
        self.populate_now_playing()
        self.populate_playlist()

    def update_ui(self, lms_data):
        """
        Update the UI based on the LMS data received.
        
        Args:
            lms_data (dict): The LMS data received from the telnet handler.
        """
        self.lms_data = lms_data
        self.populate_now_playing()
        self.populate_playlist()

    def populate_now_playing(self):
        """
        Populates the 'now playing' UI elements with the current track's information.
        """
        now_playing_data = get_now_playing(self.lms_data)
        
        if now_playing_data:
            # Update the labels with the now playing data
            self.now_playing_title.setLabel(now_playing_data['title'])
            self.now_playing_album.setLabel(now_playing_data['album'])
            self.now_playing_artist.setLabel(now_playing_data['artist'])

            # Update the artwork images
            artwork_url = now_playing_data.get('artwork_url', 'special://home/addons/plugin.program.klmsaddon/resources/media/demo-cover.jpg')
            self.artwork_background.setImage(artwork_url)
            self.artwork.setImage(artwork_url)
        else:
            log_message("No 'now playing' information available.", xbmc.LOGWARNING)
            # Clear the labels if no data is available
            self.now_playing_title.setLabel("")
            self.now_playing_album.setLabel("")
            self.now_playing_artist.setLabel("")
            # Set default artwork
            default_artwork = 'special://home/addons/plugin.program.klmsaddon/resources/media/demo-cover.jpg'
            self.artwork_background.setImage(default_artwork)
            self.artwork.setImage(default_artwork)

    def populate_playlist(self):
        """
        Populates the playlist UI element with the current playlist's information.
        """
        playlist_data = get_playlist(self.lms_data)
        
        if playlist_data:
            # Update playlist items
            self.playlist.reset()
            
            for index, item in enumerate(playlist_data):
                li = xbmcgui.ListItem(label=item['title'])
                li.setProperty("id", str(100 + index))
                info_tag = li.getMusicInfoTag()
                info_tag.setAlbum(item['album'])
                info_tag.setArtist(item['artist'])
                
                self.playlist.addItem(li)
        else:
            log_message("No 'now playing' information available.", xbmc.LOGWARNING)
    
    def onClick(self, controlId):
        pass

    def onAction(self, action):
        # This method is called when an action is performed
        if action == xbmcgui.ACTION_PREVIOUS_MENU or action == xbmcgui.ACTION_NAV_BACK:
            self.close()

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for various Kodi functionalities.
   - `xbmcgui`: Part of the Kodi API, used for GUI functionalities.
   - `fetch_lms_status`, `get_now_playing`, `get_playlist`, `log_message`, `set_update_ui_callback`: Custom utility functions and modules.

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
   - **Steps:** Updates the LMS data and populates the UI elements.

7. **populate_now_playing Method:**
   - **Purpose:** Populates the 'now playing' UI elements with the current track's information.
   - **Steps:** Updates the labels and artwork images with 'now playing' data.

8. **populate_playlist Method:**
   - **Purpose:** Populates the playlist UI element with the current playlist's information.
   - **Steps:** Updates the playlist items with data from the playlist.

9. **onClick Method:**
   - **Purpose:** Handles click events on the UI controls.
   - **Args:** `controlId`: The ID of the control that was clicked.

10. **onAction Method:**
    - **Purpose:** Handles action events in the UI.
    - **Args:** `action`: The action that was performed.
    - **Steps:** Closes the window if the action is to go back or exit.

"""

