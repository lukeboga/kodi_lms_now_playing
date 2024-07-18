from resources.lib.utils.log_message import log_message
import resources.lib.utils.global_config as global_config
from resources.lib.utils.error_handling import log_exception
from resources.lib.utils.constants import (
    LMS_SERVER_KEY,
    LMS_PORT_KEY,
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
    settings = global_config.settings
    
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
        
        log_message("Processed 'now playing' data")

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

        log_message("Processed 'playlist' data")

        return playlist
    except (KeyError, IndexError) as e:
        log_message(f"Error processing playlist data: {e}", LOG_LEVEL_ERROR)
        log_exception(e)
        return []

