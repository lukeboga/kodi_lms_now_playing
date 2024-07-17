import xbmc
import json
from resources.lib.utils.log_message import log_message
from resources.lib.utils.error_handling import log_exception

def get_playlist(data):
    """
    Organizes the playlist data from the JSON response.
    
    Args:
        data (dict): The JSON response data.
    
    Returns:
        list: A list of dictionaries containing organized playlist information.
    """
    try:
        playlist = [
            {
                'title': item['title'],
                'artist': item['artist'],
                'album': item['album'],
                'duration': item['duration']
            }
            for item in data['result']['playlist_loop']
        ]

        beautified_json = json.dumps(playlist, indent=4) 
        log_message(f"Playlist data: {beautified_json}", xbmc.LOGINFO)

        return playlist
    except (KeyError, IndexError) as e:
        log_message(f"Error processing playlist data: {e}", xbmc.LOGERROR)
        log_exception(e)
        return []

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for logging.
   - `json`: For handling JSON data.
   - `log_message`, `log_exception`: Custom utility functions for logging messages and logging exceptions.

2. **get_playlist Function:**
   - **Purpose:** Organizes the playlist data from the JSON response.
   
   - **Args:**
     - `data (dict)`: The JSON response data.
   
   - **Returns:**
     - `list`: A list of dictionaries containing organized playlist information.
   
   - **Steps:**
     - Tries to extract the playlist data from the JSON response.
     - Constructs a list of dictionaries, each representing a track in the playlist.
     - Logs the playlist data in a beautified format.
     - Handles and logs any exceptions that occur during data extraction.
   
   - **Detailed Steps:**
     - Constructs the `playlist` list by extracting relevant data from each item in the JSON response's `playlist_loop`.
     - `beautified_json = json.dumps(playlist, indent=4)`: Beautifies the playlist data for logging.
     - `log_message(f"Playlist data: {beautified_json}", xbmc.LOGINFO)`: Logs the beautified playlist data.
     - `log_exception(e)`: Logs the exception and its traceback.
"""

