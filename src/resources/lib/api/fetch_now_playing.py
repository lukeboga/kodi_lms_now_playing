# Import necessary modules
import requests
import xbmc
from resources.lib.utils.read_settings import read_settings
from resources.lib.utils.log_message import log_message

def get_now_playing():
    """
    Fetch the currently playing track information from the Logitech Media Server (LMS) using JSON-RPC.
    
    This function makes an HTTP POST request to the LMS to retrieve the current track information.
    It handles potential errors and logs the 'now playing' data to the Kodi log.
    
    Returns:
        dict: A dictionary containing the track title, artist, album, duration, and current playback time.
    """
    # Retrieve LMS settings
    settings = read_settings()
    url = f"http://{settings['lms_server']}:{settings['lms_port']}/jsonrpc.js"
    payload = {
        "method": "slim.request",
        "params": [settings['lms_player_id'], ["status", "-", 10, "tags:adKl"]],
        "id": 1
    }

    try:
        # Make the API request to the LMS
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()  # Parse the JSON response

        # Extract relevant 'now playing' information
        now_playing = {
            'title': data['result']['playlist_loop'][0]['title'],
            'artist': data['result']['playlist_loop'][0]['artist'],
            'album': data['result']['playlist_loop'][0]['album'],
            'duration': data['result']['playlist_loop'][0]['duration'],
            'time': data['result']['time']
        }

        return now_playing
    except requests.RequestException as e:
        # Log any errors encountered during the API request
        log_message(f"Error fetching now playing: {e}", xbmc.LOGERROR)
        return None
    except (KeyError, IndexError) as e:
        # Log any errors encountered during data extraction
        log_message(f"Error processing now playing data: {e}", xbmc.LOGERROR)
        return None

