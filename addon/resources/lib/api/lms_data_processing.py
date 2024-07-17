import xbmc
import json
from resources.lib.utils.log_message import log_message
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.error_handling import log_exception

def get_now_playing(data):
    """
    Organizes the 'now playing' data from the JSON response.
    
    Args:
        data (dict): The JSON response data.
    
    Returns:
        dict: A dictionary containing the organized 'now playing' information.
    """
    settings = read_settings()
    
    try:
        track_info = data['result']['playlist_loop'][0]
        now_playing = {
            'title': track_info['title'],
            'artist': track_info['artist'],
            'album': track_info['album'],
            'duration': track_info['duration'],
            'time': data['result']['time'],
            'artwork_url': f"http://{settings['lms_server']}:{settings['lms_port']}{track_info['artwork_url']}"
        }
        
        beautified_json = json.dumps(now_playing, indent=4) 
        log_message(f"Now playing data: {beautified_json}", xbmc.LOGINFO)

        return now_playing
    except (KeyError, IndexError) as e:
        log_message(f"Error processing now playing data: {e}", xbmc.LOGERROR)
        log_exception(e)
        return None

def get_playlist(data):
    """
    Organizes the playlist data from the JSON response.
    
    Args:
        data (dict): The JSON response data.
    
    Returns:
        list: A list of dictionaries containing organized playlist information.
    """
    try:
        playlist_loop = data['result']['playlist_loop']
        playlist = [
            {
                'title': item['title'],
                'artist': item['artist'],
                'album': item['album'],
                'duration': item['duration']
            }
            for item in playlist_loop
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
   - `log_message`, `log_exception`, `read_settings`: Custom utility functions for logging messages, logging exceptions, and reading settings.

2. **get_now_playing Function:**
   - **Purpose:** Organizes the 'now playing' data from the JSON response.
   
   - **Args:**
     - `data (dict)`: The JSON response data.
   
   - **Returns:**
     - `dict`: A dictionary containing the organized 'now playing' information.
   
   - **Steps:**
     - Retrieves LMS settings using `read_settings`.
     - Extracts 'now playing' information from the JSON response.
     - Constructs the 'now playing' dictionary.
     - Logs the 'now playing' data in a beautified format.
     - Handles and logs any exceptions that occur during data extraction.
   
   - **Detailed Steps:**
     - `settings = read_settings()`: Retrieves LMS settings.
     - `track_info = data['result']['playlist_loop'][0]`: Extracts the first track's information from the playlist loop.
     - Constructs the `now_playing` dictionary by extracting relevant data from `track_info` and other parts of the JSON response.
     - `beautified_json = json.dumps(now_playing, indent=4)`: Beautifies the 'now playing' data for logging.
     - `log_message(f"Now playing data: {beautified_json}", xbmc.LOGINFO)`: Logs the beautified 'now playing' data.
     - `log_exception(e)`: Logs the exception and its traceback.

3. **get_playlist Function:**
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
     - `playlist_loop = data['result']['playlist_loop']`: Extracts the playlist loop from the JSON response.
     - Constructs the `playlist` list by extracting relevant data from each item in the `playlist_loop`.
     - `beautified_json = json.dumps(playlist, indent=4)`: Beautifies the playlist data for logging.
     - `log_message(f"Playlist data: {beautified_json}", xbmc.LOGINFO)`: Logs the beautified playlist data.
     - `log_exception(e)`: Logs the exception and its traceback.
"""

