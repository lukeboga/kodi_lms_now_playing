import xbmc
import json
from resources.lib.utils.log_message import log_message

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
        log_message(f"Playlist data: {beautified_json}", xbmc.LOGINFO);

        return playlist
    except (KeyError, IndexError) as e:
        # Log any errors encountered during data extraction
        log_message(f"Error processing playlist data: {e}", xbmc.LOGERROR)
        return []

