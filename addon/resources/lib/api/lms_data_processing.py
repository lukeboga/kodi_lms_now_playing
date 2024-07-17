import xbmc
import json
from resources.lib.utils.log_message import log_message
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.error_handling import log_exception
from resources.lib.utils.constants import (
    LMS_SERVER_KEY,
    LMS_PORT_KEY,
    LOG_LEVEL_INFO,
    LOG_LEVEL_ERROR,
    LMS_RESULT_KEY,
    LMS_PLAYLIST_LOOP_KEY,
    LMS_TIME_KEY
)

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
        track_info = data[LMS_RESULT_KEY][LMS_PLAYLIST_LOOP_KEY][0]
        now_playing = {
            'title': track_info['title'],
            'artist': track_info['artist'],
            'album': track_info['album'],
            'duration': track_info['duration'],
            'time': data[LMS_RESULT_KEY][LMS_TIME_KEY],
            'artwork_url': f"http://{settings[LMS_SERVER_KEY]}:{settings[LMS_PORT_KEY]}{track_info['artwork_url']}"
        }
        
        log_message("New 'now playing' data processed", LOG_LEVEL_INFO)

        return now_playing
    except (KeyError, IndexError) as e:
        log_message(f"Error processing now playing data: {e}", LOG_LEVEL_ERROR)
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
        playlist_loop = data[LMS_RESULT_KEY][LMS_PLAYLIST_LOOP_KEY]
        playlist = [
            {
                'title': item['title'],
                'artist': item['artist'],
                'album': item['album'],
                'duration': item['duration']
            }
            for item in playlist_loop
        ]

        log_message("New 'playlist' data processed", LOG_LEVEL_INFO)

        return playlist
    except (KeyError, IndexError) as e:
        log_message(f"Error processing playlist data: {e}", LOG_LEVEL_ERROR)
        log_exception(e)
        return []

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for logging.
   - `json`: For handling JSON data.
   - `log_message`, `log_exception`, `read_settings`: Custom utility functions for logging messages, logging exceptions, and reading settings.
   - `LMS_SERVER_KEY`, `LMS_PORT_KEY`, `LOG_LEVEL_INFO`, `LOG_LEVEL_ERROR`, `LMS_RESULT_KEY`, `LMS_PLAYLIST_LOOP_KEY`, `LMS_TIME_KEY`: Constants imported from `constants.py`.

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
     - Logs the 'now playing' data.
     - Handles and logs any exceptions that occur during data extraction.
   
   - **Detailed Steps:**
     - `settings = read_settings()`: Retrieves LMS settings.
     - `track_info = data[LMS_RESULT_KEY][LMS_PLAYLIST_LOOP_KEY][0]`: Extracts the first track's information from the playlist loop.
     - Constructs the `now_playing` dictionary by extracting relevant data from `track_info` and other parts of the JSON response.
     - `log_message("New 'now playing' data processed", LOG_LEVEL_INFO)`: Logs the 'now playing' data.
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
     - Logs the playlist data.
     - Handles and logs any exceptions that occur during data extraction.
   
   - **Detailed Steps:**
     - `playlist_loop = data[LMS_RESULT_KEY][LMS_PLAYLIST_LOOP_KEY]`: Extracts the playlist loop from the JSON response.
     - Constructs the `playlist` list by extracting relevant data from each item in the `playlist_loop`.
     - `log_message("New 'playlist' data processed", LOG_LEVEL_INFO)`: Logs the playlist data.
     - `log_exception(e)`: Logs the exception and its traceback.
"""


