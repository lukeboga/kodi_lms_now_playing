# Import necessary modules
import requests
import xbmc
from resources.lib.utils.log_message import log_message
from resources.lib.utils.read_settings import read_settings

def get_now_playing():
    """
    Fetch the currently playing track information from the Logitech Media Server (LMS).
    
    This function makes an HTTP GET request to the LMS to retrieve the current track information.
    It handles potential errors and logs the 'now playing' data to the Kodi log.
    
    Returns:
        dict: A dictionary containing the track title, artist, album, duration, and current playback time.
    """
    # Retrieve LMS settings
    settings = read_settings()
    url = f"http://{settings['lms_server']}:{settings['lms_port']}/status.json"
    params = {'player': settings['lms_player_id']}
    
    try:
        # Make the API request to the LMS
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()  # Parse the JSON response
        
        # Extract relevant 'now playing' information
        now_playing = {
            'title': data['player']['current_title'],
            'artist': data['player']['current_artist'],
            'album': data['player']['current_album'],
            'duration': data['player']['duration'],
            'time': data['player']['time']
        }
        
        # Log the 'now playing' data to the Kodi log
        log_now_playing(now_playing)
        
        return now_playing
    except requests.RequestException as e:
        # Log any errors encountered during the API request
        xbmc.log(f"Error fetching now playing: {e}", level=xbmc.LOGERROR)
        return None

def log_now_playing(data):
    """
    Log the 'now playing' data to the Kodi log in a readable format.
    
    Parameters:
        data (dict): A dictionary containing the 'now playing' information.
    """
    # Format the 'now playing' information into a readable string
    log_message = (
        f"Now Playing: {data['title']} by {data['artist']} from the album {data['album']} "
        f"[{data['time']}/{data['duration']} seconds]"
    )
    # Log the formatted string to the Kodi log
    xbmc.log(log_message, level=xbmc.LOGINFO)

