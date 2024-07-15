import xbmc
import json
from resources.lib.utils.log_message import log_message

def get_now_playing(data):
    """
    Organizes the 'now playing' data from the JSON response.
    
    Args:
        data (dict): The JSON response data.
    
    Returns:
        dict: A dictionary containing the organized 'now playing' information.
    """
    try:
        now_playing = {
            'title': data['result']['playlist_loop'][0]['title'],
            'artist': data['result']['playlist_loop'][0]['artist'],
            'album': data['result']['playlist_loop'][0]['album'],
            'duration': data['result']['playlist_loop'][0]['duration'],
            'time': data['result']['time']
        }
        
        beautified_json = json.dumps(now_playing, indent=4) 
        log_message(f"Now playing data: {beautified_json}", xbmc.LOGINFO);

        return now_playing
    except (KeyError, IndexError) as e:
        # Log any errors encountered during data extraction
        log_message(f"Error processing now playing data: {e}", xbmc.LOGERROR)
        return None

