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
        now_playing = {
            'title': data['result']['playlist_loop'][0]['title'],
            'artist': data['result']['playlist_loop'][0]['artist'],
            'album': data['result']['playlist_loop'][0]['album'],
            'duration': data['result']['playlist_loop'][0]['duration'],
            'time': data['result']['time'],
            'artwork_url': f"http://{settings['lms_server']}:{settings['lms_port']}{data['result']['playlist_loop'][0]['artwork_url']}"
        }
        
        beautified_json = json.dumps(now_playing, indent=4) 
        log_message(f"Now playing data: {beautified_json}", xbmc.LOGINFO)

        return now_playing
    except (KeyError, IndexError) as e:
        log_message(f"Error processing now playing data: {e}", xbmc.LOGERROR)
        log_exception(e)
        return None

"""
Detailed Explanation for Beginners:
-----------------------------------

1. **Importing Necessary Modules:**
   - `xbmc`: Part of the Kodi API, used for logging.
   - `json`: For handling JSON data.
   - `log_message`, `read_settings`, `log_exception`: Custom utility functions for logging messages, reading settings, and logging exceptions.

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
     - Constructs the `now_playing` dictionary by extracting relevant data from the JSON response.
     - `beautified_json = json.dumps(now_playing, indent=4)`: Beautifies the 'now playing' data for logging.
     - `log_message(f"Now playing data: {beautified_json}", xbmc.LOGINFO)`: Logs the beautified 'now playing' data.
     - `log_exception(e)`: Logs the exception and its traceback.
"""

